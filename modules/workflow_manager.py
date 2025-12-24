import streamlit as st
import pandas as pd

class WorkflowManager:
    def __init__(self):
        # Initialize workflows in session state if not exists
        if 'workflows' not in st.session_state:
            st.session_state.workflows = self.initialize_workflows()
        
        # Ensure current_step exists for each workflow
        for workflow_name in ['student', 'college', 'recruiter']:
            if f'current_step_{workflow_name}' not in st.session_state:
                st.session_state[f'current_step_{workflow_name}'] = 1
    
    def initialize_workflows(self):
        """Define all systematic workflows"""
        return {
            "student": {
                "name": "Student Placement Journey",
                "steps": [
                    {"id": 1, "name": "🎯 Profile Creation", "status": "pending"},
                    {"id": 2, "name": "📝 AI Resume Building", "status": "pending"},
                    {"id": 3, "name": "📚 NEP Course Planning", "status": "pending"},
                    {"id": 4, "name": "💼 PM Internship Match", "status": "pending"},
                    {"id": 5, "name": "🎯 Career Path Planning", "status": "pending"},
                    {"id": 6, "name": "📊 Placement Prediction", "status": "pending"},
                    {"id": 7, "name": "🤝 Interview Preparation", "status": "pending"},
                    {"id": 8, "name": "✅ Placement Tracking", "status": "pending"}
                ]
            },
            "college": {
                "name": "College Placement Management",
                "steps": [
                    {"id": 1, "name": "👨‍🎓 Student Database", "status": "pending"},
                    {"id": 2, "name": "📊 Analytics Dashboard", "status": "pending"},
                    {"id": 3, "name": "🏢 Company Registration", "status": "pending"},
                    {"id": 4, "name": "📅 Drive Scheduling", "status": "pending"},
                    {"id": 5, "name": "🎯 Student-Company Matching", "status": "pending"},
                    {"id": 6, "name": "📝 Interview Management", "status": "pending"},
                    {"id": 7, "name": "✅ Placement Records", "status": "pending"},
                    {"id": 8, "name": "📈 Performance Reports", "status": "pending"}
                ]
            },
            "recruiter": {
                "name": "Recruiter Hiring Process",
                "steps": [
                    {"id": 1, "name": "🏢 Company Profile", "status": "pending"},
                    {"id": 2, "name": "📋 Job Posting", "status": "pending"},
                    {"id": 3, "name": "🎯 Candidate Search", "status": "pending"},
                    {"id": 4, "name": "🤖 AI Screening", "status": "pending"},
                    {"id": 5, "name": "📅 Interview Scheduling", "status": "pending"},
                    {"id": 6, "name": "📊 Candidate Evaluation", "status": "pending"},
                    {"id": 7, "name": "✅ Offer Management", "status": "pending"},
                    {"id": 8, "name": "📈 Hiring Analytics", "status": "pending"}
                ]
            }
        }
    
    def display_student_workflow(self):
        """Display student workflow steps in sidebar"""
        st.subheader("👨‍🎓 Student Journey")
        
        # Get current step
        current_step = st.session_state.get('current_step_student', 1)
        steps = st.session_state.workflows["student"]["steps"]
        
        # Progress bar
        progress = current_step / len(steps)
        st.progress(progress)
        st.caption(f"Step {current_step} of {len(steps)}")
        
        # Display steps
        for step in steps:
            if step["id"] < current_step:
                status_icon = "✅"
            elif step["id"] == current_step:
                status_icon = "🔄"
            else:
                status_icon = "⏳"
            
            # Create clickable step
            if step["id"] <= current_step:
                if st.button(
                    f"{status_icon} Step {step['id']}: {step['name']}",
                    key=f"student_step_{step['id']}",
                    width='stretch',
                    type="primary" if step["id"] == current_step else "secondary"
                ):
                    st.session_state.current_step_student = step["id"]
                    st.rerun()
            else:
                st.button(
                    f"{status_icon} Step {step['id']}: {step['name']}",
                    key=f"student_step_{step['id']}",
                    width='stretch',
                    disabled=True
                )
        
        # Navigation buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1 and st.button("⬅️ Previous", key="student_prev", width='stretch'):
                st.session_state.current_step_student = current_step - 1
                st.rerun()
        with col2:
            if current_step < len(steps) and st.button("Next ➡️", key="student_next", width='stretch'):
                st.session_state.current_step_student = current_step + 1
                st.rerun()
    
    def display_college_workflow(self):
        """Display college admin workflow in sidebar"""
        st.subheader("🏫 College Management")
        
        # Get current step
        current_step = st.session_state.get('current_step_college', 1)
        steps = st.session_state.workflows["college"]["steps"]
        
        # Progress bar
        progress = current_step / len(steps)
        st.progress(progress)
        st.caption(f"Step {current_step} of {len(steps)}")
        
        # Display steps
        for step in steps:
            if step["id"] < current_step:
                status_icon = "✅"
            elif step["id"] == current_step:
                status_icon = "🔄"
            else:
                status_icon = "⏳"
            
            # Create clickable step
            if step["id"] <= current_step:
                if st.button(
                    f"{status_icon} Step {step['id']}: {step['name']}",
                    key=f"college_step_{step['id']}",
                    width='stretch',
                    type="primary" if step["id"] == current_step else "secondary"
                ):
                    st.session_state.current_step_college = step["id"]
                    st.rerun()
            else:
                st.button(
                    f"{status_icon} Step {step['id']}: {step['name']}",
                    key=f"college_step_{step['id']}",
                    width='stretch',
                    disabled=True
                )
        
        # Navigation buttons
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1 and st.button("⬅️ Previous", key="college_prev", width='stretch'):
                st.session_state.current_step_college = current_step - 1
                st.rerun()
        with col2:
            if current_step < len(steps) and st.button("Next ➡️", key="college_next", width='stretch'):
                st.session_state.current_step_college = current_step + 1
                st.rerun()
    
    def display_recruiter_workflow(self):
        """Display recruiter workflow in sidebar"""
        st.subheader("💼 Recruiter Portal")
        
        # Get current step
        current_step = st.session_state.get('current_step_recruiter', 1)
        steps = st.session_state.workflows["recruiter"]["steps"]
        
        # Display as a timeline
        for step in steps:
            if step["id"] < current_step:
                st.success(f"✅ {step['name']}")
            elif step["id"] == current_step:
                st.info(f"🔄 {step['name']}")
            else:
                st.info(f"⏳ {step['name']}")
    
    def display_observer_dashboard(self):
        """Dashboard for observers/judges"""
        st.subheader("👀 Platform Overview")
        st.info("Select a role to explore the systematic workflows")
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Modules", "24")
        with col2:
            st.metric("Workflows", "3")
        with col3:
            st.metric("AI Features", "8+")
    
    def display_observer_view(self):
        """Observer view of the entire system"""
        st.header("🌐 Complete System Overview")
        
        # Create tabs for each workflow
        tab1, tab2, tab3 = st.tabs(["👨‍🎓 Student", "🏫 College", "💼 Recruiter"])
        
        with tab1:
            st.subheader("Student Placement Journey")
            student_steps = st.session_state.workflows["student"]["steps"]
            for step in student_steps:
                st.write(f"**Step {step['id']}:** {step['name']}")
            
            # Student workflow visualization
            st.image("https://via.placeholder.com/800x200/4CAF50/FFFFFF?text=Student+Workflow+Visualization", 
                    caption="Student Placement Journey Workflow")
        
        with tab2:
            st.subheader("College Management Workflow")
            college_steps = st.session_state.workflows["college"]["steps"]
            for step in college_steps:
                st.write(f"**Step {step['id']}:** {step['name']}")
            
            # College workflow visualization
            st.image("https://via.placeholder.com/800x200/2196F3/FFFFFF?text=College+Management+Workflow", 
                    caption="College Placement Management Workflow")
        
        with tab3:
            st.subheader("Recruiter Hiring Process")
            recruiter_steps = st.session_state.workflows["recruiter"]["steps"]
            for step in recruiter_steps:
                st.write(f"**Step {step['id']}:** {step['name']}")
            
            # Recruiter workflow visualization
            st.image("https://via.placeholder.com/800x200/FF9800/FFFFFF?text=Recruiter+Hiring+Workflow", 
                    caption="Recruiter Hiring Process Workflow")
        
        # System statistics
        st.subheader("📊 System Statistics")
        
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        with metrics_col1:
            st.metric("Total Workflows", "3")
        with metrics_col2:
            st.metric("Process Steps", "24")
        with metrics_col3:
            st.metric("AI Modules", "8")
        with metrics_col4:
            st.metric("Integration Points", "15+")
