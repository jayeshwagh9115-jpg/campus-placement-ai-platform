import streamlit as st
import pandas as pd

class WorkflowManager:
    def __init__(self):
        # Initialize workflows only once
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state for workflows"""
        if 'workflows_initialized' not in st.session_state:
            st.session_state.workflows = self.initialize_workflows()
            st.session_state.workflows_initialized = True
    
    def initialize_workflows(self):
        """Define all systematic workflows"""
        return {
            "student": {
                "steps": [
                    {"id": 1, "name": "🎯 Profile Creation", "status": "pending"},
                    {"id": 2, "name": "📝 AI Resume Building", "status": "pending"},
                    {"id": 3, "name": "📚 NEP Course Planning", "status": "pending"},
                    {"id": 4, "name": "💼 PM Internship Match", "status": "pending"},
                    {"id": 5, "name": "🎯 Career Path Planning", "status": "pending"},
                    {"id": 6, "name": "📊 Placement Prediction", "status": "pending"},
                    {"id": 7, "name": "🤝 Interview Preparation", "status": "pending"},
                    {"id": 8, "name": "✅ Placement Tracking", "status": "pending"}
                ],
                "current_step": 1
            },
            "college": {
                "steps": [
                    {"id": 1, "name": "👨‍🎓 Student Database", "status": "pending"},
                    {"id": 2, "name": "📊 Analytics Dashboard", "status": "pending"},
                    {"id": 3, "name": "🏢 Company Registration", "status": "pending"},
                    {"id": 4, "name": "📅 Drive Scheduling", "status": "pending"},
                    {"id": 5, "name": "🎯 Student-Company Matching", "status": "pending"},
                    {"id": 6, "name": "📝 Interview Management", "status": "pending"},
                    {"id": 7, "name": "✅ Placement Records", "status": "pending"},
                    {"id": 8, "name": "📈 Performance Reports", "status": "pending"}
                ],
                "current_step": 1
            },
            "recruiter": {
                "steps": [
                    {"id": 1, "name": "🏢 Company Profile", "status": "pending"},
                    {"id": 2, "name": "📋 Job Posting", "status": "pending"},
                    {"id": 3, "name": "🎯 Candidate Search", "status": "pending"},
                    {"id": 4, "name": "🤖 AI Screening", "status": "pending"},
                    {"id": 5, "name": "📅 Interview Scheduling", "status": "pending"},
                    {"id": 6, "name": "📊 Candidate Evaluation", "status": "pending"},
                    {"id": 7, "name": "✅ Offer Management", "status": "pending"},
                    {"id": 8, "name": "📈 Hiring Analytics", "status": "pending"}
                ],
                "current_step": 1
            }
        }
    
    def display_student_workflow(self):
        """Display student workflow steps"""
        st.subheader("📋 Student Placement Journey")
        
        workflow = st.session_state.workflows["student"]
        current_step = workflow["current_step"]
        
        # Progress bar
        progress = current_step / len(workflow["steps"])
        st.progress(progress)
        
        # Display steps with proper status indicators
        for step in workflow["steps"]:
            # Determine status based on current step
            if step["id"] < current_step:
                status_icon = "✅"
                status_color = "green"
            elif step["id"] == current_step:
                status_icon = "🔄"
                status_color = "blue"
            else:
                status_icon = "⏳"
                status_color = "gray"
            
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color}; padding-left: 10px; margin: 10px 0;">
                <b>{status_icon} Step {step['id']}: {step['name']}</b>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="prev_student"):
                    # Update session state
                    st.session_state.workflows["student"]["current_step"] -= 1
                    st.rerun()
        
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_student"):
                    # Update session state
                    st.session_state.workflows["student"]["current_step"] += 1
                    st.rerun()
    
    def display_college_workflow(self):
        """Display college admin workflow"""
        st.subheader("🏫 College Placement Management")
        
        workflow = st.session_state.workflows["college"]
        current_step = workflow["current_step"]
        
        # Display as a timeline
        for step in workflow["steps"]:
            if step["id"] < current_step:
                st.success(f"✅ {step['name']}")
            elif step["id"] == current_step:
                st.warning(f"🔄 {step['name']} (Current)")
            else:
                st.info(f"⏳ {step['name']}")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="prev_college"):
                    st.session_state.workflows["college"]["current_step"] -= 1
                    st.rerun()
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_college"):
                    st.session_state.workflows["college"]["current_step"] += 1
                    st.rerun()
    
    def display_recruiter_workflow(self):
        """Display recruiter workflow"""
        st.subheader("💼 Recruiter Hiring Process")
        
        workflow = st.session_state.workflows["recruiter"]
        current_step = workflow["current_step"]
        
        # Visual timeline
        cols = st.columns(len(workflow["steps"]))
        for idx, step in enumerate(workflow["steps"]):
            with cols[idx]:
                if step["id"] < current_step:
                    st.markdown(f"<div style='background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; text-align: center;'><b>✅ {step['id']}</b><br>{step['name'].split()[0]}</div>", unsafe_allow_html=True)
                elif step["id"] == current_step:
                    st.markdown(f"<div style='background-color: #2196F3; color: white; padding: 10px; border-radius: 5px; text-align: center;'><b>🔄 {step['id']}</b><br>{step['name'].split()[0]}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background-color: #e0e0e0; padding: 10px; border-radius: 5px; text-align: center;'><b>⏳ {step['id']}</b><br>{step['name'].split()[0]}</div>", unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="prev_recruiter"):
                    st.session_state.workflows["recruiter"]["current_step"] -= 1
                    st.rerun()
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_recruiter"):
                    st.session_state.workflows["recruiter"]["current_step"] += 1
                    st.rerun()
    
    def display_observer_dashboard(self):
        """Dashboard for observers/judges"""
        st.subheader("👀 Platform Overview")
        st.info("Select a role to explore the systematic workflows")
    
    def display_observer_view(self):
        """Observer view of the entire system"""
        st.header("🌐 Complete System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👨‍🎓 Student Journey")
            student_steps = st.session_state.workflows["student"]["steps"]
            student_current = st.session_state.workflows["student"]["current_step"]
            for step in student_steps:
                if step["id"] <= student_current:
                    st.write(f"✅ {step['name']}")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col2:
            st.subheader("🏫 College Process")
            college_steps = st.session_state.workflows["college"]["steps"]
            college_current = st.session_state.workflows["college"]["current_step"]
            for step in college_steps:
                if step["id"] <= college_current:
                    st.write(f"✅ {step['name']}")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col3:
            st.subheader("💼 Recruiter Flow")
            recruiter_steps = st.session_state.workflows["recruiter"]["steps"]
            recruiter_current = st.session_state.workflows["recruiter"]["current_step"]
            for step in recruiter_steps:
                if step["id"] <= recruiter_current:
                    st.write(f"✅ {step['name']}")
                else:
                    st.write(f"⏳ {step['name']}")
        
        # System statistics
        st.subheader("📊 System Statistics")
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        with metrics_col1:
            st.metric("Total Workflows", "3")
        with metrics_col2:
            st.metric("Process Steps", "24")
        with metrics_col3:
            st.metric("Active Users", "1,250")
        with metrics_col4:
            st.metric("Success Rate", "92%")


# Helper function to test the workflow
def test_workflow():
    """Test function to ensure workflow works properly"""
    st.title("Workflow Manager Test")
    
    # Create workflow manager instance
    wm = WorkflowManager()
    
    # Role selection
    role = st.radio("Select Role:", ["Student", "College", "Recruiter", "Observer"], horizontal=True)
    
    # Display appropriate workflow
    if role == "Student":
        wm.display_student_workflow()
    elif role == "College":
        wm.display_college_workflow()
    elif role == "Recruiter":
        wm.display_recruiter_workflow()
    else:
        wm.display_observer_view()
    
    # Add reset button
    if st.button("Reset All Workflows", key="reset_all"):
        if 'workflows_initialized' in st.session_state:
            del st.session_state.workflows_initialized
        if 'workflows' in st.session_state:
            del st.session_state.workflows
        st.rerun()


# To test this, run this file directly
if __name__ == "__main__":
    test_workflow()
