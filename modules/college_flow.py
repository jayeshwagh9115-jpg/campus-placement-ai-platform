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
        
        # ... (keep all the existing step1 code) ...
        # [Previous step1 code remains exactly the same]
        
    def step2_analytics_dashboard(self):
        """Step 2: Analytics Dashboard"""
        # ... (keep all the existing step2 code) ...
        # [Previous step2 code remains exactly the same]
        
    def step3_company_registration(self):
        """Step 3: Company Registration & Management"""
        # ... (keep all the existing step3 code) ...
        # [Previous step3 code remains exactly the same]
        
    def step4_drive_scheduling(self):
        """Step 4: Campus Drive Scheduling"""
        # ... (keep all the existing step4 code) ...
        # [Previous step4 code remains exactly the same]
        
    def step5_student_company_matching(self):
        """Step 5: Student-Company Matching"""
        # ... (keep all the existing step5 code) ...
        # [Previous step5 code remains exactly the same]
        
    def step6_interview_management(self):
        """Step 6: Interview Management"""
        # ... (keep all the existing step6 code) ...
        # [Previous step6 code remains exactly the same]
        
    def step7_placement_records(self):
        """Step 7: Placement Records Management"""
        # ... (keep all the existing step7 code) ...
        # [Previous step7 code remains exactly the same]
        
    def step8_performance_reports(self):
        """Step 8: Performance Reports & Analytics"""
        # ... (keep all the existing step8 code) ...
        # [Previous step8 code remains exactly the same]
    
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
