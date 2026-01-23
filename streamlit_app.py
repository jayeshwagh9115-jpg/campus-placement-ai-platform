import streamlit as st
import pandas as pd
import traceback

# Try to import database modules with fallbacks
try:
    from database.supabase_manager import SupabaseManager
    DB_AVAILABLE = True
except ImportError as e:
    DB_AVAILABLE = False
    st.warning(f"Supabase module not available: {e}")

try:
    from modules.workflow_manager import WorkflowManager
    from modules.student_flow import StudentFlow
    from modules.college_flow import CollegeFlow
    from modules.recruiter_flow import RecruiterFlow
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    st.error(f"❌ Failed to import modules: {e}")

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for database
if 'db_manager' not in st.session_state:
    if DB_AVAILABLE:
        try:
            st.session_state.db_manager = SupabaseManager()
            st.session_state.demo_mode = not st.session_state.db_manager.is_connected
            if st.session_state.demo_mode:
                st.warning("⚠️ Database connection failed - Running in Demo Mode")
        except Exception as e:
            st.session_state.demo_mode = True
            st.error(f"Database initialization error: {e}")
    else:
        st.session_state.demo_mode = True

# Initialize all session state objects only if modules are available
if MODULES_AVAILABLE:
    if 'workflow_manager' not in st.session_state:
        st.session_state.workflow_manager = WorkflowManager()

    if 'student_flow' not in st.session_state:
        st.session_state.student_flow = StudentFlow()

    if 'college_flow' not in st.session_state:
        st.session_state.college_flow = CollegeFlow()

    if 'recruiter_flow' not in st.session_state:
        st.session_state.recruiter_flow = RecruiterFlow()
else:
    # Create placeholder objects if modules are not available
    st.session_state.workflow_manager = None
    st.session_state.student_flow = None
    st.session_state.college_flow = None
    st.session_state.recruiter_flow = None

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

# Database status display
if st.session_state.demo_mode:
    st.warning("⚠️ **Running in Demo Mode** - Data is stored in memory only")
else:
    if hasattr(st.session_state.db_manager, 'is_connected') and st.session_state.db_manager.is_connected:
        st.success("✅ **Connected to Supabase Database**")
    else:
        st.error("❌ **Database Connection Failed** - Running in demo mode")

# Show warning if database not available
if not DB_AVAILABLE:
    st.warning("""
    ⚠️ **Database module not available** - Running in demo mode.
    All data is stored in memory and will be lost when the app restarts.
    """)

# Check if modules are available
if not MODULES_AVAILABLE:
    st.error("""
    ❌ **Critical Error: Application modules not found**
    
    Please make sure the following modules exist:
    - `modules/workflow_manager.py`
    - `modules/student_flow.py`
    - `modules/college_flow.py`
    - `modules/recruiter_flow.py`
    
    The app cannot continue without these modules.
    """)
    st.stop()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Database status indicator
    if st.session_state.get('db_manager') and hasattr(st.session_state.db_manager, 'is_connected') and st.session_state.db_manager.is_connected:
        st.success("✅ Live Database")
        
        # Quick stats with error handling
        try:
            stats = st.session_state.db_manager.get_dashboard_stats()
            with st.expander("📊 Quick Stats"):
                st.write(f"👨‍🎓 Students: {stats.get('total_students', 0)}")
                st.write(f"💼 Companies: {stats.get('total_companies', 0)}")
                st.write(f"📋 Active Jobs: {stats.get('active_jobs', 0)}")
                st.write(f"📄 Applications: {stats.get('total_applications', 0)}")
        except Exception as e:
            st.warning(f"⚠️ Could not load stats: {str(e)[:50]}")
    else:
        st.warning("⚠️ Demo Mode")
    
    st.divider()
    
    # Demo mode info
    if st.session_state.demo_mode:
        st.info("🎮 Demo Mode Active - Using in-memory data")
    
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
        if st.session_state.workflow_manager:
            st.session_state.workflow_manager.display_student_workflow()
    elif st.session_state.selected_role == "🏫 College Admin":
        if st.session_state.workflow_manager:
            st.session_state.workflow_manager.display_college_workflow()
    elif st.session_state.selected_role == "💼 Recruiter":
        # Create recruiter sidebar navigation
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
        if st.session_state.workflow_manager:
            st.session_state.workflow_manager.display_observer_dashboard()

