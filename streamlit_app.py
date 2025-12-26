import streamlit as st
import pandas as pd
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

# Initialize session state
if 'workflow_manager' not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

if 'student_flow' not in st.session_state:
    st.session_state.student_flow = StudentFlow()

if 'college_flow' not in st.session_state:
    st.session_state.college_flow = CollegeFlow()

if 'recruiter_flow' not in st.session_state:
    st.session_state.recruiter_flow = RecruiterFlow()

# Initialize role in session state
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

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
    if role != st.session_state.get('selected_role'):
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
        st.session_state.demo_mode = not st.session_state.get('demo_mode', False)
        st.rerun()
    
    if st.session_state.get('demo_mode', False):
        st.success("Demo Mode Active")
    
    # Footer
    st.divider()
    st.caption("🎓 Hackathon Project 2024")

# Main content area - Show selected workflow
if st.session_state.selected_role == "👨‍🎓 Student":
    # Get current step and display appropriate module
    current_step = st.session_state.get('current_step_student', 1)
    st.session_state.student_flow.current_step = current_step
    st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    # Get current step and display appropriate module
    current_step = st.session_state.get('current_step_college', 1)
    st.session_state.college_flow.current_step = current_step
    st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    st.session_state.recruiter_flow.display()
    
else:
    # Observer view
    st.session_state.workflow_manager.display_observer_view()
    
    # Add platform overview for observers
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
