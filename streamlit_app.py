# streamlit_app.py - REDESIGNED WITH WORKFLOW
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from modules.workflow_manager import WorkflowManager
from modules.student_flow import StudentFlow
from modules.college_flow import CollegeFlow
from modules.recruiter_flow import RecruiterFlow
import os

# Page configuration
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# Sidebar for workflow selection
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Workflow Selection")
    
    # Select user role
    user_role = st.radio(
        "Select Your Role:",
        ["👨‍🎓 Student", "🏫 College Admin", "💼 Recruiter", "👀 Observer"],
        key="user_role"
    )
    
    # Show workflow based on role
    if user_role == "👨‍🎓 Student":
        workflow.display_student_workflow()
    elif user_role == "🏫 College Admin":
        workflow.display_college_workflow()
    elif user_role == "💼 Recruiter":
        workflow.display_recruiter_workflow()
    else:
        workflow.display_observer_dashboard()

# Main content area - Show selected workflow
if user_role == "👨‍🎓 Student":
    st.session_state.student_flow.display()
elif user_role == "🏫 College Admin":
    st.session_state.college_flow.display()
elif user_role == "💼 Recruiter":
    st.session_state.recruiter_flow.display()
else:
    workflow.display_observer_view()

# Footer
st.divider()
st.caption("🎓 AI Campus Placement Platform | Systematic Workflow Design | National Level Hackathon")
