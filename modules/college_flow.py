import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

class CollegeFlow:
    def __init__(self):
        self.current_step = 1
        self.total_steps = 5
        self.db_manager = None  # Initialize as None
        self.demo_mode = True  # Default to demo mode
        
        # Initialize college data
        self.college_data = {
            "profile": {
                "name": "",
                "address": "",
                "website": "",
                "contact_email": "",
                "contact_phone": "",
                "placement_officer": "",
                "departments": [],
                "accreditation": "",
                "established_year": ""
            },
            "students": [],
            "placements": [],
            "recruiters": [],
            "reports": []
        }
        
        # Load demo data if no db connection
        if self.db_manager is None:
            self.load_demo_data()
    
    def set_database_manager(self, db_manager, demo_mode=False):
        """Set the database manager for this flow"""
        self.db_manager = db_manager
        self.demo_mode = demo_mode
        
        # If we have a db manager, try to load data
        if not self.demo_mode and self.db_manager:
            self.load_from_database()
        else:
            self.load_demo_data()
    
    def load_demo_data(self):
        """Load demo data for testing"""
        self.college_data = {
            "profile": {
                "name": "IIT Bombay",
                "address": "Powai, Mumbai, Maharashtra 400076",
                "website": "https://www.iitb.ac.in",
                "contact_email": "placement@iitb.ac.in",
                "contact_phone": "+91 22 2572 2545",
                "placement_officer": "Dr. Rajesh Kumar",
                "departments": ["Computer Science", "Electrical", "Mechanical", "Civil", "Chemical"],
                "accreditation": "NAAC A++",
                "established_year": "1958"
            },
            "students": [
                {"id": "2023CS001", "name": "John Doe", "department": "Computer Science", "cgpa": 8.5, "status": "Placed"},
                {"id": "2023CS002", "name": "Jane Smith", "department": "Computer Science", "cgpa": 9.2, "status": "Placed"},
                {"id": "2023EE001", "name": "Bob Johnson", "department": "Electrical", "cgpa": 7.8, "status": "Seeking"}
            ],
            "placements": [
                {"company": "Google", "students_placed": 15, "avg_package": 25.5, "year": "2023"},
                {"company": "Microsoft", "students_placed": 12, "avg_package": 22.0, "year": "2023"}
            ],
            "recruiters": ["Google", "Microsoft", "Amazon", "TCS", "Infosys"],
            "reports": []
        }
    
    def load_from_database(self):
        """Load college data from database"""
        try:
            if self.db_manager and hasattr(self.db_manager, 'get_college_profile'):
                # Try to get college profile from database
                college_id = st.session_state.get('college_id')
                if college_id:
                    profile = self.db_manager.get_college_profile(college_id)
                    if profile:
                        self.college_data["profile"] = profile
                        
                        # Load other data
                        self.college_data["students"] = self.db_manager.get_college_students(college_id)
                        self.college_data["placements"] = self.db_manager.get_college_placements(college_id)
                        self.college_data["recruiters"] = self.db_manager.get_college_recruiters(college_id)
                        self.college_data["reports"] = self.db_manager.get_college_reports(college_id)
        except Exception as e:
            st.error(f"Error loading from database: {e}")
            self.load_demo_data()
    
    def save_profile_to_database(self):
        """Save college profile to database"""
        try:
            if self.demo_mode or not self.db_manager:
                st.warning("⚠️ Running in demo mode - Profile saved locally only")
                return True
            
            # Check if we have required methods
            if not hasattr(self.db_manager, 'save_college_profile'):
                st.error("Database manager doesn't support saving college profiles")
                return False
            
            # Prepare profile data
            profile_data = self.college_data["profile"].copy()
            
            # Add college ID if available in session state
            college_id = st.session_state.get('college_id')
            if college_id:
                profile_data['id'] = college_id
            
            # Save profile
            success = self.db_manager.save_college_profile(profile_data)
            
            if success:
                st.success("✅ College profile saved to database successfully!")
                return True
            else:
                st.error("❌ Failed to save profile to database")
                return False
                
        except Exception as e:
            st.error(f"❌ Error saving to database: {str(e)}")
            return False
    
    def display(self):
        """Main display method"""
        st.header("🏫 College Admin Dashboard")
        
        # Display current step
        self.display_progress_bar()
        
        # Display step content
        if self.current_step == 1:
            self.step1_college_profile()
        elif self.current_step == 2:
            self.step2_student_management()
        elif self.current_step == 3:
            self.step3_placement_tracking()
        elif self.current_step == 4:
            self.step4_recruiter_management()
        elif self.current_step == 5:
            self.step5_reports_analytics()
    
    def step1_college_profile(self):
        """Step 1: College Profile Setup"""
        st.subheader("🏫 College Profile Setup")
        
        with st.form("college_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("College Name*", 
                                    value=self.college_data["profile"]["name"])
                address = st.text_area("Address*", 
                                      value=self.college_data["profile"]["address"],
                                      height=100)
                website = st.text_input("Website", 
                                       value=self.college_data["profile"]["website"])
            
            with col2:
                contact_email = st.text_input("Contact Email*", 
                                             value=self.college_data["profile"]["contact_email"])
                contact_phone = st.text_input("Contact Phone*", 
                                             value=self.college_data["profile"]["contact_phone"])
                placement_officer = st.text_input("Placement Officer*", 
                                                 value=self.college_data["profile"]["placement_officer"])
            
            # Departments
            st.subheader("🎓 Departments")
            department_options = [
                "Computer Science", "Electronics", "Mechanical", "Civil",
                "Electrical", "Chemical", "Biotechnology", "Mathematics",
                "Physics", "Chemistry", "Humanities", "Others"
            ]
            
            selected_departments = st.multiselect(
                "Select Departments",
                department_options,
                default=self.college_data["profile"]["departments"]
            )
            
            # Additional Info
            col3, col4 = st.columns(2)
            with col3:
                accreditation = st.text_input("Accreditation", 
                                             value=self.college_data["profile"]["accreditation"])
            with col4:
                established_year = st.text_input("Established Year", 
                                                value=self.college_data["profile"]["established_year"])
            
            if st.form_submit_button("💾 Save College Profile"):
                # Validate required fields
                if not all([name, address, contact_email, contact_phone, placement_officer]):
                    st.error("Please fill in all required fields (*)")
                else:
                    # Update college data
                    self.college_data["profile"].update({
                        "name": name,
                        "address": address,
                        "website": website,
                        "contact_email": contact_email,
                        "contact_phone": contact_phone,
                        "placement_officer": placement_officer,
                        "departments": selected_departments,
                        "accreditation": accreditation,
                        "established_year": established_year
                    })
                    
                    # Try to save to database
                    save_success = self.save_profile_to_database()
                    
                    if save_success:
                        st.success("✅ College profile saved successfully!")
                        st.balloons()
                    else:
                        st.info("Profile saved locally (demo mode)")
        
        # Display college profile summary
        self.display_college_summary()
    
    def step2_student_management(self):
        """Step 2: Student Management"""
        st.subheader("👨‍🎓 Student Management")
        
        # Bulk upload option
        st.write("### 📥 Bulk Student Upload")
        
        uploaded_file = st.file_uploader("Upload student data (CSV/Excel)", 
                                        type=['csv', 'xlsx', 'xls'])
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                st.success(f"✅ Successfully loaded {len(df)} student records")
                
                # Show preview
                with st.expander("Preview Data"):
                    st.dataframe(df.head(), use_container_width=True)
                
                # Process and save data
                if st.button("📋 Process and Save Student Data"):
                    with st.spinner("Processing student data..."):
                        # Convert to list of dictionaries
                        students_data = df.to_dict('records')
                        
                        # Update college data
                        self.college_data["students"].extend(students_data)
                        
                        # Save to database if available
                        if not self.demo_mode and self.db_manager:
                            try:
                                college_id = st.session_state.get('college_id')
                                if college_id and hasattr(self.db_manager, 'bulk_save_students'):
                                    success_count = self.db_manager.bulk_save_students(college_id, students_data)
                                    st.success(f"✅ Saved {success_count} students to database")
                            except Exception as e:
                                st.warning(f"Could not save to database: {e}")
                                st.info("Data saved locally only")
                        else:
                            st.info("Data saved locally (demo mode)")
                        
                        st.rerun()
                        
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        # Manual student addition
        st.write("### 👤 Add Student Manually")
        
        with st.form("add_student_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                student_id = st.text_input("Student ID*")
                student_name = st.text_input("Full Name*")
                department = st.selectbox("Department", 
                                         self.college_data["profile"]["departments"] 
                                         if self.college_data["profile"]["departments"] 
                                         else ["Computer Science"])
            
            with col2:
                cgpa = st.number_input("CGPA*", 0.0, 10.0, 7.0, 0.1)
                email = st.text_input("Email*")
                status = st.selectbox("Placement Status", 
                                     ["Placed", "Seeking", "Not Looking", "Higher Studies"])
            
            if st.form_submit_button("➕ Add Student"):
                if not all([student_id, student_name, department, email]):
                    st.error("Please fill in all required fields (*)")
                else:
                    new_student = {
                        "id": student_id,
                        "name": student_name,
                        "department": department,
                        "cgpa": cgpa,
                        "email": email,
                        "status": status
                    }
                    
                    self.college_data["students"].append(new_student)
                    
                    # Save to database if available
                    if not self.demo_mode and self.db_manager:
                        try:
                            college_id = st.session_state.get('college_id')
                            if college_id and hasattr(self.db_manager, 'save_student'):
                                new_student['college_id'] = college_id
                                success = self.db_manager.save_student(new_student)
                                if success:
                                    st.success("✅ Student saved to database")
                        except Exception as e:
                            st.warning(f"Could not save to database: {e}")
                            st.info("Student saved locally only")
                    else:
                        st.info("Student saved locally (demo mode)")
                    
                    st.rerun()
        
        # Display student list
        st.write("### 📋 Student Directory")
        
        if self.college_data["students"]:
            # Create dataframe for display
            students_df = pd.DataFrame(self.college_data["students"])
            
            # Search and filter
            col1, col2 = st.columns(2)
            with col1:
                search_name = st.text_input("Search by name", "")
            with col2:
                filter_department = st.selectbox("Filter by department", 
                                                ["All"] + list(students_df['department'].unique()))
            
            # Apply filters
            filtered_df = students_df.copy()
            if search_name:
                filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]
            if filter_department != "All":
                filtered_df = filtered_df[filtered_df['department'] == filter_department]
            
            # Display table
            st.dataframe(filtered_df, use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", len(students_df))
            with col2:
                placed_count = len(students_df[students_df['status'] == 'Placed'])
                st.metric("Placed Students", placed_count)
            with col3:
                avg_cgpa = students_df['cgpa'].mean() if not students_df.empty else 0
                st.metric("Average CGPA", f"{avg_cgpa:.2f}")
        else:
            st.info("No student data available. Upload or add students to get started.")
    
   
    
    def step3_company_registration(self):
        """Step 3: Company Registration & Management"""
        st.info("Register and manage company profiles for campus recruitment")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("🏢 Company Registration")
            
            with st.form("company_registration_form"):
                company_name = st.text_input("Company Name *")
                industry = st.selectbox("Industry *", 
                                      options=["Technology", "Software", "E-commerce", 
                                              "IT Services", "Finance", "Manufacturing"])
                website = st.text_input("Website")
                contact_person = st.text_input("Contact Person *")
                contact_email = st.text_input("Contact Email *")
                contact_phone = st.text_input("Contact Phone")
                
                # Company requirements
                st.write("### Recruitment Requirements")
                min_cgpa = st.slider("Minimum CGPA", 0.0, 10.0, 7.0, 0.5)
                max_backlogs = st.number_input("Maximum Backlogs Allowed", 0, 10, 0)
                
                submit = st.form_submit_button("Register Company")
                
                if submit:
                    if company_name and contact_person and contact_email:
                        company_data = {
                            "name": company_name,
                            "industry": industry,
                            "website": website,
                            "contact_person": contact_person,
                            "email": contact_email,
                            "phone": contact_phone,
                            "min_cgpa": float(min_cgpa),
                            "max_backlogs": max_backlogs,
                            "status": "Active",
                            "created_at": datetime.now().isoformat()
                        }
                        
                        success = self.save_to_database('company', company_data)
                        
                        if success or st.session_state.demo_mode:
                            st.success(f"✅ Successfully registered {company_name}")
                            if not st.session_state.demo_mode:
                                st.success("✅ Company saved to database!")
                                # Refresh data
                                companies_data = self.get_from_database('companies')
                                if not companies_data.empty:
                                    self.college_data["companies"] = companies_data
                        else:
                            st.error("❌ Failed to register company")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Registered Companies")
            
            if self.college_data["companies"].empty:
                st.info("No companies registered yet")
                return
            
            # Display companies table
            display_cols = ["name", "industry", "contact_person", "email", "phone", "status", "total_hires", "avg_package"]
            available_cols = [col for col in display_cols if col in self.college_data["companies"].columns]
            
            st.dataframe(
                self.college_data["companies"][available_cols],
                use_container_width=True,
                height=400
            )
            
            # Company statistics
            st.subheader("📊 Company Statistics")
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                active_companies = len(self.college_data["companies"])
                st.metric("Active Companies", active_companies)
            with col_stats2:
                total_hires = self.college_data["companies"]["total_hires"].sum() if "total_hires" in self.college_data["companies"].columns else 0
                st.metric("Total Hires", total_hires)
            with col_stats3:
                if "avg_package" in self.college_data["companies"].columns:
                    avg_package = self.college_data["companies"]["avg_package"].mean()
                    st.metric("Avg Package", f"{avg_package:.1f} LPA")
                else:
                    st.metric("Avg Package", "N/A")
    
    def step4_drive_scheduling(self):
        """Step 4: Campus Drive Scheduling"""
        st.info("Schedule and manage campus recruitment drives")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📅 Schedule New Drive")
            
            # Get companies from database
            companies = []
            if not self.college_data["companies"].empty:
                companies = self.college_data["companies"]["name"].tolist()
            
            with st.form("schedule_drive_form"):
                company = st.selectbox(
                    "Select Company *",
                    options=companies if companies else ["Google", "Microsoft", "Amazon"]
                )
                drive_date = st.date_input("Drive Date *", min_value=datetime.now().date())
                drive_time = st.time_input("Drive Time", value=datetime.strptime("10:00", "%H:%M").time())
                mode = st.radio("Mode *", ["Online", "Offline", "Hybrid"])
                
                if mode != "Online":
                    venue = st.text_input("Venue *", value="Main Campus Auditorium")
                else:
                    venue = "Virtual"
                
                coordinator = st.text_input("Coordinator *", value="Placement Officer")
                job_roles = st.text_area("Job Roles *", value="Software Engineer, Data Analyst")
                
                submit = st.form_submit_button("Schedule Drive")
                
                if submit:
                    if company and coordinator and job_roles:
                        # In a real app, you would save this to a 'drives' table
                        st.success(f"✅ Drive scheduled for {company} on {drive_date}")
                        if not st.session_state.demo_mode:
                            st.info("Note: Drive scheduling database integration would be implemented here")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Upcoming Drives")
            
            # Display drives
            if not self.college_data["drives"].empty:
                drives_df = self.college_data["drives"].copy()
                drives_df["date"] = pd.to_datetime(drives_df["date"])
                upcoming_drives = drives_df[drives_df["date"] >= pd.Timestamp.now()]
                
                if not upcoming_drives.empty:
                    st.dataframe(
                        upcoming_drives[
                            ["company", "date", "mode", "venue", "coordinator", "status", "registered"]
                        ],
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.info("No upcoming drives scheduled")
            else:
                st.info("No drive data available")
            
            st.subheader("📊 Drive Statistics")
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                total_drives = len(self.college_data["drives"])
                st.metric("Total Drives", total_drives)
            with col_stats2:
                if not self.college_data["drives"].empty:
                    drives_df = self.college_data["drives"].copy()
                    drives_df["date"] = pd.to_datetime(drives_df["date"])
                    upcoming = len(drives_df[drives_df["date"] >= pd.Timestamp.now()])
                    st.metric("Upcoming", upcoming)
                else:
                    st.metric("Upcoming", 0)
            with col_stats3:
                if not self.college_data["drives"].empty:
                    completed = len(self.college_data["drives"][self.college_data["drives"]["status"] == "Completed"])
                    st.metric("Completed", completed)
                else:
                    st.metric("Completed", 0)
    
    def step5_student_company_matching(self):
        """Step 5: Student-Company Matching"""
        st.info("Match students with suitable companies based on criteria")
        
        if self.college_data["students"].empty or self.college_data["companies"].empty:
            st.warning("Student or company data not available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Matching Criteria")
            
            # Company selection
            selected_company = st.selectbox(
                "Select Company for Matching",
                options=self.college_data["companies"]["name"].tolist()
            )
            
            if selected_company:
                # Get company requirements (simulated)
                company_requirements = {
                    "min_cgpa": 7.5,
                    "max_backlogs": 1,
                    "preferred_departments": ["Computer Science", "Information Technology", "Electrical Engineering"],
                    "skills": ["Python", "Java", "SQL"]
                }
                
                st.write("### Company Requirements:")
                st.write(f"- Minimum CGPA: **{company_requirements['min_cgpa']}**")
                st.write(f"- Maximum Backlogs: **{company_requirements['max_backlogs']}**")
                st.write(f"- Preferred Departments: **{', '.join(company_requirements['preferred_departments'])}**")
                st.write(f"- Required Skills: **{', '.join(company_requirements['skills'])}**")
                
                # Match students
                matched_students = self.college_data["students"].copy()
                matched_students = matched_students[
                    (matched_students["cgpa"] >= company_requirements["min_cgpa"]) &
                    (matched_students["backlogs"] <= company_requirements["max_backlogs"]) &
                    (matched_students["department"].isin(company_requirements["preferred_departments"]))
                ]
                
                if "placement_status" in matched_students.columns:
                    matched_students = matched_students[matched_students["placement_status"] == "Not Placed"]
                
                st.metric("Matching Students", len(matched_students))
        
        with col2:
            st.subheader("👥 Matched Students")
            
            if 'matched_students' in locals() and not matched_students.empty:
                # Display matched students
                display_cols = ["id", "full_name", "department", "cgpa", "backlogs", "email"]
                available_cols = [col for col in display_cols if col in matched_students.columns]
                
                st.dataframe(
                    matched_students[available_cols].sort_values("cgpa", ascending=False),
                    use_container_width=True,
                    height=400
                )
                
                # Matching statistics
                st.subheader("📊 Matching Statistics")
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    avg_cgpa = matched_students["cgpa"].mean() if not matched_students.empty else 0
                    st.metric("Avg CGPA", f"{avg_cgpa:.2f}")
                with col_stats2:
                    total_students = len(matched_students)
                    st.metric("Total Matched", total_students)
                with col_stats3:
                    top_dept = matched_students["department"].mode()[0] if not matched_students.empty else "N/A"
                    st.metric("Top Department", top_dept)
            else:
                st.info("Select a company to see matching students")
    
    def step6_interview_management(self):
        """Step 6: Interview Management"""
        st.info("Schedule and track interview progress for students")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📝 Schedule Interview")
            
            # Get data for dropdowns
            student_ids = []
            if not self.college_data["students"].empty:
                student_ids = self.college_data["students"]["id"].tolist()
            
            companies = []
            if not self.college_data["companies"].empty:
                companies = self.college_data["companies"]["name"].tolist()
            
            with st.form("schedule_interview_form"):
                student_id = st.selectbox(
                    "Select Student *",
                    options=student_ids if student_ids else ["S0001", "S0002", "S0003"]
                )
                company = st.selectbox(
                    "Company *",
                    options=companies if companies else ["Google", "Microsoft", "Amazon"]
                )
                interview_round = st.selectbox(
                    "Interview Round *",
                    options=["Aptitude Test", "Technical Round 1", "Technical Round 2", "HR Round", "Final Round"]
                )
                interview_date = st.date_input("Interview Date *", min_value=datetime.now().date())
                interview_time = st.time_input("Interview Time *")
                mode = st.radio("Mode *", ["Online", "Offline"])
                interviewer = st.text_input("Interviewer Name")
                
                submit = st.form_submit_button("Schedule Interview")
                
                if submit:
                    if student_id and company and interview_round:
                        # In a real app, you would save this to an 'interviews' table
                        st.success(f"✅ Interview scheduled for {student_id} with {company}")
                        if not st.session_state.demo_mode:
                            st.info("Note: Interview scheduling database integration would be implemented here")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Interview Schedule")
            
            # Display interviews
            if not self.college_data["interviews"].empty:
                interviews_df = self.college_data["interviews"].copy()
                interviews_df["datetime"] = pd.to_datetime(interviews_df["date"] + " " + interviews_df["time"])
                upcoming_interviews = interviews_df[interviews_df["datetime"] >= pd.Timestamp.now()]
                
                if not upcoming_interviews.empty:
                    display_cols = ["student_id", "student_name", "company", "round", "date", "time", "mode", "status"]
                    available_cols = [col for col in display_cols if col in upcoming_interviews.columns]
                    
                    st.dataframe(
                        upcoming_interviews[available_cols],
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.info("No upcoming interviews scheduled")
            else:
                st.info("No interview data available")
    
    def step7_placement_records(self):
        """Step 7: Placement Records Management"""
        st.info("Manage and track all placement offers and records")
        
        if self.college_data["placements"].empty:
            st.info("No placement records available")
            return
        
        # Overall placement statistics
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        with col_stats1:
            total_placements = len(self.college_data["placements"])
            st.metric("Total Placements", total_placements)
        with col_stats2:
            avg_package = self.college_data["placements"]["package"].mean() if not self.college_data["placements"].empty else 0
            st.metric("Avg Package (LPA)", f"{avg_package:.2f}")
        with col_stats3:
            unique_companies = self.college_data["placements"]["company"].nunique() if not self.college_data["placements"].empty else 0
            st.metric("Companies", unique_companies)
        with col_stats4:
            highest_package = self.college_data["placements"]["package"].max() if not self.college_data["placements"].empty else 0
            st.metric("Highest Package", f"{highest_package:.2f} LPA")
        
        # Placement records table
        st.subheader("📋 Placement Records")
        
        # Display table
        st.dataframe(
            self.college_data["placements"],
            use_container_width=True,
            height=400
        )
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.subheader("🏢 Placements by Company")
            
            if not self.college_data["placements"].empty:
                company_placements = self.college_data["placements"]["company"].value_counts().head(10)
                
                fig1 = px.bar(
                    x=company_placements.values,
                    y=company_placements.index,
                    orientation='h',
                    title="Top 10 Companies by Placements",
                    labels={"x": "Number of Placements", "y": "Company"}
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_viz2:
            st.subheader("📊 Package Distribution")
            
            if not self.college_data["placements"].empty:
                fig2 = px.histogram(
                    self.college_data["placements"],
                    x="package",
                    nbins=20,
                    title="Package Distribution",
                    labels={"package": "Package (LPA)", "count": "Number of Students"}
                )
                st.plotly_chart(fig2, use_container_width=True)
    
    def step8_performance_reports(self):
        """Step 8: Performance Reports & Analytics"""
        st.info("Generate comprehensive performance reports and analytics")
        
        # Report selection
        report_type = st.selectbox(
            "Select Report Type",
            options=[
                "📈 Annual Placement Report",
                "🏢 Company Performance Report",
                "🎓 Department Performance Report",
                "📊 Comprehensive Analytics Report"
            ]
        )
        
        # Generate report button
        if st.button("📊 Generate Report", type="primary"):
            st.success(f"Generating {report_type}...")
            
            # Report content based on selection
            if "Annual Placement Report" in report_type:
                self.generate_annual_report()
            elif "Company Performance Report" in report_type:
                self.generate_company_report()
            elif "Department Performance Report" in report_type:
                self.generate_department_report()
            else:
                self.generate_comprehensive_report()

     # Continue with other steps (3, 4, 5)...
    # (Your existing code for steps 3, 4, 5 remains the same)
    
    def display_progress_bar(self):
        """Display progress bar for current step"""
        progress = self.current_step / self.total_steps
        st.progress(progress)
        st.caption(f"Step {self.current_step} of {self.total_steps}")
    
    def display_college_summary(self):
        """Display college profile summary"""
        with st.expander("🏫 College Summary", expanded=False):
            profile = self.college_data["profile"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {profile['name']}")
                st.write(f"**Contact Email:** {profile['contact_email']}")
                st.write(f"**Contact Phone:** {profile['contact_phone']}")
                st.write(f"**Website:** {profile['website']}")
            
            with col2:
                st.write(f"**Placement Officer:** {profile['placement_officer']}")
                st.write(f"**Accreditation:** {profile['accreditation']}")
                st.write(f"**Established:** {profile['established_year']}")
            
            if profile['departments']:
                st.write(f"**Departments:** {', '.join(profile['departments'])}")
    
    def generate_annual_report(self):
        """Generate annual placement report"""
        st.subheader("📈 Annual Placement Report")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if not self.college_data["placements"].empty:
                total_placements = len(self.college_data["placements"])
                st.metric("Total Placements", total_placements)
            else:
                st.metric("Total Placements", "N/A")
        
        with col2:
            if not self.college_data["placements"].empty:
                avg_package = self.college_data["placements"]["package"].mean()
                st.metric("Average Package", f"{avg_package:.2f} LPA")
            else:
                st.metric("Average Package", "N/A")
        
        # Key insights
        st.subheader("📋 Key Insights")
        
        insights = [
            "✅ Strong placement performance in Computer Science department",
            "📈 Increasing average package year over year",
            "🏢 Good diversity in recruiting companies",
            "🎯 High placement rate for students with CGPA > 8.0",
            "🔧 Opportunities for improvement in core engineering placements"
        ]
        
        for insight in insights:
            st.write(f"- {insight}")
    
    def generate_company_report(self):
        """Generate company performance report"""
        st.subheader("🏢 Company Performance Report")
        
        if self.college_data["companies"].empty:
            st.info("No company data available")
            return
        
        # Company performance metrics
        company_metrics = []
        for _, company in self.college_data["companies"].iterrows():
            company_metrics.append({
                "Company": company["name"],
                "Status": company.get("status", "Active"),
                "Total Hires": company.get("total_hires", 0),
                "Avg Package": company.get("avg_package", "N/A")
            })
        
        metrics_df = pd.DataFrame(company_metrics)
        st.dataframe(metrics_df.sort_values("Total Hires", ascending=False), use_container_width=True)
    
    def generate_department_report(self):
        """Generate department performance report"""
        st.subheader("🎓 Department Performance Report")
        
        if self.college_data["students"].empty:
            st.info("No student data available")
            return
        
        # Department-wise analysis
        dept_stats = []
        for dept in self.college_data["students"]["department"].unique():
            dept_students = self.college_data["students"][self.college_data["students"]["department"] == dept]
            
            dept_stats.append({
                "Department": dept,
                "Total Students": len(dept_students),
                "Avg CGPA": dept_students["cgpa"].mean() if not dept_students.empty else 0
            })
        
        stats_df = pd.DataFrame(dept_stats)
        st.dataframe(stats_df.sort_values("Avg CGPA", ascending=False), use_container_width=True)
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analytics report"""
        st.subheader("📊 Comprehensive Analytics Report")
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        
        summary_cols = st.columns(3)
        with summary_cols[0]:
            if not self.college_data["students"].empty:
                total_students = len(self.college_data["students"])
                placed = len(self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"])
                rate = (placed / total_students * 100) if total_students > 0 else 0
                st.metric("Placement Rate", f"{rate:.1f}%")
        
        # Recommendations
        st.subheader("🎯 Recommendations")
        
        recommendations = [
            "Increase industry-academia collaboration programs",
            "Enhance soft skills and interview preparation",
            "Expand recruitment to more startups and product companies",
            "Implement better tracking of student skill development",
            "Increase international placement opportunities"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    
    def display_workflow_navigation(self, current_step):
        """Display navigation buttons for workflow"""
        st.divider()
        
        # Create a container for navigation buttons
        nav_container = st.container()
        
        with nav_container:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if current_step > 1:
                    if st.button("⬅️ Previous Step", 
                                key=f"college_prev_{current_step}",
                                help="Go to previous step",
                                use_container_width=True):
                        # Update session state and rerun
                        st.session_state.current_step_college = current_step - 1
                        st.rerun()
            
            with col2:
                # Database status
                if not st.session_state.demo_mode and st.session_state.get('db_manager') and st.session_state.db_manager.is_connected:
                    st.caption("💾 Connected to Live Database")
                else:
                    st.caption("⚠️ Demo Mode - Data not saved")
            
            with col3:
                if current_step < 8:
                    if st.button("Next Step ➡️", 
                                key=f"college_next_{current_step}",
                                help="Proceed to next step",
                                use_container_width=True,
                                type="primary"):
                        # Update session state and rerun
                        st.session_state.current_step_college = current_step + 1
                        st.rerun()
                else:
                    if st.button("🏁 Complete Workflow", 
                                key="college_complete",
                                help="Finish college workflow",
                                use_container_width=True,
                                type="primary"):
                        st.success("🎉 College workflow completed successfully!")
                        # Option to reset to step 1
                        if st.button("🔄 Start Over", key="college_reset"):
                            st.session_state.current_step_college = 1
                            st.rerun()
