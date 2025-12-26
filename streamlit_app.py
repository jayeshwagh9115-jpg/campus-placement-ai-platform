import streamlit as st
import pandas as pd
from database.db_manager import db_manager
from modules.workflow_manager import WorkflowManager
from modules.student_flow import StudentFlow
from modules.college_flow import CollegeFlow
from modules.recruiter_flow import RecruiterFlow

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database session
if 'db' not in st.session_state:
    st.session_state.db = db_manager
if 'user' not in st.session_state:
    st.session_state.user = None
if 'student' not in st.session_state:
    st.session_state.student = None

# Initialize workflow manager
workflow = WorkflowManager()

# Initialize user flows
if 'student_flow' not in st.session_state:
    st.session_state.student_flow = StudentFlow()
if 'college_flow' not in st.session_state:
    st.session_state.college_flow = CollegeFlow()
if 'recruiter_flow' not in st.session_state:
    st.session_state.recruiter_flow = RecruiterFlow()

# Title and description
st.title("🎓 AI-Powered Campus Placement Management System")
st.markdown("""
### National Level Hackathon Project
**A Systematic End-to-End Placement Management Platform**
""")

# Sidebar for authentication
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    
    if st.session_state.user is None:
        # Login form
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_as = st.selectbox("Login as", ["Student", "College Admin", "Recruiter"])
            
            if st.form_submit_button("Login"):
                user = db_manager.authenticate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.session_state.role = login_as.lower()
                    
                    # Load student data if student
                    if login_as.lower() == 'student':
                        student = db_manager.get_student_by_user_id(user['user_id'])
                        if student:
                            st.session_state.student = student
                    
                    st.success(f"Welcome {user['full_name']}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        # Demo mode
        if st.button("🎮 Try Demo Mode"):
            st.session_state.demo_mode = True
            st.session_state.role = 'student'
            st.rerun()
    
    else:
        # User is logged in
        st.subheader(f"👋 Welcome, {st.session_state.user['full_name']}")
        st.write(f"**Role:** {st.session_state.role.title()}")
        
        # Role-based navigation
        user_role = st.radio(
            "Select Workflow:",
            ["👨‍🎓 Student Journey", "🏫 College Management", "💼 Recruiter Portal"],
            key="workflow_selection"
        )
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.user = None
            st.session_state.student = None
            st.session_state.role = None
            st.rerun()

# Main content area
if st.session_state.user is None and not st.session_state.get('demo_mode', False):
    # Show landing page
    st.info("👈 Please login from the sidebar to access the platform")
    
    # Platform overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🗄️ Database Backed")
        st.write("Secure SQLite database with complete data persistence")
    with col2:
        st.markdown("### 🔄 Systematic Workflow")
        st.write("End-to-end placement management with proper flow")
    with col3:
        st.markdown("### 🤖 AI Integrated")
        st.write("Intelligent resume building and placement prediction")
    
    # Database statistics
    try:
        stats = db_manager.get_placement_statistics()
        st.subheader("📊 Platform Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", stats.get('total_students', 0))
        with col2:
            st.metric("Placement Rate", f"{stats.get('placement_rate', 0):.1f}%")
        with col3:
            st.metric("Avg CGPA", f"{stats.get('avg_cgpa', 0):.2f}")
        with col4:
            st.metric("Avg Package", f"₹{stats.get('avg_package', 0):.1f}L")
    except:
        pass

elif st.session_state.get('demo_mode', False):
    # Demo mode
    st.info("🎮 **Demo Mode Active** - Using sample data")
    workflow.display_observer_view()
    
elif st.session_state.role == 'student':
    # Student workflow
    st.session_state.student_flow.display()
    
elif st.session_state.role == 'college_admin':
    # College admin workflow
    st.session_state.college_flow.display()
    
elif st.session_state.role == 'recruiter':
    # Recruiter workflow
    st.session_state.recruiter_flow.display()

# Footer
st.divider()
st.caption("🎓 AI Campus Placement Platform | Database Integrated | National Level Hackathon")
