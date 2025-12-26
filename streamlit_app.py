import streamlit as st
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize ALL session state variables
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False
if 'current_step_student' not in st.session_state:
    st.session_state.current_step_student = 1
if 'current_step_college' not in st.session_state:
    st.session_state.current_step_college = 1

# Try to import modules with error handling
try:
    from modules.workflow_manager import WorkflowManager
    from modules.student_flow import StudentFlow
    from modules.college_flow import CollegeFlow
    from modules.recruiter_flow import RecruiterFlow
    
    MODULES_AVAILABLE = True
except ImportError as e:
    st.warning(f"⚠️ Note: Some modules not available: {e}")
    MODULES_AVAILABLE = False
    
    # Create dummy classes to prevent crashes
    class DummyWorkflowManager:
        def display_student_workflow(self):
            st.info("Student workflow - Module not loaded")
        def display_college_workflow(self):
            st.info("College workflow - Module not loaded")
        def display_recruiter_workflow(self):
            st.info("Recruiter workflow - Module not loaded")
        def display_observer_dashboard(self):
            st.info("Observer dashboard - Module not loaded")
        def display_observer_view(self):
            st.info("Observer view - Module not loaded")
    
    class DummyFlow:
        def __init__(self):
            self.current_step = 1
        def display(self):
            st.info("Flow module not loaded. Check your modules directory.")
    
    WorkflowManager = DummyWorkflowManager
    StudentFlow = DummyFlow
    CollegeFlow = DummyFlow
    RecruiterFlow = DummyFlow

# Initialize managers in session state
if 'workflow_manager' not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

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

# Sidebar for workflow selection
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Role selection
    st.subheader("Select Your Role")
    
    # Use radio buttons for role selection
    role = st.radio(
        "Choose your role:",
        ["👨‍🎓 Student", "🏫 College Admin", "💼 Recruiter", "👀 Observer"],
        key="role_selection",
        label_visibility="collapsed"
    )
    
    # Store selected role in session state
    if role != st.session_state.selected_role:
        st.session_state.selected_role = role
        st.rerun()
    
    st.divider()
    
    # Show workflow based on selected role
    if st.session_state.selected_role == "👨‍🎓 Student":
        st.session_state.workflow_manager.display_student_workflow()
        
    elif st.session_state.selected_role == "🏫 College Admin":
        st.session_state.workflow_manager.display_college_workflow()
        
    elif st.session_state.selected_role == "💼 Recruiter":
        st.session_state.workflow_manager.display_recruiter_workflow()
        
    else:
        st.session_state.workflow_manager.display_observer_dashboard()
    
    # Demo mode toggle
    st.divider()
    if st.button("🎮 Toggle Demo Mode", use_container_width=True):
        st.session_state.demo_mode = not st.session_state.demo_mode
        st.rerun()
    
    if st.session_state.demo_mode:
        st.success("✅ Demo Mode Active")
    else:
        st.info("🌐 Live Mode Active")
    
    # Quick stats (always visible)
    st.divider()
    st.subheader("Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Students", "1,250", "+45")
    with col2:
        st.metric("Companies", "85", "+12")
    
    # Footer
    st.divider()
    st.caption("🎓 Hackathon Project 2024")

# Main content area - Show selected workflow
if st.session_state.selected_role == "👨‍🎓 Student":
    # Get current step and display appropriate module
    current_step = st.session_state.current_step_student
    st.session_state.student_flow.current_step = current_step
    
    # Add fallback if module not available
    if not MODULES_AVAILABLE:
        st.header("👨‍🎓 Student Dashboard")
        st.info("Student module not available. Here's a basic interface:")
        st.write(f"Current Step: {current_step}")
        
        # Basic student interface
        if current_step == 1:
            st.subheader("Step 1: Profile Setup")
            name = st.text_input("Name", "John Doe")
            if st.button("Next Step"):
                st.session_state.current_step_student = 2
                st.rerun()
        elif current_step == 2:
            st.subheader("Step 2: Resume Builder")
            if st.button("Previous Step"):
                st.session_state.current_step_student = 1
                st.rerun()
            if st.button("Next Step"):
                st.session_state.current_step_student = 3
                st.rerun()
    else:
        st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    # Get current step and display appropriate module
    current_step = st.session_state.current_step_college
    st.session_state.college_flow.current_step = current_step
    
    # Add fallback if module not available
    if not MODULES_AVAILABLE:
        st.header("🏫 College Admin Dashboard")
        st.info("College admin module not available. Here's a basic interface:")
        st.write(f"Current Step: {current_step}")
        
        # Basic college admin interface
        if current_step == 1:
            st.subheader("Step 1: Student Management")
            if st.button("Next Step"):
                st.session_state.current_step_college = 2
                st.rerun()
        elif current_step == 2:
            st.subheader("Step 2: Company Registration")
            if st.button("Previous Step"):
                st.session_state.current_step_college = 1
                st.rerun()
    else:
        st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    # Add fallback if module not available
    if not MODULES_AVAILABLE:
        st.header("💼 Recruiter Dashboard")
        st.info("Recruiter module not available. Basic interface:")
        st.write("Company Profile Management")
        st.write("Job Posting")
        st.write("Candidate Search")
    else:
        st.session_state.recruiter_flow.display()
    
else:
    # Observer view
    if MODULES_AVAILABLE:
        st.session_state.workflow_manager.display_observer_view()
    else:
        st.header("👀 Observer View")
        st.info("Observer module not available. Showing basic overview.")
    
    # Add platform overview for observers (always show)
    st.header("🚀 Platform Features Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👨‍🎓 Student Features")
        features = [
            "✅ AI Resume Builder",
            "✅ Career Path Planning",
            "✅ Placement Prediction",
            "✅ Interview Preparation",
            "✅ NEP Course Advisor",
            "✅ PM Internship Match"
        ]
        for feature in features:
            st.write(feature)
    
    with col2:
        st.markdown("### 🏫 College Admin Features")
        features = [
            "✅ Student Database",
            "✅ Analytics Dashboard",
            "✅ Company Registration",
            "✅ Drive Scheduling",
            "✅ Student-Company Matching",
            "✅ Interview Management",
            "✅ Placement Records",
            "✅ Performance Reports"
        ]
        for feature in features:
            st.write(feature)
    
    with col3:
        st.markdown("### 💼 Recruiter Features")
        features = [
            "✅ Company Profile",
            "✅ Job Posting",
            "✅ Candidate Search",
            "✅ AI Screening",
            "✅ Interview Scheduling",
            "✅ Offer Management",
            "✅ Hiring Analytics"
        ]
        for feature in features:
            st.write(feature)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python | Database Integrated | Systematic Workflow</p>
</div>
""", unsafe_allow_html=True)

# Add some basic CSS for better appearance
st.markdown("""
<style>
    .stButton > button {
        border-radius: 10px;
    }
    .css-1d391kg {
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)
