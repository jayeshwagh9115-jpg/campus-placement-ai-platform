import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from typing import List, Dict, Optional

class CollegeFlow:
    def __init__(self):
        self.college_data = self.initialize_college_data()
        # Initialize current_step from session state or default to 1
        self.current_step = st.session_state.get('current_step_college', 1)
    
    def initialize_college_data(self):
        """Initialize college data"""
        return {
            "college_name": "ABC Engineering College",
            "college_id": None,
            "students": pd.DataFrame(),
            "companies": pd.DataFrame(),
            "drives": pd.DataFrame(),
            "placements": pd.DataFrame(),
            "interviews": pd.DataFrame()
        }
    
    # ==================== DATABASE METHODS ====================
    
    def get_from_database(self, data_type: str, college_id: str = None) -> pd.DataFrame:
        """Get data from database"""
        if st.session_state.demo_mode:
            return pd.DataFrame()  # Will use sample data in demo mode
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return pd.DataFrame()
        
        try:
            if data_type == 'students':
                if college_id:
                    data = db.get_students(college_id=college_id)
                else:
                    data = db.get_students()
                return pd.DataFrame(data) if data else pd.DataFrame()
            
            elif data_type == 'companies':
                data = db.get_companies()
                return pd.DataFrame(data) if data else pd.DataFrame()
            
            elif data_type == 'jobs':
                data = db.get_jobs()
                return pd.DataFrame(data) if data else pd.DataFrame()
            
            elif data_type == 'applications':
                data = db.get_applications()
                return pd.DataFrame(data) if data else pd.DataFrame()
            
            elif data_type == 'colleges':
                data = db.get_colleges()
                return pd.DataFrame(data) if data else pd.DataFrame()
            
        except Exception as e:
            st.error(f"Database error fetching {data_type}: {e}")
        
        return pd.DataFrame()
    
    def save_to_database(self, data_type: str, data: Dict) -> bool:
        """Save data to database"""
        if st.session_state.demo_mode:
            return True  # Return success in demo mode
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return False
        
        try:
            if data_type == 'student':
                result = db.create_student(data)
            elif data_type == 'company':
                result = db.insert('companies', data)
            elif data_type == 'college':
                result = db.create_college(data)
            elif data_type == 'job':
                result = db.create_job(data)
            elif data_type == 'application':
                result = db.create_application(data)
            else:
                return False
            
            return result is not None
            
        except Exception as e:
            st.error(f"Database error saving {data_type}: {e}")
            return False
    
    def get_current_college_id(self) -> Optional[str]:
        """Get current college ID from session or database"""
        # Try to get from session state first
        college_id = st.session_state.get('current_college_id')
        
        if college_id:
            return college_id
        
        # If not in session, try to get from database using college email
        if 'college_email' in st.session_state:
            db = st.session_state.get('db_manager')
            if db and db.is_connected:
                colleges = db.get_colleges()
                college = next((c for c in colleges if c.get('email') == st.session_state.college_email), None)
                if college:
                    st.session_state.current_college_id = college.get('id')
                    return college.get('id')
        
        return None
    
    def load_college_data(self):
        """Load all college-related data from database"""
        if st.session_state.demo_mode:
            # Load sample data for demo mode
            self.load_sample_data()
            return
        
        college_id = self.get_current_college_id()
        
        if not college_id:
            st.warning("College ID not found. Running in demo mode.")
            self.load_sample_data()
            return
        
        # Load real data from database
        with st.spinner("Loading college data..."):
            # Students
            students_data = self.get_from_database('students', college_id)
            if not students_data.empty:
                self.college_data["students"] = students_data
            else:
                st.info("No students found in database. Using sample data.")
                self.college_data["students"] = self.generate_sample_students()
            
            # Companies
            companies_data = self.get_from_database('companies')
            if not companies_data.empty:
                self.college_data["companies"] = companies_data
            else:
                self.college_data["companies"] = self.generate_sample_companies()
            
            # Load other data (you can add database methods for these)
            self.college_data["drives"] = self.generate_sample_drives()
            self.college_data["placements"] = self.generate_sample_placements()
            self.college_data["interviews"] = self.generate_sample_interviews()
    
    def load_sample_data(self):
        """Load sample data for demo mode"""
        self.college_data["students"] = self.generate_sample_students()
        self.college_data["companies"] = self.generate_sample_companies()
        self.college_data["drives"] = self.generate_sample_drives()
        self.college_data["placements"] = self.generate_sample_placements()
        self.college_data["interviews"] = self.generate_sample_interviews()
    
    def generate_sample_students(self):
        """Generate sample student data for demo mode"""
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
                "id": f"S{i+1:04d}",
                "full_name": f"Student {i+1}",
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
        """Generate sample company data for demo mode"""
        companies = [
            {
                "id": "C001",
                "name": "Google",
                "industry": "Technology",
                "website": "https://google.com",
                "contact_person": "John Doe",
                "email": "campus@google.com",
                "phone": "+1-650-253-0000",
                "status": "Active",
                "total_hires": 25,
                "avg_package": 22.5
            },
            {
                "id": "C002",
                "name": "Microsoft",
                "industry": "Software",
                "website": "https://microsoft.com",
                "contact_person": "Jane Smith",
                "email": "university@microsoft.com",
                "phone": "+1-425-882-8080",
                "status": "Active",
                "total_hires": 18,
                "avg_package": 20.0
            },
            {
                "id": "C003",
                "name": "Amazon",
                "industry": "E-commerce",
                "website": "https://amazon.com",
                "contact_person": "Bob Johnson",
                "email": "campus@amazon.com",
                "phone": "+1-206-266-1000",
                "status": "Active",
                "total_hires": 15,
                "avg_package": 18.5
            },
            {
                "id": "C004",
                "name": "TCS",
                "industry": "IT Services",
                "website": "https://tcs.com",
                "contact_person": "Alice Brown",
                "email": "campus@tcs.com",
                "phone": "+91-22-6778-9999",
                "status": "Active",
                "total_hires": 45,
                "avg_package": 8.5
            },
            {
                "id": "C005",
                "name": "Infosys",
                "industry": "IT Services",
                "website": "https://infosys.com",
                "contact_person": "Charlie Wilson",
                "email": "campus@infosys.com",
                "phone": "+91-80-2852-0261",
                "status": "Active",
                "total_hires": 38,
                "avg_package": 8.0
            }
        ]
        return pd.DataFrame(companies)
    
    def generate_sample_drives(self):
        """Generate sample campus drives for demo mode"""
        drives = []
        companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys"]
        
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
        """Generate sample placement records for demo mode"""
        placements = []
        companies = ["Google", "Microsoft", "Amazon", "TCS", "Infosys", 
                    "Adobe", "Intel", "Oracle", "Cisco", "IBM"]
        
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
        """Generate sample interview records for demo mode"""
        interviews = []
        rounds = ["Aptitude Test", "Technical Round 1", "Technical Round 2", "HR Round", "Managerial Round"]
        
        for i in range(30):
            interview_date = datetime.now() + timedelta(days=np.random.randint(1, 30))
            
            interview = {
                "interview_id": f"I{i+1:04d}",
                "student_id": f"S{np.random.randint(1000, 1100):04d}",
                "student_name": f"Student {np.random.randint(1, 150)}",
                "company": np.random.choice(["Google", "Microsoft", "Amazon", "TCS", "Infosys"]),
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
    
    def display(self):
        """Display complete college admin workflow"""
        st.header("🏫 College Placement Management System")
        
        # Get current step from session state
        current_step = st.session_state.get('current_step_college', 1)
        self.current_step = current_step
        
        # Display step header
        step_names = {
            1: "👨‍🎓 Student Database",
            2: "📊 Analytics Dashboard",
            3: "🏢 Company Registration",
            4: "📅 Drive Scheduling",
            5: "🎯 Student-Company Matching",
            6: "📝 Interview Management",
            7: "✅ Placement Records",
            8: "📈 Performance Reports"
        }
        
        # Create header with progress
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Step {current_step}: {step_names[current_step]}")
        with col2:
            progress = current_step / 8
            st.progress(progress)
            st.caption(f"Step {current_step} of 8")
        
        # Database status indicator
        if not st.session_state.demo_mode and st.session_state.get('db_manager') and st.session_state.db_manager.is_connected:
            st.success("✅ Connected to Live Database")
            # Load data from database
            self.load_college_data()
        else:
            st.warning("⚠️ Running in Demo Mode")
            # Load sample data for demo
            self.load_sample_data()
        
        # Display appropriate step
        if current_step == 1:
            self.step1_student_database()
        elif current_step == 2:
            self.step2_analytics_dashboard()
        elif current_step == 3:
            self.step3_company_registration()
        elif current_step == 4:
            self.step4_drive_scheduling()
        elif current_step == 5:
            self.step5_student_company_matching()
        elif current_step == 6:
            self.step6_interview_management()
        elif current_step == 7:
            self.step7_placement_records()
        elif current_step == 8:
            self.step8_performance_reports()
        
        # Navigation - Moved to bottom and made more prominent
        self.display_workflow_navigation(current_step)
    
    def step1_student_database(self):
        """Step 1: Student Database Management"""
        st.info("Manage and view all student records in the college")
        
        # Database info
        if not st.session_state.demo_mode:
            college_id = self.get_current_college_id()
            if college_id:
                st.info(f"📋 College ID: {college_id}")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("📋 Student Management")
            
            # Filters
            st.write("### Filters")
            department_filter = st.multiselect(
                "Select Department",
                options=self.college_data["students"]["department"].unique() if not self.college_data["students"].empty else [],
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
                new_name = st.text_input("Full Name*")
                new_email = st.text_input("Email*")
                new_roll = st.text_input("Roll Number*")
                new_dept = st.selectbox("Department*", 
                                      options=self.college_data["students"]["department"].unique() if not self.college_data["students"].empty else ["Computer Science"])
                new_cgpa = st.number_input("CGPA*", min_value=0.0, max_value=10.0, value=7.5)
                new_year = st.selectbox("Graduation Year*", options=[2023, 2024, 2025])
                
                submit = st.form_submit_button("Add Student")
                
                if submit:
                    if new_name and new_email and new_roll and new_dept:
                        student_data = {
                            "full_name": new_name,
                            "email": new_email,
                            "roll_number": new_roll,
                            "department": new_dept,
                            "cgpa": float(new_cgpa),
                            "graduation_year": new_year,
                            "college_id": self.get_current_college_id() if not st.session_state.demo_mode else None,
                            "created_at": datetime.now().isoformat()
                        }
                        
                        success = self.save_to_database('student', student_data)
                        
                        if success or st.session_state.demo_mode:
                            st.success(f"✅ Added student: {new_name}")
                            if not st.session_state.demo_mode:
                                st.success("✅ Student saved to database!")
                                # Refresh data
                                self.load_college_data()
                        else:
                            st.error("❌ Failed to save student to database")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("👥 Student Database")
            
            if self.college_data["students"].empty:
                st.info("No student data available")
                return
            
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
                avg_cgpa = filtered_students["cgpa"].mean() if not filtered_students.empty else 0
                st.metric("Avg CGPA", f"{avg_cgpa:.2f}")
            with col_stats4:
                internships = len(filtered_students[filtered_students["placement_status"] == "Intern"])
                st.metric("Internships", internships)
            
            # Display data table
            display_cols = ["id", "full_name", "department", "cgpa", "placement_status", "company", "package"]
            # Use available columns
            available_cols = [col for col in display_cols if col in filtered_students.columns]
            
            st.dataframe(
                filtered_students[available_cols].sort_values("cgpa", ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Export option
            if st.button("📥 Export Student Data"):
                csv = filtered_students.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="student_database.csv",
                    mime="text/csv"
                )
    
    def step2_analytics_dashboard(self):
        """Step 2: Analytics Dashboard"""
        st.info("Comprehensive analytics and insights on placement performance")
        
        if self.college_data["students"].empty:
            st.warning("No student data available for analytics")
            return
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_students = len(self.college_data["students"])
            st.metric("Total Students", total_students)
        with col2:
            placed_students = len(self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"])
            placement_rate = (placed_students / total_students) * 100 if total_students > 0 else 0
            st.metric("Placement Rate", f"{placement_rate:.1f}%")
        with col3:
            placed_df = self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"]
            avg_package = placed_df["package"].mean() if not placed_df.empty else 0
            st.metric("Avg Package (LPA)", f"{avg_package:.2f}" if not pd.isna(avg_package) else "N/A")
        with col4:
            active_companies = len(self.college_data["companies"])
            st.metric("Active Companies", active_companies)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📈 Placement by Department")
            
            # Department-wise placement data
            if not self.college_data["students"].empty:
                dept_data = self.college_data["students"].groupby("department").agg({
                    "id": "count",
                    "placement_status": lambda x: (x == "Placed").sum()
                }).reset_index()
                dept_data["placement_rate"] = (dept_data["placement_status"] / dept_data["id"]) * 100
                
                fig1 = px.bar(
                    dept_data,
                    x="department",
                    y="placement_rate",
                    color="department",
                    title="Placement Rate by Department",
                    labels={"department": "Department", "placement_rate": "Placement Rate (%)"}
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col_chart2:
            st.subheader("🏢 Top Hiring Companies")
            
            # Company-wise hiring data
            if not self.college_data["students"].empty:
                company_counts = self.college_data["students"]["company"].value_counts().head(10)
                
                if not company_counts.empty:
                    fig2 = px.pie(
                        values=company_counts.values,
                        names=company_counts.index,
                        title="Top 10 Hiring Companies",
                        hole=0.4
                    )
                    st.plotly_chart(fig2, use_container_width=True)
                else:
                    st.info("No company hiring data available")
        
        # CGPA Distribution
        st.subheader("📊 CGPA Distribution")
        if not self.college_data["students"].empty:
            fig3 = px.histogram(
                self.college_data["students"],
                x="cgpa",
                nbins=20,
                title="CGPA Distribution of Students",
                labels={"cgpa": "CGPA", "count": "Number of Students"}
            )
            st.plotly_chart(fig3, use_container_width=True)
    
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
