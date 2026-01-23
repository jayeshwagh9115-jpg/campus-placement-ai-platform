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

# Add this function at the top
def check_database_status():
    """Check and display database connection status"""
    if 'db_manager' not in st.session_state:
        return "Not initialized"
    
    db = st.session_state.db_manager
    
    if not db:
        return "No database manager"
    
    if db.is_connected:
        try:
            # Test with actual query
            test_data = db.get_students(limit=1)
            return f"✅ Connected | Students: {len(test_data)}"
        except Exception as e:
            return f"⚠️ Connected but query failed: {str(e)[:50]}"
    else:
        return "❌ Not connected"

# Update the sidebar to show DB status
with st.sidebar:
    st.divider()
    st.caption("Database Status")
    
    if st.session_state.get('db_manager'):
        status_text = check_database_status()
        if "✅" in status_text:
            st.success(status_text)
        elif "⚠️" in status_text:
            st.warning(status_text)
        else:
            st.error(status_text)
    
    # Add debug button
    if st.button("🔧 Debug Database", type="secondary"):
        with st.expander("Debug Info", expanded=True):
            db = st.session_state.get('db_manager')
            if db:
                st.write("URL:", db.url)
                st.write("Key available:", "Yes" if db.key else "No")
                st.write("Connected:", db.is_connected)
                
                # Test query
                if st.button("Test Query"):
                    try:
                        students = db.get_students(limit=3)
                        st.write(f"Students found: {len(students)}")
                        if students:
                            st.json(students[0])
                    except Exception as e:
                        st.error(f"Query failed: {e}")
            else:
                st.error("No database manager")


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

# Initialize all session state objects
if 'workflow_manager' not in st.session_state:
    st.session_state.workflow_manager = WorkflowManager()

if 'student_flow' not in st.session_state:
    st.session_state.student_flow = StudentFlow()

if 'college_flow' not in st.session_state:
    st.session_state.college_flow = CollegeFlow()

if 'recruiter_flow' not in st.session_state:
    st.session_state.recruiter_flow = RecruiterFlow()

# Initialize session state variables
if 'recruiter_step' not in st.session_state:
    st.session_state.recruiter_step = 1
    
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

if 'current_step_student' not in st.session_state:
    st.session_state.current_step_student = 1
    
if 'current_step_college' not in st.session_state:
    st.session_state.current_step_college = 1

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
        # Reset steps when switching roles
        st.session_state.recruiter_step = 1
        st.session_state.current_step_student = 1
        st.session_state.current_step_college = 1
        st.rerun()
    
    st.divider()
    
    # Show workflow based on selected role
    if st.session_state.selected_role == "👨‍🎓 Student":
        st.session_state.workflow_manager.display_student_workflow()
    elif st.session_state.selected_role == "🏫 College Admin":
        st.session_state.workflow_manager.display_college_workflow()
    elif st.session_state.selected_role == "💼 Recruiter":
        # Create recruiter sidebar navigation
        with st.sidebar:
            st.subheader("📋 Recruiter Hiring Process")
            
            # Define all steps
            steps = [
                "🏢 Company Profile",
                "📋 Job Posting",
                "🔍 Candidate Search",
                "🤖 AI Screening",
                "📅 Interview Scheduling",
                "⭐ Candidate Evaluation",
                "📄 Offer Management",
                "📊 Hiring Analytics"
            ]
            
            # Create step selection
            selected_step = st.radio(
                "Select Step:",
                steps,
                index=st.session_state.recruiter_step - 1,
                key="recruiter_step_selector"
            )
            
            # Update current step based on selection
            step_index = steps.index(selected_step) + 1
            st.session_state.recruiter_step = step_index
            
            # Display status
            st.divider()
            st.caption(f"**Current Step:** {step_index}/8")
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Previous", key="recruiter_prev", disabled=(step_index == 1)):
                    st.session_state.recruiter_step -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", key="recruiter_next", disabled=(step_index == 8)):
                    st.session_state.recruiter_step += 1
                    st.rerun()
    else:
        st.session_state.workflow_manager.display_observer_dashboard()

# Main content
if st.session_state.selected_role == "👨‍🎓 Student":
    # Get current step from session state
    current_step = st.session_state.current_step_student
    st.session_state.student_flow.current_step = current_step
    st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    # Get current step from session state
    current_step = st.session_state.current_step_college
    st.session_state.college_flow.current_step = current_step
    st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    # Display recruiter flow with current step
    st.session_state.recruiter_flow.display(st.session_state.recruiter_step)
    
elif st.session_state.selected_role == "👀 Observer":
    # Display observer dashboard
    st.header("📊 Observer Dashboard")
    st.info("Welcome to the Observer Dashboard. This view provides an overview of all platform activities.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", "1,250")
    with col2:
        st.metric("Active Jobs", "45")
    with col3:
        st.metric("Companies", "32")
    
    st.divider()
    
    # Recent activities
    st.subheader("Recent Activities")
    activities = pd.DataFrame({
        "Time": ["10:30 AM", "09:45 AM", "Yesterday", "Yesterday", "2 days ago"],
        "Activity": [
            "TechCorp Solutions posted new job: Frontend Developer",
            "John Doe (Student) applied for Software Engineer position",
            "IIT Bombay uploaded 250 student records",
            "5 interviews scheduled for Amazon positions",
            "Microsoft extended offers to 3 candidates"
        ],
        "Type": ["Job Posting", "Application", "Data Upload", "Interview", "Offer"]
    })
    
    st.dataframe(activities, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
