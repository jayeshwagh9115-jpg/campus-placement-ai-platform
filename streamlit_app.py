import streamlit as st
import pandas as pd

# Try to import database modules with fallbacks
try:
    from database.supabase_manager import SupabaseManager
    DB_AVAILABLE = True
except ImportError as e:
    DB_AVAILABLE = False
    st.warning(f"Supabase module not available: {e}")

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

# Initialize session state and database
if 'db_manager' not in st.session_state:
    if DB_AVAILABLE:
        try:
            st.session_state.db_manager = SupabaseManager()
            st.session_state.demo_mode = not st.session_state.db_manager.is_connected
        except:
            st.session_state.demo_mode = True
    else:
        st.session_state.demo_mode = True

# Initialize other session state objects
if 'workflow_manager' not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

if 'student_flow' not in st.session_state:
    st.session_state.student_flow = StudentFlow()

if 'college_flow' not in st.session_state:
    st.session_state.college_flow = CollegeFlow()

if 'recruiter_flow' not in st.session_state:
    st.session_state.recruiter_flow = RecruiterFlow()

if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

# Title and description
st.title("🎓 AI-Powered Campus Placement Management System")
st.markdown("""
### National Level Hackathon Project
**A Systematic End-to-End Placement Management Platform**
""")

# Database status
if st.session_state.demo_mode:
    st.warning("⚠️ **Running in Demo Mode** - Data is stored in memory only")
else:
    st.success("✅ **Connected to Supabase Database**")

# ... rest of your app remains the same ...
# Show warning if database not available
if not DB_AVAILABLE:
    st.warning("""
    ⚠️ **Database module not available** - Running in demo mode.
    All data is stored in memory and will be lost when the app restarts.
    """)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Demo mode info
    if st.session_state.demo_mode:
        st.success("🎮 Demo Mode Active")
    
    st.subheader("Select Your Role")
    
    role = st.radio(
        "Choose your role:",
        ["👨‍🎓 Student", "🏫 College Admin", "💼 Recruiter", "👀 Observer"],
        key="role_selection",
        label_visibility="collapsed"
    )
    
    # Store selected role
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

# Main content
# In your streamlit_app.py, make sure you're updating session state correctly:

# Main content section - update this part:
if st.session_state.selected_role == "👨‍🎓 Student":
    # Get current step from session state, default to 1
    current_step = st.session_state.get('current_step_student', 1)
    st.session_state.student_flow.current_step = current_step
    st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    # Get current step from session state, default to 1
    current_step = st.session_state.get('current_step_college', 1)
    # Update the flow's current step
    st.session_state.college_flow.current_step = current_step
    # Display the flow
    st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    st.session_state.recruiter_flow.display()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