# Main content
try:
    if st.session_state.selected_role == "👨‍🎓 Student":
        if not st.session_state.student_flow:
            st.error("Student flow module not initialized")
            st.stop()
        
        # Get current step from session state
        current_step = st.session_state.current_step_student
        
        # SAFE METHOD: Check if set_database_manager exists before calling
        if not st.session_state.demo_mode and st.session_state.get('db_manager'):
            if hasattr(st.session_state.student_flow, 'set_database_manager'):
                # Use the new method if it exists
                st.session_state.student_flow.set_database_manager(
                    st.session_state.db_manager, 
                    st.session_state.demo_mode
                )
            elif hasattr(st.session_state.student_flow, 'db_manager'):
                # Fallback to old method (set attribute directly)
                st.session_state.student_flow.db_manager = st.session_state.db_manager
                if hasattr(st.session_state.student_flow, 'demo_mode'):
                    st.session_state.student_flow.demo_mode = st.session_state.demo_mode
            else:
                # If neither method exists, just set as attribute
                st.session_state.student_flow.db_manager = st.session_state.db_manager
        else:
            # Demo mode - set to None
            if hasattr(st.session_state.student_flow, 'set_database_manager'):
                st.session_state.student_flow.set_database_manager(None, True)
            elif hasattr(st.session_state.student_flow, 'db_manager'):
                st.session_state.student_flow.db_manager = None
                if hasattr(st.session_state.student_flow, 'demo_mode'):
                    st.session_state.student_flow.demo_mode = True
        
        st.session_state.student_flow.current_step = current_step
        st.session_state.student_flow.display()
        
    elif st.session_state.selected_role == "🏫 College Admin":
        if not st.session_state.college_flow:
            st.error("College flow module not initialized")
            st.stop()
        
        # Get current step from session state
        current_step = st.session_state.current_step_college
        
        # SAFE METHOD for college flow too
        if not st.session_state.demo_mode and st.session_state.get('db_manager'):
            if hasattr(st.session_state.college_flow, 'set_database_manager'):
                st.session_state.college_flow.set_database_manager(
                    st.session_state.db_manager,
                    st.session_state.demo_mode
                )
            elif hasattr(st.session_state.college_flow, 'db_manager'):
                st.session_state.college_flow.db_manager = st.session_state.db_manager
                if hasattr(st.session_state.college_flow, 'demo_mode'):
                    st.session_state.college_flow.demo_mode = st.session_state.demo_mode
            else:
                st.session_state.college_flow.db_manager = st.session_state.db_manager
        else:
            if hasattr(st.session_state.college_flow, 'set_database_manager'):
                st.session_state.college_flow.set_database_manager(None, True)
            elif hasattr(st.session_state.college_flow, 'db_manager'):
                st.session_state.college_flow.db_manager = None
                if hasattr(st.session_state.college_flow, 'demo_mode'):
                    st.session_state.college_flow.demo_mode = True
        
        st.session_state.college_flow.current_step = current_step
        st.session_state.college_flow.display()
        
    elif st.session_state.selected_role == "💼 Recruiter":
        if not st.session_state.recruiter_flow:
            st.error("Recruiter flow module not initialized")
            st.stop()
        
        # For recruiter flow
        if not st.session_state.demo_mode and st.session_state.get('db_manager'):
            if hasattr(st.session_state.recruiter_flow, 'set_database_manager'):
                st.session_state.recruiter_flow.set_database_manager(
                    st.session_state.db_manager,
                    st.session_state.demo_mode
                )
            elif hasattr(st.session_state.recruiter_flow, 'db_manager'):
                st.session_state.recruiter_flow.db_manager = st.session_state.db_manager
                if hasattr(st.session_state.recruiter_flow, 'demo_mode'):
                    st.session_state.recruiter_flow.demo_mode = st.session_state.demo_mode
            else:
                st.session_state.recruiter_flow.db_manager = st.session_state.db_manager
        else:
            if hasattr(st.session_state.recruiter_flow, 'set_database_manager'):
                st.session_state.recruiter_flow.set_database_manager(None, True)
            elif hasattr(st.session_state.recruiter_flow, 'db_manager'):
                st.session_state.recruiter_flow.db_manager = None
                if hasattr(st.session_state.recruiter_flow, 'demo_mode'):
                    st.session_state.recruiter_flow.demo_mode = True
        
        # Display recruiter flow with current step
        st.session_state.recruiter_flow.display(st.session_state.recruiter_step)
        
    elif st.session_state.selected_role == "👀 Observer":
        # Display observer dashboard
        st.header("📊 Observer Dashboard")
        st.info("Welcome to the Observer Dashboard. This view provides an overview of all platform activities.")
        
        # Get real data from database if available
        if not st.session_state.demo_mode and st.session_state.get('db_manager') and hasattr(st.session_state.db_manager, 'is_connected') and st.session_state.db_manager.is_connected:
            db = st.session_state.db_manager
            
            try:
                # Get statistics
                stats = db.get_dashboard_stats()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Students", stats.get('total_students', 0))
                with col2:
                    st.metric("Active Jobs", stats.get('active_jobs', 0))
                with col3:
                    st.metric("Companies", stats.get('total_companies', 0))
                with col4:
                    st.metric("Applications", stats.get('total_applications', 0))
                
                st.divider()
                
                # Recent Activities
                st.subheader("📈 Recent Activities")
                
                # Get recent jobs and applications
                recent_jobs = db.get_jobs()[:5] if hasattr(db, 'get_jobs') else []
                recent_apps = db.get_all_applications()[:5] if hasattr(db, 'get_all_applications') else []
                
                # Combine activities
                activities_data = []
                
                for job in recent_jobs:
                    company_name = job.get('company_name', 'Company')
                    if isinstance(company_name, dict):
                        company_name = company_name.get('name', 'Company')
                    
                    activities_data.append({
                        "Time": job.get('created_at', 'N/A'),
                        "Activity": f"{company_name} posted: {job.get('title', 'Job')}",
                        "Type": "Job Posting",
                        "Status": job.get('status', 'open')
                    })
                
                for app in recent_apps:
                    student_name = app.get('student_name', 'Student')
                    if isinstance(student_name, dict):
                        student_name = student_name.get('full_name', 'Student')
                    
                    job_title = app.get('job_title', 'Position')
                    if isinstance(job_title, dict):
                        job_title = job_title.get('title', 'Position')
                    
                    activities_data.append({
                        "Time": app.get('applied_at', 'N/A'),
                        "Activity": f"{student_name} applied for {job_title}",
                        "Type": "Application",
                        "Status": app.get('status', 'pending')
                    })
                
                # Sort by time and display
                if activities_data:
                    df_activities = pd.DataFrame(activities_data)
                    if 'Time' in df_activities.columns:
                        df_activities = df_activities.sort_values('Time', ascending=False)
                    st.dataframe(df_activities[['Time', 'Activity', 'Type', 'Status']], 
                                use_container_width=True, 
                                hide_index=True)
                else:
                    st.info("No recent activities found.")
                
                st.divider()
                
                # Data Tables Preview
                st.subheader("📋 Data Preview")
                
                tab1, tab2, tab3, tab4 = st.tabs(["Students", "Companies", "Jobs", "Applications"])
                
                with tab1:
                    try:
                        students = db.get_all_students()[:10] if hasattr(db, 'get_all_students') else []
                        if students:
                            df_students = pd.DataFrame(students)
                            st.dataframe(df_students[['full_name', 'email', 'department', 'cgpa']], 
                                        use_container_width=True)
                        else:
                            st.info("No students in database")
                    except Exception as e:
                        st.error(f"Error loading students: {str(e)[:50]}")
                
                with tab2:
                    try:
                        companies = db.get_companies()[:10] if hasattr(db, 'get_companies') else []
                        if companies:
                            df_companies = pd.DataFrame(companies)
                            st.dataframe(df_companies[['name', 'email', 'industry', 'size']], 
                                        use_container_width=True)
                        else:
                            st.info("No companies in database")
                    except Exception as e:
                        st.error(f"Error loading companies: {str(e)[:50]}")
                
                with tab3:
                    try:
                        jobs = db.get_all_jobs()[:10] if hasattr(db, 'get_all_jobs') else []
                        if jobs:
                            df_jobs = pd.DataFrame(jobs)
                            st.dataframe(df_jobs[['title', 'location', 'job_type', 'status']], 
                                        use_container_width=True)
                        else:
                            st.info("No jobs in database")
                    except Exception as e:
                        st.error(f"Error loading jobs: {str(e)[:50]}")
                
                with tab4:
                    try:
                        applications = db.get_all_applications()[:10] if hasattr(db, 'get_all_applications') else []
                        if applications:
                            df_apps = pd.DataFrame(applications)
                            st.dataframe(df_apps[['applied_at', 'status']], 
                                        use_container_width=True)
                        else:
                            st.info("No applications in database")
                    except Exception as e:
                        st.error(f"Error loading applications: {str(e)[:50]}")
                        
            except Exception as e:
                st.error(f"Error loading dashboard data: {str(e)}")
                st.info("Switching to demo mode for this session")
                
                # Fallback to demo data
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Students", "1,250")
                with col2:
                    st.metric("Active Jobs", "45")
                with col3:
                    st.metric("Companies", "32")
                
                st.divider()
                
                # Recent activities (demo)
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
        else:
            # Demo mode data
            st.warning("⚠️ Running in Demo Mode - Showing sample data")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", "1,250")
            with col2:
                st.metric("Active Jobs", "45")
            with col3:
                st.metric("Companies", "32")
            
            st.divider()
            
            # Recent activities (demo)
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

