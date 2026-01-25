import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from database.db_manager import db_manager

class CollegeFlow:
    def __init__(self):
        # Initialize session state for step management
        if 'current_step_college' not in st.session_state:
            st.session_state.current_step_college = 1
        
        self.current_step = st.session_state.current_step_college
        self.db_manager = None
        self.demo_mode = True
        
        # Initialize college data
        self.college_data = self.initialize_college_data()
        
    def initialize_college_data(self):
        """Initialize college data with sample data"""
        return {
            "college_id": 1,
            "college_name": "ABC Engineering College",
            "profile": {
                "name": "ABC Engineering College",
                "address": "123 College Road, City, State 123456",
                "website": "https://abcengg.edu",
                "contact_email": "placement@abcengg.edu",
                "contact_phone": "+91 9876543210",
                "placement_officer": "Dr. Placement Officer",
                "departments": ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Information Technology"],
                "accreditation": "NAAC A",
                "established_year": "2000"
            },
            "students": self.generate_sample_students(),
            "companies": self.generate_sample_companies(),
            "drives": self.generate_sample_drives(),
            "placements": self.generate_sample_placements(),
            "interviews": self.generate_sample_interviews(),
            "recruiters": [],
            "reports": []
        }
    
    def generate_sample_students(self):
        """Generate sample student data"""
        np.random.seed(42)
        n_students = 150
        
        departments = ["Computer Science", "Electrical Engineering", 
                      "Mechanical Engineering", "Civil Engineering", "Information Technology"]
        years = [2022, 2023, 2024]
        
        data = []
        for i in range(n_students):
            dept = departments[i % len(departments)]
            grad_year = years[i % len(years)]
            
            student = {
                "student_id": f"S{i+1:04d}",
                "name": f"Student {i+1}",
                "department": dept,
                "semester": np.random.randint(3, 9),
                "cgpa": round(6.5 + np.random.random() * 3, 2),
                "backlogs": np.random.randint(0, 4),
                "graduation_year": grad_year,
                "placement_status": "Not Placed" if i < 100 else "Placed",
                "company": None if i < 100 else ["Google", "Microsoft", "Amazon", "TCS", "Infosys"][i % 5],
                "package": None if i < 100 else round(8 + np.random.random() * 12, 2),
                "email": f"student{i+1}@college.edu",
                "phone": f"+91 98765{np.random.randint(10000, 99999)}"
            }
            
            # Add some interns
            if 50 <= i < 70:
                student["placement_status"] = "Intern"
                student["company"] = ["TechCorp", "StartupX", "InnovateLabs"][i % 3]
                student["package"] = round(0.5 + np.random.random() * 0.5, 2)
            
            data.append(student)
        
        return pd.DataFrame(data)
    
    def generate_sample_companies(self):
        """Generate sample company data"""
        companies = [
            {
                "company_id": "C001",
                "name": "Google",
                "industry": "Technology",
                "website": "https://google.com",
                "contact_person": "John Doe",
                "contact_email": "campus@google.com",
                "contact_phone": "+1-650-253-0000",
                "recruitment_status": "Active",
                "visits_this_year": 3,
                "total_hires": 25,
                "avg_package": 22.5
            },
            {
                "company_id": "C002",
                "name": "Microsoft",
                "industry": "Software",
                "website": "https://microsoft.com",
                "contact_person": "Jane Smith",
                "contact_email": "university@microsoft.com",
                "contact_phone": "+1-425-882-8080",
                "recruitment_status": "Active",
                "visits_this_year": 2,
                "total_hires": 18,
                "avg_package": 20.0
            },
            {
                "company_id": "C003",
                "name": "Amazon",
                "industry": "E-commerce",
                "website": "https://amazon.com",
                "contact_person": "Bob Johnson",
                "contact_email": "campus@amazon.com",
                "contact_phone": "+1-206-266-1000",
                "recruitment_status": "Active",
                "visits_this_year": 2,
                "total_hires": 15,
                "avg_package": 18.5
            }
        ]
        return pd.DataFrame(companies)
    
    def generate_sample_drives(self):
        """Generate sample campus drives"""
        drives = []
        companies = ["Google", "Microsoft", "Amazon"]
        
        for i in range(10):
            drive_date = datetime.now() + timedelta(days=np.random.randint(10, 90))
            
            drive = {
                "drive_id": f"D{i+1:03d}",
                "company": companies[i % len(companies)],
                "date": drive_date.strftime("%Y-%m-%d"),
                "mode": np.random.choice(["Online", "Offline", "Hybrid"]),
                "venue": "Main Campus Auditorium" if i % 2 == 0 else "Virtual",
                "coordinator": f"Coordinator {i+1}",
                "status": "Scheduled" if i < 7 else "Completed",
                "registered": np.random.randint(50, 200),
                "selected": np.random.randint(5, 25) if i >= 7 else 0,
                "job_roles": "SDE, Data Scientist" if i % 2 == 0 else "PM, Business Analyst"
            }
            drives.append(drive)
        
        return pd.DataFrame(drives)
    
    def generate_sample_placements(self):
        """Generate sample placement records"""
        placements = []
        companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys"]
        
        for i in range(50):
            placement = {
                "placement_id": f"P{i+1:04d}",
                "student_id": f"S{np.random.randint(1000, 1150):04d}",
                "student_name": f"Student {i+151}",
                "department": np.random.choice(["Computer Science", "Electrical", "Mechanical", "Civil", "IT"]),
                "company": companies[i % len(companies)],
                "job_role": np.random.choice(["Software Engineer", "Data Scientist", "Product Manager", 
                                            "Business Analyst", "DevOps Engineer"]),
                "package": round(8 + np.random.random() * 22, 2),
                "placement_date": (datetime.now() - timedelta(days=np.random.randint(1, 365))).strftime("%Y-%m-%d"),
                "status": np.random.choice(["Offer Accepted", "Joined", "Completed Internship"])
            }
            placements.append(placement)
        
        return pd.DataFrame(placements)
    
    def generate_sample_interviews(self):
        """Generate sample interview records"""
        interviews = []
        rounds = ["Aptitude Test", "Technical Round 1", "Technical Round 2", "HR Round", "Managerial Round"]
        
        for i in range(30):
            interview_date = datetime.now() + timedelta(days=np.random.randint(1, 30))
            
            interview = {
                "interview_id": f"I{i+1:04d}",
                "student_id": f"S{np.random.randint(1000, 1100):04d}",
                "student_name": f"Student {np.random.randint(1, 150)}",
                "company": np.random.choice(["Google", "Microsoft", "Amazon"]),
                "round": rounds[i % len(rounds)],
                "date": interview_date.strftime("%Y-%m-%d"),
                "time": f"{np.random.randint(9, 17):02d}:00",
                "mode": np.random.choice(["Online", "Offline"]),
                "interviewer": f"Interviewer {np.random.randint(1, 20)}",
                "status": np.random.choice(["Scheduled", "Completed", "Cancelled"]),
                "result": "Pending" if i < 20 else np.random.choice(["Selected", "Rejected", "On Hold"])
            }
            interviews.append(interview)
        
        return pd.DataFrame(interviews)
    
    def set_database_manager(self, db_manager, demo_mode=False):
        """Set the database manager for this flow"""
        self.db_manager = db_manager
        self.demo_mode = demo_mode
        
        # If we have a db manager, try to load data
        if not self.demo_mode and self.db_manager:
            self.load_from_database()
    
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
        except Exception as e:
            st.error(f"Error loading from database: {e}")
    
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
        """Display complete college admin workflow"""
        # Update current step from session state
        self.current_step = st.session_state.current_step_college
        
        # Display step header
        step_names = {
            1: "🏫 College Profile Setup",
            2: "👨‍🎓 Student Management",
            3: "🏢 Company Management",
            4: "📅 Drive Scheduling",
            5: "🎯 Student-Company Matching",
            6: "📝 Interview Management",
            7: "✅ Placement Records",
            8: "📊 Reports & Analytics"
        }
        
        # Create header with progress
        st.header("🏫 College Placement Management System")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Step {self.current_step}: {step_names[self.current_step]}")
        with col2:
            progress = self.current_step / 8
            st.progress(progress)
            st.caption(f"Step {self.current_step} of 8")
        
        # Display appropriate step
        if self.current_step == 1:
            self.step1_college_profile()
        elif self.current_step == 2:
            self.step2_student_management()
        elif self.current_step == 3:
            self.step3_company_registration()
        elif self.current_step == 4:
            self.step4_drive_scheduling()
        elif self.current_step == 5:
            self.step5_student_company_matching()
        elif self.current_step == 6:
            self.step6_interview_management()
        elif self.current_step == 7:
            self.step7_placement_records()
        elif self.current_step == 8:
            self.step8_performance_reports()
        
        # Navigation
        self.display_workflow_navigation(self.current_step)
    
    def step1_college_profile(self):
        """Step 1: College Profile Setup"""
        st.info("Setup and manage your college profile information")
        
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
        st.info("Manage and view all student records in the college")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("📋 Student Management")
            
            # Filters
            st.write("### Filters")
            department_filter = st.multiselect(
                "Select Department",
                options=self.college_data["students"]["department"].unique(),
                default=[]
            )
            
            placement_filter = st.selectbox(
                "Placement Status",
                options=["All", "Placed", "Not Placed", "Intern"]
            )
            
            cgpa_filter = st.slider(
                "Minimum CGPA",
                min_value=0.0,
                max_value=10.0,
                value=0.0,
                step=0.5
            )
            
            # Add new student form
            st.write("### Add New Student")
            with st.form("add_student_form"):
                new_name = st.text_input("Name")
                new_dept = st.selectbox("Department", 
                                      options=self.college_data["profile"]["departments"])
                new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5)
                new_year = st.selectbox("Graduation Year", options=[2023, 2024, 2025])
                new_email = st.text_input("Email")
                
                if st.form_submit_button("Add Student"):
                    if new_name and new_dept and new_email:
                        new_student_id = f"S{len(self.college_data['students']) + 1001:04d}"
                        new_student = {
                            "student_id": new_student_id,
                            "name": new_name,
                            "department": new_dept,
                            "cgpa": new_cgpa,
                            "graduation_year": new_year,
                            "email": new_email,
                            "placement_status": "Not Placed"
                        }
                        
                        # Add to DataFrame
                        self.college_data["students"] = pd.concat([
                            self.college_data["students"],
                            pd.DataFrame([new_student])
                        ], ignore_index=True)
                        
                        st.success(f"Added student: {new_name} (ID: {new_student_id})")
                        st.rerun()
                    else:
                        st.error("Please fill required fields")
        
        with col2:
            st.subheader("👥 Student Database")
            
            # Apply filters
            filtered_students = self.college_data["students"].copy()
            
            if department_filter:
                filtered_students = filtered_students[filtered_students["department"].isin(department_filter)]
            
            if placement_filter != "All":
                filtered_students = filtered_students[filtered_students["placement_status"] == placement_filter]
            
            filtered_students = filtered_students[filtered_students["cgpa"] >= cgpa_filter]
            
            # Display statistics
            col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
            with col_stats1:
                st.metric("Total Students", len(filtered_students))
            with col_stats2:
                placed_count = len(filtered_students[filtered_students["placement_status"] == "Placed"])
                st.metric("Placed", placed_count)
            with col_stats3:
                avg_cgpa = filtered_students["cgpa"].mean()
                st.metric("Avg CGPA", f"{avg_cgpa:.2f}")
            with col_stats4:
                internships = len(filtered_students[filtered_students["placement_status"] == "Intern"])
                st.metric("Internships", internships)
            
            # Display data table
            st.dataframe(
                filtered_students[
                    ["student_id", "name", "department", "cgpa", "placement_status", "company", "package"]
                ].sort_values("cgpa", ascending=False),
                use_container_width=True,
                height=400
            )
    
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
                            "company_id": f"C{len(self.college_data['companies']) + 1:03d}",
                            "name": company_name,
                            "industry": industry,
                            "website": website,
                            "contact_person": contact_person,
                            "contact_email": contact_email,
                            "contact_phone": contact_phone,
                            "min_cgpa": float(min_cgpa),
                            "max_backlogs": max_backlogs,
                            "recruitment_status": "Active",
                            "visits_this_year": 0,
                            "total_hires": 0,
                            "avg_package": 0
                        }
                        
                        # Add to DataFrame
                        self.college_data["companies"] = pd.concat([
                            self.college_data["companies"],
                            pd.DataFrame([company_data])
                        ], ignore_index=True)
                        
                        st.success(f"✅ Successfully registered {company_name}")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Registered Companies")
            
            if self.college_data["companies"].empty:
                st.info("No companies registered yet")
                return
            
            # Display companies table
            display_cols = ["name", "industry", "contact_person", "contact_email", "contact_phone", "recruitment_status", "total_hires", "avg_package"]
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
                        drive_id = f"D{len(self.college_data['drives']) + 1:03d}"
                        new_drive = {
                            "drive_id": drive_id,
                            "company": company,
                            "date": drive_date.strftime("%Y-%m-%d"),
                            "mode": mode,
                            "venue": venue,
                            "coordinator": coordinator,
                            "status": "Scheduled",
                            "registered": 0,
                            "selected": 0,
                            "job_roles": job_roles
                        }
                        
                        # Add to DataFrame
                        self.college_data["drives"] = pd.concat([
                            self.college_data["drives"],
                            pd.DataFrame([new_drive])
                        ], ignore_index=True)
                        
                        st.success(f"✅ Drive scheduled for {company} on {drive_date}")
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
                
                matched_students = matched_students[matched_students["placement_status"] == "Not Placed"]
                
                st.metric("Matching Students", len(matched_students))
        
        with col2:
            st.subheader("👥 Matched Students")
            
            if 'matched_students' in locals() and not matched_students.empty:
                # Display matched students
                display_cols = ["student_id", "name", "department", "cgpa", "backlogs", "email"]
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
                student_ids = self.college_data["students"]["student_id"].tolist()
            
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
                        interview_id = f"I{len(self.college_data['interviews']) + 1:04d}"
                        new_interview = {
                            "interview_id": interview_id,
                            "student_id": student_id,
                            "student_name": self.get_student_name(student_id),
                            "company": company,
                            "round": interview_round,
                            "date": interview_date.strftime("%Y-%m-%d"),
                            "time": interview_time.strftime("%H:%M"),
                            "mode": mode,
                            "interviewer": interviewer,
                            "status": "Scheduled",
                            "result": "Pending"
                        }
                        
                        # Add to DataFrame
                        self.college_data["interviews"] = pd.concat([
                            self.college_data["interviews"],
                            pd.DataFrame([new_interview])
                        ], ignore_index=True)
                        
                        st.success(f"✅ Interview scheduled for {student_id} with {company}")
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
    
    def get_student_name(self, student_id):
        """Get student name by ID"""
        student = self.college_data["students"][self.college_data["students"]["student_id"] == student_id]
        return student["name"].iloc[0] if not student.empty else "Unknown"
    
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
        col1, col2, col_stats3, col_stats4 = st.columns(4)
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
        
        with col_stats3:
            st.metric("Placement Rate", "82%")
        
        with col_stats4:
            st.metric("Highest Package", "32.5 LPA")
        
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
                "Status": company.get("recruitment_status", "Active"),
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
        
        with summary_cols[1]:
            if not self.college_data["placements"].empty:
                avg_package = self.college_data["placements"]["package"].mean()
                st.metric("Avg Package", f"{avg_package:.2f} LPA")
            else:
                st.metric("Avg Package", "N/A")
        
        with summary_cols[2]:
            if not self.college_data["companies"].empty:
                active_companies = len(self.college_data["companies"])
                st.metric("Active Companies", active_companies)
        
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
                # Show step summary
                st.info(f"**Step {current_step} of 8** - Complete this step before proceeding")
            
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
