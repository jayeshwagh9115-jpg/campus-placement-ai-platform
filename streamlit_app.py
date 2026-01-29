import streamlit as st
import pandas as pd
import traceback
import random
import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Add modules directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def debug_database_save():
    """Debug function to test database save"""
    if st.session_state.get('db_manager') and st.session_state.db_manager.is_connected:
        db = st.session_state.db_manager
        
        # Simple test data
        test_data = {
            "full_name": "Debug Test",
            "email": f"debug{random.randint(1000, 9999)}@test.com",
            "roll_number": f"DEBUG{random.randint(1000, 9999)}",
            "department": "Test"
        }
        
        try:
            # Try different methods
            st.write("**Testing save methods:**")
            
            # Method 1: Direct insert
            st.write("1. Direct insert:")
            result1 = db.insert('students', test_data)
            st.write(f"   Result: {result1}")
            
            # Method 2: Using client directly
            st.write("2. Using client directly:")
            try:
                result2 = db.client.table('students').insert(test_data).execute()
                st.write(f"   Result: {result2.data if result2.data else 'No data'}")
            except Exception as e:
                st.write(f"   Error: {e}")
            
            # Method 3: Raw request
            st.write("3. Raw HTTP request:")
            import requests
            headers = {
                "apikey": db.key,
                "Authorization": f"Bearer {db.key}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                f"{db.url}/rest/v1/students",
                json=test_data,
                headers=headers
            )
            st.write(f"   Status: {response.status_code}")
            st.write(f"   Response: {response.text[:200]}")
            
        except Exception as e:
            st.error(f"Debug error: {e}")

# Try to import database modules with fallbacks
try:
    from database.supabase_manager import SupabaseManager
    DB_AVAILABLE = True
    print("✅ SupabaseManager imported successfully")
except ImportError as e:
    DB_AVAILABLE = False
    print(f"⚠️ Supabase module not available: {e}")

# Try to import modules with better error handling
MODULES_AVAILABLE = False
modules_status = {}

try:
    from modules.workflow_manager import WorkflowManager
    modules_status['workflow_manager'] = True
    print("✅ WorkflowManager imported successfully")
except ImportError as e:
    modules_status['workflow_manager'] = False
    print(f"❌ Failed to import workflow_manager: {e}")

try:
    from modules.student_flow import StudentFlow
    modules_status['student_flow'] = True
    print("✅ StudentFlow imported successfully")
except ImportError as e:
    modules_status['student_flow'] = False
    print(f"❌ Failed to import student_flow: {e}")

try:
    from modules.college_flow import CollegeFlow
    modules_status['college_flow'] = True
    print("✅ CollegeFlow imported successfully")
except ImportError as e:
    modules_status['college_flow'] = False
    print(f"❌ Failed to import college_flow: {e}")

try:
    from modules.recruiter_flow import RecruiterFlow
    modules_status['recruiter_flow'] = True
    print("✅ RecruiterFlow imported successfully")
except ImportError as e:
    modules_status['recruiter_flow'] = False
    print(f"❌ Failed to import recruiter_flow: {e}")

# Check if all modules are available
if all(modules_status.values()):
    MODULES_AVAILABLE = True
    print("✅ All modules imported successfully")
else:
    MODULES_AVAILABLE = False
    print(f"⚠️ Some modules missing: {[k for k, v in modules_status.items() if not v]}")

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
    try:
        if 'workflow_manager' not in st.session_state:
            st.session_state.workflow_manager = WorkflowManager()
            print("✅ WorkflowManager initialized")
        
        if 'student_flow' not in st.session_state:
            st.session_state.student_flow = StudentFlow()
            print("✅ StudentFlow initialized")
        
        if 'college_flow' not in st.session_state:
            # Create placeholder if module not available
            if modules_status.get('college_flow', False):
                st.session_state.college_flow = CollegeFlow()
                print("✅ CollegeFlow initialized")
            else:
                st.session_state.college_flow = None
                print("⚠️ CollegeFlow not available")
        
        if 'recruiter_flow' not in st.session_state:
            # Create placeholder if module not available
            if modules_status.get('recruiter_flow', False):
                st.session_state.recruiter_flow = RecruiterFlow()
                print("✅ RecruiterFlow initialized")
            else:
                st.session_state.recruiter_flow = None
                print("⚠️ RecruiterFlow not available")
                
    except Exception as e:
        st.error(f"Error initializing modules: {e}")
        MODULES_AVAILABLE = False
