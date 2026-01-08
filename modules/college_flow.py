import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from database.db_manager import db_manager

class CollegeFlow:
    def __init__(self):
        self.college_data = self.initialize_college_data()
        # Initialize current_step from session state or default to 1
        self.current_step = st.session_state.get('current_step_college', 1)
    
    def initialize_college_data(self):
        """Initialize college data"""
        return {
            "college_id": 1,  # Default college ID
            "college_name": "ABC Engineering College",
            "students": self.generate_sample_students(),
            "companies": self.generate_sample_companies(),
            "drives": self.generate_sample_drives(),
            "placements": self.generate_sample_placements(),
            "interviews": self.generate_sample_interviews()
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
            },
            {
                "company_id": "C004",
                "name": "TCS",
                "industry": "IT Services",
                "website": "https://tcs.com",
                "contact_person": "Alice Brown",
                "contact_email": "campus@tcs.com",
                "contact_phone": "+91-22-6778-9999",
                "recruitment_status": "Active",
                "visits_this_year": 4,
                "total_hires": 45,
                "avg_package": 8.5
            },
            {
                "company_id": "C005",
                "name": "Infosys",
                "industry": "IT Services",
                "website": "https://infosys.com",
                "contact_person": "Charlie Wilson",
                "contact_email": "campus@infosys.com",
                "contact_phone": "+91-80-2852-0261",
                "recruitment_status": "Active",
                "visits_this_year": 3,
                "total_hires": 38,
                "avg_package": 8.0
            }
        ]
        return pd.DataFrame(companies)
    
    def generate_sample_drives(self):
        """Generate sample campus drives"""
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
        """Generate sample placement records"""
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
        """Generate sample interview records"""
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
                                      options=self.college_data["students"]["department"].unique())
                new_cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5)
                new_year = st.selectbox("Graduation Year", options=[2023, 2024, 2025])
                
                if st.form_submit_button("Add Student"):
                    # Add student logic here
                    st.success(f"Added student: {new_name}")
        
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
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_students = len(self.college_data["students"])
            st.metric("Total Students", total_students)
        with col2:
            placed_students = len(self.college_data["students"][self.college_data["students"]["placement_status"] == "Placed"])
            placement_rate = (placed_students / total_students) * 100
            st.metric("Placement Rate", f"{placement_rate:.1f}%")
        with col3:
            avg_package = self.college_data["students"]["package"].mean()
            st.metric("Avg Package (LPA)", f"{avg_package:.2f}" if not pd.isna(avg_package) else "N/A")
        with col4:
            active_companies = len(self.college_data["companies"])
            st.metric("Active Companies", active_companies)
        
        # Charts
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.subheader("📈 Placement by Department")
            
            # Department-wise placement data
            dept_data = self.college_data["students"].groupby("department").agg({
                "student_id": "count",
                "placement_status": lambda x: (x == "Placed").sum()
            }).reset_index()
            dept_data["placement_rate"] = (dept_data["placement_status"] / dept_data["student_id"]) * 100
            
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
            company_counts = self.college_data["students"]["company"].value_counts().head(10)
            
            fig2 = px.pie(
                values=company_counts.values,
                names=company_counts.index,
                title="Top 10 Hiring Companies",
                hole=0.4
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # CGPA Distribution
        st.subheader("📊 CGPA Distribution")
        fig3 = px.histogram(
            self.college_data["students"],
            x="cgpa",
            nbins=20,
            title="CGPA Distribution of Students",
            labels={"cgpa": "CGPA", "count": "Number of Students"}
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Year-wise Trends
        st.subheader("📅 Year-wise Placement Trends")
        
        # Create sample trend data
        years = [2020, 2021, 2022, 2023]
        trend_data = pd.DataFrame({
            "Year": years,
            "Placement Rate": [65, 72, 78, 82],
            "Avg Package": [12.5, 14.2, 16.8, 18.5],
            "Total Offers": [120, 145, 165, 190]
        })
        
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=trend_data["Year"],
            y=trend_data["Placement Rate"],
            mode="lines+markers",
            name="Placement Rate (%)",
            yaxis="y"
        ))
        fig4.add_trace(go.Bar(
            x=trend_data["Year"],
            y=trend_data["Total Offers"],
            name="Total Offers",
            yaxis="y2"
        ))
        
        fig4.update_layout(
            title="Placement Trends Over Years",
            xaxis=dict(title="Year"),
            yaxis=dict(title="Placement Rate (%)", side="left"),
            yaxis2=dict(title="Total Offers", side="right", overlaying="y"),
            legend=dict(x=0.1, y=1.1, orientation="h")
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
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
                preferred_departments = st.multiselect(
                    "Preferred Departments",
                    options=self.college_data["students"]["department"].unique(),
                    default=self.college_data["students"]["department"].unique()
                )
                
                submit = st.form_submit_button("Register Company")
                
                if submit:
                    if company_name and contact_person and contact_email:
                        # Add company logic here
                        st.success(f"Successfully registered {company_name}")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Registered Companies")
            
            # Display companies table
            st.dataframe(
                self.college_data["companies"],
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
                total_hires = self.college_data["companies"]["total_hires"].sum()
                st.metric("Total Hires", total_hires)
            with col_stats3:
                avg_package = self.college_data["companies"]["avg_package"].mean()
                st.metric("Avg Package", f"{avg_package:.1f} LPA")
            
            # Top companies visualization
            st.write("### Top Hiring Companies")
            top_companies = self.college_data["companies"].nlargest(5, "total_hires")
            
            fig = px.bar(
                top_companies,
                x="name",
                y="total_hires",
                color="avg_package",
                title="Top Companies by Number of Hires",
                labels={"name": "Company", "total_hires": "Total Hires", "avg_package": "Avg Package (LPA)"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Export option
            if st.button("📥 Export Company Data"):
                csv = self.college_data["companies"].to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="company_database.csv",
                    mime="text/csv"
                )
    
    def step4_drive_scheduling(self):
        """Step 4: Campus Drive Scheduling"""
        st.info("Schedule and manage campus recruitment drives")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📅 Schedule New Drive")
            
            with st.form("schedule_drive_form"):
                company = st.selectbox(
                    "Select Company *",
                    options=self.college_data["companies"]["name"].tolist()
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
                        # Schedule drive logic here
                        st.success(f"Drive scheduled for {company} on {drive_date}")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Upcoming Drives")
            
            # Display drives
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
            
            st.subheader("📊 Drive Statistics")
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                total_drives = len(self.college_data["drives"])
                st.metric("Total Drives", total_drives)
            with col_stats2:
                upcoming = len(upcoming_drives)
                st.metric("Upcoming", upcoming)
            with col_stats3:
                completed = len(drives_df[drives_df["status"] == "Completed"])
                st.metric("Completed", completed)
            
            # Drive calendar view
            st.subheader("🗓️ Drive Calendar")
            
            # Create a simple calendar display
            calendar_data = []
            for _, drive in self.college_data["drives"].iterrows():
                calendar_data.append({
                    "Company": drive["company"],
                    "Date": drive["date"],
                    "Mode": drive["mode"],
                    "Status": drive["status"]
                })
            
            calendar_df = pd.DataFrame(calendar_data)
            calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])
            calendar_df = calendar_df.sort_values("Date")
            
            # Display as timeline
            fig = px.timeline(
                calendar_df,
                x_start="Date",
                x_end="Date",
                y="Company",
                color="Status",
                title="Campus Drive Timeline",
                labels={"Date": "Date", "Company": "Company"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def step5_student_company_matching(self):
        """Step 5: Student-Company Matching"""
        st.info("Match students with suitable companies based on criteria")
        
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
                    (matched_students["department"].isin(company_requirements["preferred_departments"])) &
                    (matched_students["placement_status"] == "Not Placed")
                ]
                
                st.metric("Matching Students", len(matched_students))
        
        with col2:
            st.subheader("👥 Matched Students")
            
            if 'matched_students' in locals() and not matched_students.empty:
                # Display matched students
                st.dataframe(
                    matched_students[
                        ["student_id", "name", "department", "cgpa", "backlogs", "email"]
                    ].sort_values("cgpa", ascending=False),
                    use_container_width=True,
                    height=400
                )
                
                # Matching statistics
                st.subheader("📊 Matching Statistics")
                
                col_stats1, col_stats2, col_stats3 = st.columns(3)
                with col_stats1:
                    avg_cgpa = matched_students["cgpa"].mean()
                    st.metric("Avg CGPA", f"{avg_cgpa:.2f}")
                with col_stats2:
                    total_students = len(matched_students)
                    st.metric("Total Matched", total_students)
                with col_stats3:
                    top_dept = matched_students["department"].mode()[0]
                    st.metric("Top Department", top_dept)
                
                # Send notification option
                if st.button("📧 Notify Matched Students"):
                    st.success(f"Notification sent to {len(matched_students)} students about {selected_company} drive")
            else:
                st.info("Select a company to see matching students")
        
        # Automated matching for all companies
        st.subheader("🤖 Automated Matching Report")
        
        # Generate matching report for all companies
        if st.button("Generate Matching Report"):
            matching_report = []
            
            for _, company in self.college_data["companies"].iterrows():
                # Simulate matching for each company
                matched = self.college_data["students"][
                    (self.college_data["students"]["cgpa"] >= 7.0) &
                    (self.college_data["students"]["placement_status"] == "Not Placed")
                ].head(np.random.randint(5, 20))
                
                matching_report.append({
                    "Company": company["name"],
                    "Matched Students": len(matched),
                    "Avg CGPA": matched["cgpa"].mean() if not matched.empty else 0,
                    "Top Department": matched["department"].mode()[0] if not matched.empty else "N/A"
                })
            
            report_df = pd.DataFrame(matching_report)
            st.dataframe(report_df, use_container_width=True)
            
            # Visualize matching
            fig = px.bar(
                report_df,
                x="Company",
                y="Matched Students",
                color="Avg CGPA",
                title="Student-Company Matching Overview",
                labels={"Company": "Company", "Matched Students": "Number of Matched Students"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def step6_interview_management(self):
        """Step 6: Interview Management"""
        st.info("Schedule and track interview progress for students")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("📝 Schedule Interview")
            
            with st.form("schedule_interview_form"):
                student_id = st.selectbox(
                    "Select Student *",
                    options=self.college_data["students"]["student_id"].tolist()
                )
                company = st.selectbox(
                    "Company *",
                    options=self.college_data["companies"]["name"].tolist()
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
                        # Schedule interview logic here
                        st.success(f"Interview scheduled for {student_id} with {company}")
                    else:
                        st.error("Please fill all required fields (*)")
        
        with col2:
            st.subheader("📋 Interview Schedule")
            
            # Display interviews
            interviews_df = self.college_data["interviews"].copy()
            interviews_df["datetime"] = pd.to_datetime(interviews_df["date"] + " " + interviews_df["time"])
            upcoming_interviews = interviews_df[interviews_df["datetime"] >= pd.Timestamp.now()]
            
            if not upcoming_interviews.empty:
                st.dataframe(
                    upcoming_interviews[
                        ["student_id", "student_name", "company", "round", "date", "time", "mode", "status"]
                    ],
                    use_container_width=True,
                    height=300
                )
            else:
                st.info("No upcoming interviews scheduled")
            
            st.subheader("📊 Interview Statistics")
            
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            with col_stats1:
                total_interviews = len(interviews_df)
                st.metric("Total Interviews", total_interviews)
            with col_stats2:
                scheduled = len(interviews_df[interviews_df["status"] == "Scheduled"])
                st.metric("Scheduled", scheduled)
            with col_stats3:
                completed = len(interviews_df[interviews_df["status"] == "Completed"])
                st.metric("Completed", completed)
            
            # Interview results
            st.subheader("📈 Interview Results")
            
            if not interviews_df.empty:
                result_counts = interviews_df["result"].value_counts()
                
                fig = px.pie(
                    values=result_counts.values,
                    names=result_counts.index,
                    title="Interview Results Distribution",
                    hole=0.3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Interview feedback and tracking
        st.subheader("📋 Interview Feedback Management")
        
        col_feedback1, col_feedback2 = st.columns(2)
        
        with col_feedback1:
            st.write("### Update Interview Status")
            
            if not interviews_df.empty:
                interview_to_update = st.selectbox(
                    "Select Interview to Update",
                    options=interviews_df["interview_id"].tolist()
                )
                
                new_status = st.selectbox(
                    "Update Status",
                    options=["Scheduled", "In Progress", "Completed", "Cancelled"]
                )
                
                new_result = st.selectbox(
                    "Update Result",
                    options=["Pending", "Selected", "Rejected", "On Hold"]
                )
                
                feedback = st.text_area("Interview Feedback")
                
                if st.button("Update Interview"):
                    st.success(f"Updated interview {interview_to_update}")
        
        with col_feedback2:
            st.write("### Interview Performance")
            
            # Company-wise interview performance
            company_performance = interviews_df.groupby("company").agg({
                "interview_id": "count",
                "result": lambda x: (x == "Selected").sum()
            }).reset_index()
            company_performance["selection_rate"] = (company_performance["result"] / company_performance["interview_id"]) * 100
            
            fig = px.bar(
                company_performance,
                x="company",
                y="selection_rate",
                title="Selection Rate by Company",
                labels={"company": "Company", "selection_rate": "Selection Rate (%)"}
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def step7_placement_records(self):
        """Step 7: Placement Records Management"""
        st.info("Manage and track all placement offers and records")
        
        # Overall placement statistics
        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        with col_stats1:
            total_placements = len(self.college_data["placements"])
            st.metric("Total Placements", total_placements)
        with col_stats2:
            avg_package = self.college_data["placements"]["package"].mean()
            st.metric("Avg Package (LPA)", f"{avg_package:.2f}")
        with col_stats3:
            unique_companies = self.college_data["placements"]["company"].nunique()
            st.metric("Companies", unique_companies)
        with col_stats4:
            highest_package = self.college_data["placements"]["package"].max()
            st.metric("Highest Package", f"{highest_package:.2f} LPA")
        
        # Placement records table
        st.subheader("📋 Placement Records")
        
        # Filters
        col_filters1, col_filters2, col_filters3 = st.columns(3)
        with col_filters1:
            company_filter = st.multiselect(
                "Filter by Company",
                options=self.college_data["placements"]["company"].unique()
            )
        with col_filters2:
            dept_filter = st.multiselect(
                "Filter by Department",
                options=self.college_data["placements"]["department"].unique()
            )
        with col_filters3:
            package_range = st.slider(
                "Package Range (LPA)",
                min_value=0.0,
                max_value=40.0,
                value=(0.0, 40.0),
                step=1.0
            )
        
        # Apply filters
        filtered_placements = self.college_data["placements"].copy()
        
        if company_filter:
            filtered_placements = filtered_placements[filtered_placements["company"].isin(company_filter)]
        
        if dept_filter:
            filtered_placements = filtered_placements[filtered_placements["department"].isin(dept_filter)]
        
        filtered_placements = filtered_placements[
            (filtered_placements["package"] >= package_range[0]) &
            (filtered_placements["package"] <= package_range[1])
        ]
        
        # Display table
        st.dataframe(
            filtered_placements,
            use_container_width=True,
            height=400
        )
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.subheader("🏢 Placements by Company")
            
            company_placements = filtered_placements["company"].value_counts().head(10)
            
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
            
            fig2 = px.histogram(
                filtered_placements,
                x="package",
                nbins=20,
                title="Package Distribution",
                labels={"package": "Package (LPA)", "count": "Number of Students"}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Department-wise analysis
        st.subheader("🎓 Department-wise Placement Analysis")
        
        dept_analysis = filtered_placements.groupby("department").agg({
            "placement_id": "count",
            "package": ["mean", "max", "min"]
        }).reset_index()
        
        dept_analysis.columns = ["Department", "Total Placements", "Avg Package", "Max Package", "Min Package"]
        
        col_dept1, col_dept2 = st.columns(2)
        
        with col_dept1:
            st.dataframe(
                dept_analysis.sort_values("Avg Package", ascending=False),
                use_container_width=True
            )
        
        with col_dept2:
            fig3 = px.bar(
                dept_analysis,
                x="Department",
                y=["Avg Package", "Max Package"],
                title="Package Comparison by Department",
                labels={"value": "Package (LPA)", "variable": "Package Type"},
                barmode="group"
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Add new placement record
        st.subheader("➕ Add New Placement Record")
        
        with st.form("add_placement_form"):
            col_new1, col_new2, col_new3 = st.columns(3)
            
            with col_new1:
                new_student = st.selectbox(
                    "Student",
                    options=self.college_data["students"]["name"].tolist()
                )
                new_company = st.text_input("Company *")
            
            with col_new2:
                new_job_role = st.text_input("Job Role *")
                new_package = st.number_input("Package (LPA) *", min_value=0.0, max_value=100.0, value=12.0)
            
            with col_new3:
                new_dept = st.selectbox(
                    "Department",
                    options=self.college_data["students"]["department"].unique()
                )
                new_status = st.selectbox(
                    "Status",
                    options=["Offer Received", "Offer Accepted", "Joined", "Internship Completed"]
                )
            
            if st.form_submit_button("Add Placement Record"):
                if new_company and new_job_role and new_package:
                    st.success(f"Added placement record for {new_student} at {new_company}")
                else:
                    st.error("Please fill all required fields (*)")
        
        # Export option
        if st.button("📥 Export Placement Data"):
            csv = filtered_placements.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="placement_records.csv",
                mime="text/csv"
            )
    
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
                "📅 Monthly Placement Trends",
                "📊 Comprehensive Analytics Report"
            ]
        )
        
        # Date range for report
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", value=datetime.now().date() - timedelta(days=365))
        with col_date2:
            end_date = st.date_input("End Date", value=datetime.now().date())
        
        # Generate report button
        if st.button("📊 Generate Report", type="primary"):
            st.success(f"Generating {report_type}...")
            
            # Report content based on selection
            if "Annual Placement Report" in report_type:
                self.generate_annual_report(start_date, end_date)
            elif "Company Performance Report" in report_type:
                self.generate_company_report(start_date, end_date)
            elif "Department Performance Report" in report_type:
                self.generate_department_report(start_date, end_date)
            elif "Monthly Placement Trends" in report_type:
                self.generate_monthly_trends(start_date, end_date)
            else:
                self.generate_comprehensive_report(start_date, end_date)
    
    def generate_annual_report(self, start_date, end_date):
        """Generate annual placement report"""
        st.subheader("📈 Annual Placement Report")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_placements = len(self.college_data["placements"])
            st.metric("Total Placements", total_placements)
        with col2:
            avg_package = self.college_data["placements"]["package"].mean()
            st.metric("Average Package", f"{avg_package:.2f} LPA")
        with col3:
            highest_package = self.college_data["placements"]["package"].max()
            st.metric("Highest Package", f"{highest_package:.2f} LPA")
        with col4:
            companies_count = self.college_data["placements"]["company"].nunique()
            st.metric("Companies Visited", companies_count)
        
        # Key metrics chart
        metrics_data = pd.DataFrame({
            "Metric": ["Placement Rate", "Avg Package", "Student Satisfaction", "Company Satisfaction"],
            "Score": [82, 18.5, 88, 92],
            "Target": [85, 20, 90, 90]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name="Actual",
            x=metrics_data["Metric"],
            y=metrics_data["Score"],
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            name="Target",
            x=metrics_data["Metric"],
            y=metrics_data["Target"],
            marker_color='lightsalmon'
        ))
        
        fig.update_layout(
            title="Key Performance Metrics vs Targets",
            barmode="group",
            yaxis_title="Score"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("📋 Recommendations for Next Year")
        
        recommendations = [
            "Increase focus on core engineering companies",
            "Improve industry-academia collaboration",
            "Enhance soft skills training programs",
            "Expand company outreach to startups and unicorns",
            "Implement better pre-placement training modules"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    
    def generate_company_report(self, start_date, end_date):
        """Generate company performance report"""
        st.subheader("🏢 Company Performance Report")
        
        # Company performance metrics
        company_metrics = []
        for _, company in self.college_data["companies"].iterrows():
            company_metrics.append({
                "Company": company["name"],
                "Visits": company["visits_this_year"],
                "Total Hires": company["total_hires"],
                "Avg Package": company["avg_package"],
                "Selection Rate": f"{np.random.randint(10, 50)}%"
            })
        
        metrics_df = pd.DataFrame(company_metrics)
        st.dataframe(metrics_df.sort_values("Total Hires", ascending=False), use_container_width=True)
        
        # Visualization
        fig = px.scatter(
            metrics_df,
            x="Total Hires",
            y="Avg Package",
            size="Visits",
            color="Company",
            title="Company Performance: Hires vs Package",
            labels={"Total Hires": "Number of Hires", "Avg Package": "Average Package (LPA)"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_department_report(self, start_date, end_date):
        """Generate department performance report"""
        st.subheader("🎓 Department Performance Report")
        
        # Department-wise analysis
        dept_stats = []
        for dept in self.college_data["students"]["department"].unique():
            dept_students = self.college_data["students"][self.college_data["students"]["department"] == dept]
            placed_students = dept_students[dept_students["placement_status"] == "Placed"]
            
            dept_stats.append({
                "Department": dept,
                "Total Students": len(dept_students),
                "Placed Students": len(placed_students),
                "Placement Rate": f"{(len(placed_students)/len(dept_students)*100):.1f}%",
                "Avg CGPA": dept_students["cgpa"].mean(),
                "Avg Package": placed_students["package"].mean() if not placed_students.empty else 0
            })
        
        stats_df = pd.DataFrame(dept_stats)
        st.dataframe(stats_df.sort_values("Placement Rate", ascending=False), use_container_width=True)
        
        # Comparative visualization
        fig = px.bar(
            stats_df,
            x="Department",
            y=["Placement Rate", "Avg Package"],
            title="Department Performance Comparison",
            barmode="group",
            labels={"value": "Score", "variable": "Metric"}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_monthly_trends(self, start_date, end_date):
        """Generate monthly placement trends"""
        st.subheader("📅 Monthly Placement Trends")
        
        # Simulate monthly data
        months = pd.date_range(start=start_date, end=end_date, freq='MS').strftime('%b %Y')
        monthly_data = pd.DataFrame({
            "Month": months,
            "Placements": np.random.randint(10, 50, size=len(months)),
            "Avg Package": np.random.uniform(10, 25, size=len(months)),
            "Companies": np.random.randint(5, 15, size=len(months))
        })
        
        # Line chart for trends
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_data["Month"],
            y=monthly_data["Placements"],
            name="Placements",
            yaxis="y"
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_data["Month"],
            y=monthly_data["Avg Package"],
            name="Avg Package (LPA)",
            yaxis="y2"
        ))
        
        fig.update_layout(
            title="Monthly Placement Trends",
            xaxis_title="Month",
            yaxis=dict(title="Number of Placements", side="left"),
            yaxis2=dict(title="Average Package (LPA)", side="right", overlaying="y"),
            legend=dict(x=0.1, y=1.1, orientation="h")
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display monthly data
        st.dataframe(monthly_data, use_container_width=True)
    
    def generate_comprehensive_report(self, start_date, end_date):
        """Generate comprehensive analytics report"""
        st.subheader("📊 Comprehensive Analytics Report")
        
        # Executive Summary
        st.subheader("📋 Executive Summary")
        
        summary_cols = st.columns(3)
        with summary_cols[0]:
            st.metric("Overall Placement Rate", "82%", "+2% YoY")
        with summary_cols[1]:
            st.metric("Average Package", "18.5 LPA", "+1.5 LPA YoY")
        with summary_cols[2]:
            st.metric("Top Recruiter", "Google", "25 offers")
        
        # SWOT Analysis
        st.subheader("🔍 SWOT Analysis")
        
        swot_cols = st.columns(2)
        
        with swot_cols[0]:
            st.write("**Strengths**")
            strengths = [
                "Strong industry connections",
                "High-quality technical curriculum",
                "Active alumni network",
                "Good campus infrastructure"
            ]
            for strength in strengths:
                st.write(f"✓ {strength}")
            
            st.write("**Weaknesses**")
            weaknesses = [
                "Limited soft skills training",
                "Low participation in core companies",
                "Seasonal placement patterns"
            ]
            for weakness in weaknesses:
                st.write(f"✗ {weakness}")
        
        with swot_cols[1]:
            st.write("**Opportunities**")
            opportunities = [
                "Growing startup ecosystem",
                "Remote work opportunities",
                "International placements",
                "Industry research collaborations"
            ]
            for opportunity in opportunities:
                st.write(f"🔮 {opportunity}")
            
            st.write("**Threats**")
            threats = [
                "Economic slowdown",
                "Increased competition",
                "Changing industry requirements",
                "Skill gap issues"
            ]
            for threat in threats:
                st.write(f"⚠️ {threat}")
        
        # Action Plan
        st.subheader("🎯 Recommended Action Plan")
        
        action_plan = pd.DataFrame({
            "Priority": ["High", "High", "Medium", "Medium", "Low"],
            "Action": [
                "Implement comprehensive soft skills program",
                "Increase core company outreach",
                "Establish industry mentorship program",
                "Enhance interview preparation modules",
                "Develop international placement cell"
            ],
            "Timeline": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025"],
            "Responsibility": ["Placement Cell", "Department Heads", "Alumni Association", "Training Team", "International Office"]
        })
        
        st.dataframe(action_plan, use_container_width=True)
        
        # Download report option
        st.download_button(
            label="📥 Download Complete Report",
            data="This is a sample comprehensive report content.",
            file_name="comprehensive_placement_report.pdf",
            mime="application/pdf"
        )
    
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