except Exception as e:
    st.error(f"❌ Application Error: {str(e)}")
    with st.expander("Click to see error details"):
        st.code(traceback.format_exc())
    
    st.info("""
    **Troubleshooting Steps:**
    1. Make sure all module files exist in the `modules/` directory
    2. Check that `student_flow.py` has the correct methods
    3. Verify the database connection is working
    4. Try refreshing the page
    """)

# Debug section (collapsed by default)
with st.expander("🔧 Debug Information", expanded=False):
    st.write("**Session State:**")
    st.write(f"- Demo Mode: {st.session_state.demo_mode}")
    st.write(f"- Selected Role: {st.session_state.selected_role}")
    st.write(f"- DB Available: {DB_AVAILABLE}")
    st.write(f"- Modules Available: {MODULES_AVAILABLE}")
    
    if st.session_state.get('db_manager'):
        st.write(f"- DB Manager exists: Yes")
        st.write(f"- DB Connected: {hasattr(st.session_state.db_manager, 'is_connected') and st.session_state.db_manager.is_connected}")
    
    # Check student_flow attributes
    if st.session_state.student_flow:
        st.write("**Student Flow Attributes:**")
        st.write(f"- Has set_database_manager: {hasattr(st.session_state.student_flow, 'set_database_manager')}")
        st.write(f"- Has db_manager attribute: {hasattr(st.session_state.student_flow, 'db_manager')}")
        st.write(f"- Has demo_mode attribute: {hasattr(st.session_state.student_flow, 'demo_mode')}")
    
    # Quick database test
    if st.button("Run Quick Database Test"):
        if st.session_state.get('db_manager'):
            try:
                db = st.session_state.db_manager
                st.write("**Database Test Results:**")
                
                # Test connection
                st.write(f"- Connection Status: {'✅ Connected' if db.is_connected else '❌ Not Connected'}")
                
                if db.is_connected:
                    # Test each table
                    tables = ['students', 'companies', 'job_postings', 'applications', 'colleges']
                    for table in tables:
                        try:
                            data = db.select(table, limit=1)
                            st.write(f"- {table}: {'✅ Accessible' if data is not None else '❌ Not accessible'}")
                        except:
                            st.write(f"- {table}: ❌ Error accessing")
            except Exception as e:
                st.error(f"Database test failed: {e}")

# Add database initialization check
if not st.session_state.demo_mode and st.session_state.get('db_manager') and not st.session_state.db_manager.is_connected:
    st.error("""
    ⚠️ **Database Connection Issue**
    
    The app is trying to connect to the database but failed. Here are some things to check:
    
    1. **Internet Connection**: Make sure you're connected to the internet
    2. **Supabase URL & Key**: Verify they are correct in supabase_manager.py
    3. **Supabase Project**: Make sure your Supabase project is active
    4. **Table Permissions**: Check if tables have proper RLS policies
    5. **Firewall**: Ensure no firewall is blocking the connection
    
    The app will run in **Demo Mode** with sample data.
    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