else:
    # Create placeholder objects if modules are not available
    st.session_state.workflow_manager = None
    st.session_state.student_flow = None
    st.session_state.college_flow = None
    st.session_state.recruiter_flow = None
    print("⚠️ Using placeholder objects for missing modules")

# Initialize session state variables
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None

# Initialize workflow steps if not exists
if 'workflows' not in st.session_state:
    st.session_state.workflows = {
        "student": {"current_step": 1},
        "college": {"current_step": 1},
        "recruiter": {"current_step": 1}
    }

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
    ❌ **Critical Error: Some application modules not found**
    
    Missing modules:
    """)
    
    for module, status in modules_status.items():
        if not status:
            st.write(f"- ❌ `modules/{module}.py`")
    
    st.info("""
    **Temporary Solution:** Creating basic module files for you...
    """)
    
    # Create minimal module files automatically
    create_minimal_modules()
    
    # Try to import again
    st.info("Trying to import modules again...")
    st.rerun()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Database status indicator
    if st.session_state.get('db_manager') and hasattr(st.session_state.db_manager, 'is_connected') and st.session_state.db_manager.is_connected:
        st.success("✅ Live Database")
        
        # Quick stats with error handling
        try:
            if hasattr(st.session_state.db_manager, 'get_dashboard_stats'):
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
        st.rerun()
    
    st.divider()
    
    # Show workflow based on selected role
    if st.session_state.selected_role == "👨‍🎓 Student":
        if st.session_state.workflow_manager:
            try:
                st.session_state.workflow_manager.display_student_workflow()
            except Exception as e:
                st.error(f"Error displaying student workflow: {e}")
        else:
            display_basic_student_sidebar()
    elif st.session_state.selected_role == "🏫 College Admin":
        if st.session_state.workflow_manager:
            try:
                st.session_state.workflow_manager.display_college_workflow()
            except Exception as e:
                st.error(f"Error displaying college workflow: {e}")
        else:
            display_basic_college_sidebar()
    elif st.session_state.selected_role == "💼 Recruiter":
        if st.session_state.workflow_manager:
            try:
                st.session_state.workflow_manager.display_recruiter_workflow()
            except Exception as e:
                st.error(f"Error displaying recruiter workflow: {e}")
        else:
            display_basic_recruiter_sidebar()
    else:
        if st.session_state.workflow_manager:
            try:
                st.session_state.workflow_manager.display_observer_dashboard()
            except Exception as e:
                st.error(f"Error displaying observer dashboard: {e}")
        else:
            display_basic_observer_sidebar()

# Main content
try:
    if st.session_state.selected_role == "👨‍🎓 Student":
        if not st.session_state.student_flow:
            st.error("Student flow module not initialized")
            # Try to create a basic one
            try:
                st.session_state.student_flow = StudentFlow()
            except:
                st.info("Showing basic student interface...")
                display_basic_student_interface()
                st.stop()
        
        # Get current step from workflow
        current_step = st.session_state.workflows["student"]["current_step"]
        
        # Set database manager for student flow
        if not st.session_state.demo_mode and st.session_state.get('db_manager'):
            if hasattr(st.session_state.student_flow, 'set_database_manager'):
                st.session_state.student_flow.set_database_manager(
                    st.session_state.db_manager, 
                    st.session_state.demo_mode
                )
            elif hasattr(st.session_state.student_flow, 'db_manager'):
                st.session_state.student_flow.db_manager = st.session_state.db_manager
                if hasattr(st.session_state.student_flow, 'demo_mode'):
                    st.session_state.student_flow.demo_mode = st.session_state.demo_mode
            else:
                st.session_state.student_flow.db_manager = st.session_state.db_manager
        else:
            if hasattr(st.session_state.student_flow, 'set_database_manager'):
                st.session_state.student_flow.set_database_manager(None, True)
            elif hasattr(st.session_state.student_flow, 'db_manager'):
                st.session_state.student_flow.db_manager = None
                if hasattr(st.session_state.student_flow, 'demo_mode'):
                    st.session_state.student_flow.demo_mode = True
        
        # Sync current step with StudentFlow object
        st.session_state.student_flow.current_step = current_step
        
        # Display student flow
        try:
            st.session_state.student_flow.display()
        except Exception as e:
            st.error(f"Error displaying student flow: {e}")
            st.info("Showing fallback interface...")
            display_fallback_student_interface(current_step)
        
        # REMOVED: Navigation buttons from main content (they are in workflow_manager)
        
    elif st.session_state.selected_role == "🏫 College Admin":
        if not st.session_state.college_flow:
            st.error("College flow module not available")
            display_basic_college_interface()
            st.stop()
        
        # Get current step from workflow
        current_step = st.session_state.workflows["college"]["current_step"]
        
        # Set database manager for college flow
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
        
        # Sync current step with CollegeFlow object
        st.session_state.college_flow.current_step = current_step
        
        # Display college flow with current step
        try:
            if hasattr(st.session_state.college_flow, 'display'):
                st.session_state.college_flow.display()
            else:
                display_fallback_college_interface(current_step)
        except Exception as e:
            st.error(f"Error displaying college flow: {e}")
            display_fallback_college_interface(current_step)
        
        # REMOVED: Navigation buttons from main content (they are in workflow_manager)
        
    elif st.session_state.selected_role == "💼 Recruiter":
        if not st.session_state.recruiter_flow:
            st.error("Recruiter flow module not available")
            display_basic_recruiter_interface()
            st.stop()
        
        # Get current step from workflow
        current_step = st.session_state.workflows["recruiter"]["current_step"]
        
        # Sync current step with RecruiterFlow object
        st.session_state.recruiter_flow.current_step = current_step
        
        # Display recruiter flow with current step
        try:
            if hasattr(st.session_state.recruiter_flow, 'display'):
                st.session_state.recruiter_flow.display()
            else:
                display_fallback_recruiter_interface(current_step)
        except Exception as e:
            st.error(f"Error displaying recruiter flow: {e}")
            display_fallback_recruiter_interface(current_step)
        
        # REMOVED: Navigation buttons from main content (they are in workflow_manager)
        
    elif st.session_state.selected_role == "👀 Observer":
        # Display observer view from workflow manager
        if st.session_state.workflow_manager:
            try:
                if hasattr(st.session_state.workflow_manager, 'display_observer_view'):
                    st.session_state.workflow_manager.display_observer_view()
                else:
                    display_fallback_observer_view()
            except Exception as e:
                st.error(f"Error displaying observer view: {e}")
                display_fallback_observer_view()
        else:
            # Fallback if workflow manager is not available
            display_fallback_observer_view()

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
    
    # Check workflow status
    st.write("**Workflow Status:**")
    st.write(f"- Student Step: {st.session_state.workflows['student']['current_step']}")
    st.write(f"- College Step: {st.session_state.workflows['college']['current_step']}")
    st.write(f"- Recruiter Step: {st.session_state.workflows['recruiter']['current_step']}")
    
    # Check student_flow attributes
    if st.session_state.student_flow:
        st.write("**Student Flow Attributes:**")
        st.write(f"- Has set_database_manager: {hasattr(st.session_state.student_flow, 'set_database_manager')}")
        st.write(f"- Has db_manager attribute: {hasattr(st.session_state.student_flow, 'db_manager')}")
        st.write(f"- Has demo_mode attribute: {hasattr(st.session_state.student_flow, 'demo_mode')}")
    
    # Module status
    st.write("**Module Import Status:**")
    for module, status in modules_status.items():
        st.write(f"- {module}: {'✅' if status else '❌'}")
    
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
    
    # Reset workflow button
    if st.button("🔄 Reset All Workflow Steps"):
        st.session_state.workflows["student"]["current_step"] = 1
        st.session_state.workflows["college"]["current_step"] = 1
        st.session_state.workflows["recruiter"]["current_step"] = 1
        st.rerun()
        
    # Debug database save button
    if st.button("🔧 Test Database Save"):
        debug_database_save()

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

# ========== FALLBACK DISPLAY METHODS ==========

def display_basic_student_interface():
    """Basic student interface fallback"""
    st.header("👨‍🎓 Student Interface (Basic)")
    st.info("The student flow module is not available. Showing basic interface.")
    
    current_step = st.session_state.workflows["student"]["current_step"]
    
    if current_step == 1:
        st.subheader("Step 1: Profile Creation")
        st.write("Please create your profile")
        name = st.text_input("Name")
        email = st.text_input("Email")
        if st.button("Save Profile"):
            st.success("Profile saved (demo)")
    elif current_step == 2:
        st.subheader("Step 2: Resume Building")
        st.write("Build your resume here")
        st.text_area("Resume Content", height=200)
        if st.button("Save Resume"):
            st.success("Resume saved (demo)")
    elif current_step == 3:
        st.subheader("Step 3: Skill Assessment")
        st.write("Take skill assessment tests")
    else:
        st.write(f"Step {current_step} content would go here")

def display_fallback_student_interface(current_step):
    """Fallback interface for student"""
    st.header(f"👨‍🎓 Student - Step {current_step}")
    st.info("This is a fallback interface")
    st.write(f"You are on step {current_step} of 8")

def display_basic_college_interface():
    """Basic college interface fallback"""
    st.header("🏫 College Admin Interface (Basic)")
    st.info("The college flow module is not available.")
    
    st.write("College administration features:")
    st.write("- Student management")
    st.write("- Placement statistics")
    st.write("- Company coordination")

def display_fallback_college_interface(current_step):
    """Fallback interface for college admin"""
    st.header(f"🏫 College Admin - Step {current_step}")
    st.info("Fallback interface for college admin")

def display_basic_recruiter_interface():
    """Basic recruiter interface fallback"""
    st.header("💼 Recruiter Interface (Basic)")
    st.info("The recruiter flow module is not available.")
    
    st.write("Recruiter features:")
    st.write("- Post jobs")
    st.write("- Review candidates")
    st.write("- Schedule interviews")

def display_fallback_recruiter_interface(current_step):
    """Fallback interface for recruiter"""
    st.header(f"💼 Recruiter - Step {current_step}")
    st.info("Fallback interface for recruiter")

def display_fallback_observer_view():
    """Fallback observer dashboard"""
    st.header("📊 Observer Dashboard")
    st.info("Welcome to the Observer Dashboard. This view provides an overview of all platform activities.")
    
    # Demo data
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


# ========== SIDEBAR FALLBACK FUNCTIONS ==========

# ========== SIDEBAR FALLBACK FUNCTIONS ==========

def display_basic_student_sidebar():
    """Basic student sidebar when workflow_manager is not available"""
    st.subheader("Student Workflow")
    current_step = st.session_state.workflows["student"]["current_step"]
    st.write(f"**Current Step:** {current_step}/8")
    
    steps = [
        "🎯 Profile Creation",
        "📝 Resume Building", 
        "📚 Skill Assessment",
        "🔍 Job Search",
        "📝 Application",
        "🎤 Interview Prep",
        "💼 Interview",
        "✅ Offer"
    ]
    
    for i, step in enumerate(steps, 1):
        status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
        st.write(f"{status} Step {i}: {step}")

def display_basic_college_sidebar():
    """Basic college sidebar when workflow_manager is not available"""
    st.subheader("College Admin Workflow")
    current_step = st.session_state.workflows["college"]["current_step"]
    st.write(f"**Current Step:** {current_step}/6")
    
    steps = [
        "📊 Dashboard",
        "👨‍🎓 Student Management",
        "🤝 Company Coordination",
        "📋 Job Postings",
        "📈 Placement Stats",
        "📄 Reports"
    ]
    
    for i, step in enumerate(steps, 1):
        status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
        st.write(f"{status} Step {i}: {step}")

def display_basic_recruiter_sidebar():
    """Basic recruiter sidebar when workflow_manager is not available"""
    st.subheader("Recruiter Workflow")
    current_step = st.session_state.workflows["recruiter"]["current_step"]
    st.write(f"**Current Step:** {current_step}/5")
    
    steps = [
        "🏢 Company Profile",
        "📝 Post Jobs",
        "📋 Review Applications",
        "📅 Schedule Interviews",
        "🎉 Make Offers"
    ]
    
    for i, step in enumerate(steps, 1):
        status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
        st.write(f"{status} Step {i}: {step}")

def display_basic_observer_sidebar():
    """Basic observer sidebar when workflow_manager is not available"""
    st.subheader("Observer Dashboard")
    st.write("📊 Monitor all platform activities")
    st.write("• Student placements")
    st.write("• Company interactions")
    st.write("• Placement statistics")

# ========== MODULE CREATION FUNCTIONS ==========

def create_minimal_modules():
    """Create minimal module files if they don't exist"""
    # ... rest of the function ...

