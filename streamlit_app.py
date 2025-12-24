import streamlit as st
import pandas as pd
import numpy as np
from modules.student_info import StudentInfoModule
from modules.college_info import CollegeInfoModule
from modules.placement_module import PlacementModule
from modules.ai_resume_builder import AIResumeBuilder
from modules.pm_internship_ai import PMInternshipAI
from modules.nep_advisor import NEPAdvisor
from modules.career_advisor import CareerAdvisor
from modules.chatbot import IntegratedChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False

# Function definitions (moved to top)
def display_dashboard():
    """Display main dashboard with analytics"""
    st.header("📈 Platform Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", "1,250", "+12%")
    with col2:
        st.metric("Placement Rate", "85%", "+5%")
    with col3:
        st.metric("Active Companies", "45", "+3")
    with col4:
        st.metric("AI Recommendations", "2,340", "+120")
    
    # Recent activities
    st.subheader("Recent Activities")
    activities = pd.DataFrame({
        'Time': ['2h ago', '4h ago', '6h ago', '1d ago'],
        'Activity': [
            'AI resume analysis completed for 15 students',
            'Placement prediction model updated',
            'New company registration: TechCorp Inc.',
            'Career counseling session conducted'
        ],
        'Status': ['✅', '🔄', '✅', '✅']
    })
    st.dataframe(activities, use_container_width=True)
    
    # Quick actions
    st.subheader("Quick Actions")
    quick_col1, quick_col2, quick_col3 = st.columns(3)
    with quick_col1:
        if st.button("🚀 Build Resume", use_container_width=True):
            st.session_state.selected_module = "📝 AI Resume Builder"
            st.rerun()
    with quick_col2:
        if st.button("🎯 Career Advice", use_container_width=True):
            st.session_state.selected_module = "🎯 Career Advisor"
            st.rerun()
    with quick_col3:
        if st.button("🤖 Ask Chatbot", use_container_width=True):
            st.session_state.selected_module = "🤖 Integrated Chatbot"
            st.rerun()

# Title and description
st.title("🎓 AI-Powered Campus Placement Management System")
st.markdown("""
### National Level Hackathon Project
An intelligent platform connecting students, colleges, and recruiters with AI-powered tools.
""")

# Sidebar for navigation and authentication
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Navigation")
    
    # Demo mode toggle
    demo_col1, demo_col2 = st.columns([2, 1])
    with demo_col1:
        st.caption("Try without login")
    with demo_col2:
        if st.button("🎮 Demo"):
            st.session_state.demo_mode = True
            st.session_state.authenticated = True
            st.session_state.user_role = "student"
            st.rerun()
    
    if st.session_state.demo_mode:
        st.success("Demo Mode Active")
        if st.button("Exit Demo"):
            st.session_state.demo_mode = False
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.rerun()
    
    # User authentication (simplified for hackathon)
    if not st.session_state.authenticated:
        st.subheader("Login")
        role = st.selectbox("Select Role", ["Student", "College Admin", "Recruiter", "TPO"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Simplified authentication for hackathon
            if username and password:
                st.session_state.authenticated = True
                st.session_state.user_role = role.lower()
                st.rerun()
    
    # Navigation menu
    if st.session_state.authenticated:
        # Initialize selected_module in session state
        if 'selected_module' not in st.session_state:
            st.session_state.selected_module = "🏠 Dashboard"
        
        st.subheader("Modules")
        module = st.radio(
            "Select Module",
            [
                "🏠 Dashboard",
                "👨‍🎓 Student Information",
                "🏫 College Information",
                "📊 Campus Placement",
                "📝 AI Resume Builder",
                "💼 PM Internship AI",
                "📚 NEP Advisor",
                "🎯 Career Advisor",
                "🤖 Integrated Chatbot"
            ],
            key="module_selector"
        )
        
        # Update selected module
        st.session_state.selected_module = module
        
        # User info display
        st.divider()
        st.caption(f"Logged in as: {st.session_state.user_role.title()}")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.demo_mode = False
            st.session_state.selected_module = "🏠 Dashboard"
            st.rerun()

# Main content area
if not st.session_state.authenticated:
    st.info("👈 Please login from the sidebar to access the platform")
    
    # Show platform features
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🎯 AI-Powered")
        st.write("Intelligent resume building and career suggestions")
    with col2:
        st.markdown("### 📊 Data-Driven")
        st.write("Predictive analytics for placement success")
    with col3:
        st.markdown("### 🤖 Integrated")
        st.write("Seamless chatbot assistance throughout")
    
    st.divider()
    st.markdown("""
    ### Platform Features
    1. **Student Information Management** - Complete student profiles with academic records
    2. **College Information System** - College data and placement statistics
    3. **AI Resume Builder** - Intelligent resume creation and optimization 
    4. **PM Internship AI** - Product Management internship recommendations
    5. **NEP-Aligned Advisor** - Major/Minor suggestions per NEP guidelines
    6. **Career Advisor** - Personalized career path recommendations 
    7. **Integrated Chatbot** - 24/7 AI assistance for all queries
    """)
    
else:
    # Initialize modules
    student_module = StudentInfoModule()
    college_module = CollegeInfoModule()
    placement_module = PlacementModule()
    resume_builder = AIResumeBuilder()
    pm_internship = PMInternshipAI()
    nep_advisor = NEPAdvisor()
    career_advisor = CareerAdvisor()
    chatbot = IntegratedChatbot()
    
    # Get selected module from session state
    module = st.session_state.selected_module
    
    # Route to selected module
    if module == "🏠 Dashboard":
        display_dashboard()
    elif module == "👨‍🎓 Student Information":
        student_module.display()
    elif module == "🏫 College Information":
        college_module.display()
    elif module == "📊 Campus Placement":
        placement_module.display()
    elif module == "📝 AI Resume Builder":
        resume_builder.display()
    elif module == "💼 PM Internship AI":
        pm_internship.display()
    elif module == "📚 NEP Advisor":
        nep_advisor.display()
    elif module == "🎯 Career Advisor":
        career_advisor.display()
    elif module == "🤖 Integrated Chatbot":
        chatbot.display()

if __name__ == "__main__":
    # Add footer
    st.divider()
    st.caption("""
    🎓 AI Campus Placement Platform | National Level Hackathon Project | 
    Built with Streamlit & Python | 
    """)
