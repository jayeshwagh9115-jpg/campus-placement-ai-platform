import streamlit as st
import pandas as pd
import plotly.express as px

class CollegeFlow:
    def __init__(self):
        self.college_data = self.initialize_college_data()
    
    def initialize_college_data(self):
        """Initialize college data"""
        return {
            "students": self.generate_sample_students(),
            "companies": self.generate_sample_companies(),
            "drives": [],
            "placements": []
        }
    
    def generate_sample_students(self):
        """Generate sample student data"""
        students = []
        departments = ["Computer Science", "Electrical", "Mechanical", "Civil", "IT"]
        
        for i in range(100):
            students.append({
                "id": f"S{i+1:03d}",
                "name": f"Student {i+1}",
                "department": departments[i % len(departments)],
                "cgpa": round(6.5 + (i % 35) / 10, 1),
                "backlogs": i % 4,
                "placement_status": "Not Placed" if i < 70 else "Placed",
                "company": None if i < 70 else ["Google", "Microsoft", "Amazon", "TCS", "Infosys"][i % 5]
            })
        
        return pd.DataFrame(students)
    
    def generate_sample_companies(self):
        """Generate sample company data"""
        companies = [
            {"name": "Google", "industry": "IT", "visiting_date": "2024-03-20", "roles": ["SDE", "PM"]},
            {"name": "Microsoft", "industry": "IT", "visiting_date": "2024-03-25", "roles": ["SDE", "Data Scientist"]},
            {"name": "Amazon", "industry": "E-commerce", "visiting_date": "2024-04-01", "roles": ["SDE", "PM"]},
            {"name": "TCS", "industry": "Consulting", "visiting_date": "2024-04-10", "roles": ["Developer", "Tester"]},
            {"name": "Infosys", "industry": "IT", "visiting_date": "2024-04-15", "roles": ["Developer", "Consultant"]}
        ]
        return pd.DataFrame(companies)
    
    def display(self):
        """Display college admin workflow"""
        st.header("🏫 College Placement Management Dashboard")
        
        # Get current step
        from modules.workflow_manager import WorkflowManager
        workflow = WorkflowManager()
        current_step = workflow.workflows["college"]["current_step"]
        
        # Display step
        if current_step == 1:
            self.step1_student_database()
        elif current_step == 2:
            self.step2_analytics_dashboard()
        elif current_step == 3:
            self.step3_company_registration()
        elif current_step == 4:
            self.step4_drive_scheduling()
        elif current_step == 5:
            self.step5_student_matching()
        elif current_step == 6:
            self.step6_interview_management()
        elif current_step == 7:
            self.step7_placement_records()
        elif current_step == 8:
            self.step8_performance_reports()
    
    def step1_student_database(self):
        """Step 1: Student Database Management"""
        st.subheader("👨‍🎓 Student Database")
        
        # Search and filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search = st.text_input("Search by Name/ID")
        with col2:
            department_filter = st.selectbox("Department", ["All"] + list(self.college_data["students"]["department"].unique()))
        with col3:
            placement_filter = st.selectbox("Placement Status", ["All", "Placed", "Not Placed"])
        
        # Filter data
        filtered_students = self.college_data["students"].copy()
        if search:
            filtered_students = filtered_students[
                filtered_students["name"].str.contains(search, case=False) |
                filtered_students["id"].str.contains(search, case=False)
            ]
        if department_filter != "All":
            filtered_students = filtered_students[filtered_students["department"] == department_filter]
        if placement_filter != "All":
            filtered_students = filtered_students[filtered_students["placement_status"] == placement_filter]
        
        # Display
        st.dataframe(filtered_students, use_container_width=True)
        
        # Statistics
        total_students = len(filtered_students)
        placed_count = len(filtered_students[filtered_students["placement_status"] == "Placed"])
        placement_rate = (placed_count / total_students * 100) if total_students > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", total_students)
        with col2:
            st.metric("Placed Students", placed_count)
        with col3:
            st.metric("Placement Rate", f"{placement_rate:.1f}%")
    
    def step2_analytics_dashboard(self):
        """Step 2: Analytics Dashboard"""
        st.subheader("📊 Analytics Dashboard")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Department-wise placement
            dept_stats = self.college_data["students"].groupby("department").agg({
                "id": "count",
                "placement_status": lambda x: (x == "Placed").sum()
            }).reset_index()
            dept_stats["placement_rate"] = (dept_stats["placement_status"] / dept_stats["id"] * 100)
            
            fig1 = px.bar(dept_stats, x="department", y="placement_rate",
                         title="Placement Rate by Department",
                         color="placement_rate")
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # CGPA distribution
            fig2 = px.histogram(self.college_data["students"], x="cgpa", 
                               title="CGPA Distribution",
                               nbins=20, color_discrete_sequence=['#3498db'])
            st.plotly_chart(fig2, use_container_width=True)
        
        # Top performers
        st.subheader("🏆 Top Performers")
        top_students = self.college_data["students"].sort_values("cgpa", ascending=False).head(10)
        st.dataframe(top_students[["id", "name", "department", "cgpa", "placement_status"]], 
                    use_container_width=True)
    
    # ... (Other steps would follow similar pattern)