# ========== MODULE CREATION FUNCTIONS ==========

def create_minimal_modules():
    """Create minimal module files if they don't exist"""
    import os
    
    # Check if modules directory exists
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    if not os.path.exists(modules_dir):
        os.makedirs(modules_dir)
    
    # Create __init__.py
    init_file = os.path.join(modules_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Modules package\n')
    
    # Create missing module files
    missing_modules = [k for k, v in modules_status.items() if not v]
    
    for module in missing_modules:
        if module == 'workflow_manager':
            create_minimal_workflow_manager_NO_BUTTONS()  # Use NO BUTTONS version
        elif module == 'student_flow':
            create_minimal_student_flow_NO_BUTTONS()  # Use NO BUTTONS version
        elif module == 'college_flow':
            create_minimal_college_flow()
        elif module == 'recruiter_flow':
            create_minimal_recruiter_flow()

def create_minimal_workflow_manager_NO_BUTTONS():
    """Create minimal workflow_manager.py WITHOUT navigation buttons"""
    import os
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    file_path = os.path.join(modules_dir, 'workflow_manager.py')
    
    content = '''
import streamlit as st

class WorkflowManager:
    def __init__(self):
        pass
    
    def display_student_workflow(self):
        """Display student workflow in sidebar - NO NAVIGATION BUTTONS"""
        st.subheader("Student Workflow")
        current_step = st.session_state.workflows["student"]["current_step"]
        st.write(f"**Current Step:** {current_step}/8")
        
        steps = [
            "Profile Creation",
            "Resume Building",
            "Skill Assessment",
            "Job Search",
            "Application",
            "Interview Prep",
            "Interview",
            "Offer"
        ]
        
        for i, step in enumerate(steps, 1):
            status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
            st.write(f"{status} Step {i}: {step}")
        
        # NO NAVIGATION BUTTONS HERE
    
    def display_college_workflow(self):
        """Display college workflow in sidebar - NO NAVIGATION BUTTONS"""
        st.subheader("College Admin Workflow")
        current_step = st.session_state.workflows["college"]["current_step"]
        st.write(f"**Current Step:** {current_step}/6")
        
        steps = [
            "Dashboard",
            "Student Management",
            "Company Coordination",
            "Job Postings",
            "Placement Stats",
            "Reports"
        ]
        
        for i, step in enumerate(steps, 1):
            status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
            st.write(f"{status} Step {i}: {step}")
    
    def display_recruiter_workflow(self):
        """Display recruiter workflow in sidebar - NO NAVIGATION BUTTONS"""
        st.subheader("Recruiter Workflow")
        current_step = st.session_state.workflows["recruiter"]["current_step"]
        st.write(f"**Current Step:** {current_step}/5")
        
        steps = [
            "Company Profile",
            "Post Jobs",
            "Review Applications",
            "Schedule Interviews",
            "Make Offers"
        ]
        
        for i, step in enumerate(steps, 1):
            status = "✅" if i < current_step else "▶️" if i == current_step else "⏳"
            st.write(f"{status} Step {i}: {step}")
    
    def display_observer_dashboard(self):
        """Display observer dashboard in sidebar"""
        st.subheader("Observer Dashboard")
        st.write("Monitor all platform activities")
    
    def display_observer_view(self):
        """Display observer view in main content"""
        st.header("📊 Platform Overview")
        st.write("Observer view content would go here")
'''
    
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created minimal workflow_manager.py (NO BUTTONS)")

def create_minimal_student_flow_NO_BUTTONS():
    """Create minimal student_flow.py WITH navigation buttons in display()"""
    import os
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    file_path = os.path.join(modules_dir, 'student_flow.py')
    
    content = '''
import streamlit as st

class StudentFlow:
    def __init__(self):
        self.current_step = 1
        self.db_manager = None
        self.demo_mode = True
    
    def set_database_manager(self, db_manager, demo_mode=False):
        self.db_manager = db_manager
        self.demo_mode = demo_mode
    
    def display(self):
        st.header("👨‍🎓 Student Placement Journey")
        st.info(f"Current Step: {self.current_step}")
        
        if self.current_step == 1:
            st.subheader("🎯 Profile Creation")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            department = st.selectbox("Department", ["Computer Science", "Electrical", "Mechanical", "Civil", "Chemical"])
            if st.button("Save Profile"):
                st.success("Profile saved (demo)")
        elif self.current_step == 2:
            st.subheader("📄 Resume Building")
            st.write("Build your resume here")
            skills = st.text_area("Skills (comma separated)")
            projects = st.text_area("Projects")
            if st.button("Save Resume"):
                st.success("Resume saved (demo)")
        elif self.current_step == 3:
            st.subheader("🧠 Skill Assessment")
            st.write("Take skill assessment tests")
            st.selectbox("Select Test", ["Programming", "Aptitude", "Technical", "Soft Skills"])
        elif self.current_step == 4:
            st.subheader("🔍 Job Search")
            st.write("Search for jobs")
        elif self.current_step == 5:
            st.subheader("📝 Application")
            st.write("Apply for jobs")
        elif self.current_step == 6:
            st.subheader("🎤 Interview Preparation")
            st.write("Prepare for interviews")
        elif self.current_step == 7:
            st.subheader("💼 Interview")
            st.write("Interview process")
        elif self.current_step == 8:
            st.subheader("🏆 Offer")
            st.write("Review and accept offers")
        else:
            st.write(f"Step {self.current_step} content would go here")
        
        # Navigation buttons INSIDE the display method
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Previous Step", key="student_nav_prev", disabled=(self.current_step <= 1)):
                if self.current_step > 1:
                    self.current_step -= 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["student"]["current_step"] = self.current_step
                    st.rerun()
        with col2:
            st.write(f"**Step {self.current_step} of 8**")
        with col3:
            if st.button("Next Step ▶", key="student_nav_next", disabled=(self.current_step >= 8)):
                if self.current_step < 8:
                    self.current_step += 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["student"]["current_step"] = self.current_step
                    st.rerun()
'''
    
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created minimal student_flow.py (WITH NAVIGATION)")

def create_minimal_college_flow():
    """Create minimal college_flow.py"""
    import os
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    file_path = os.path.join(modules_dir, 'college_flow.py')
    
    content = '''
import streamlit as st

class CollegeFlow:
    def __init__(self):
        self.current_step = 1
        self.db_manager = None
        self.demo_mode = True
    
    def set_database_manager(self, db_manager, demo_mode=False):
        self.db_manager = db_manager
        self.demo_mode = demo_mode
    
    def display(self):
        st.header("🏫 College Admin Dashboard")
        st.info(f"Current Step: {self.current_step}")
        
        if self.current_step == 1:
            st.subheader("📊 Dashboard Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", "1,250")
            with col2:
                st.metric("Placement %", "85%")
            with col3:
                st.metric("Active Companies", "45")
        elif self.current_step == 2:
            st.subheader("👨‍🎓 Student Management")
            st.write("Manage student records")
        elif self.current_step == 3:
            st.subheader("🤝 Company Coordination")
            st.write("Coordinate with companies")
        elif self.current_step == 4:
            st.subheader("📋 Job Postings")
            st.write("Manage job postings")
        elif self.current_step == 5:
            st.subheader("📈 Placement Statistics")
            st.write("View placement statistics")
        elif self.current_step == 6:
            st.subheader("📄 Reports")
            st.write("Generate reports")
        else:
            st.write(f"Step {self.current_step} content would go here")
        
        # Navigation buttons
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Previous Step", key="college_nav_prev", disabled=(self.current_step <= 1)):
                if self.current_step > 1:
                    self.current_step -= 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["college"]["current_step"] = self.current_step
                    st.rerun()
        with col2:
            st.write(f"**Step {self.current_step} of 6**")
        with col3:
            if st.button("Next Step ▶", key="college_nav_next", disabled=(self.current_step >= 6)):
                if self.current_step < 6:
                    self.current_step += 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["college"]["current_step"] = self.current_step
                    st.rerun()
'''
    
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created minimal college_flow.py")

def create_minimal_recruiter_flow():
    """Create minimal recruiter_flow.py"""
    import os
    modules_dir = os.path.join(os.path.dirname(__file__), 'modules')
    file_path = os.path.join(modules_dir, 'recruiter_flow.py')
    
    content = '''
import streamlit as st

class RecruiterFlow:
    def __init__(self):
        self.current_step = 1
        self.db_manager = None
        self.demo_mode = True
    
    def set_database_manager(self, db_manager, demo_mode=False):
        self.db_manager = db_manager
        self.demo_mode = demo_mode
    
    def display(self):
        st.header("💼 Recruiter Dashboard")
        st.info(f"Current Step: {self.current_step}")
        
        if self.current_step == 1:
            st.subheader("🏢 Company Profile")
            company_name = st.text_input("Company Name")
            industry = st.selectbox("Industry", ["IT", "Finance", "Manufacturing", "Healthcare", "Education"])
        elif self.current_step == 2:
            st.subheader("📝 Post Jobs")
            job_title = st.text_input("Job Title")
            job_description = st.text_area("Job Description")
        elif self.current_step == 3:
            st.subheader("📋 Review Applications")
            st.write("Review candidate applications")
        elif self.current_step == 4:
            st.subheader("📅 Schedule Interviews")
            st.write("Schedule interviews with candidates")
        elif self.current_step == 5:
            st.subheader("🎉 Make Offers")
            st.write("Make job offers to selected candidates")
        else:
            st.write(f"Step {self.current_step} content would go here")
        
        # Navigation buttons
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("◀ Previous Step", key="recruiter_nav_prev", disabled=(self.current_step <= 1)):
                if self.current_step > 1:
                    self.current_step -= 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["recruiter"]["current_step"] = self.current_step
                    st.rerun()
        with col2:
            st.write(f"**Step {self.current_step} of 5**")
        with col3:
            if st.button("Next Step ▶", key="recruiter_nav_next", disabled=(self.current_step >= 5)):
                if self.current_step < 5:
                    self.current_step += 1
                    # Update session state
                    if 'workflows' in st.session_state:
                        st.session_state.workflows["recruiter"]["current_step"] = self.current_step
                    st.rerun()
'''
    
    with open(file_path, 'w') as f:
        f.write(content)
    print(f"✅ Created minimal recruiter_flow.py")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python</p>
</div>
""", unsafe_allow_html=True)
