import streamlit as st
import pandas as pd

class WorkflowManager:
    def __init__(self):
        # Initialize workflows in session state
        if 'workflows' not in st.session_state:
            self._initialize_workflows()
    
    def _initialize_workflows(self):
        """Define all systematic workflows"""
        st.session_state.workflows = {
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
    
    def _update_step(self, role, direction):
        """Update step for a specific role"""
        if direction == "next":
            st.session_state.workflows[role]["current_step"] += 1
        elif direction == "prev":
            st.session_state.workflows[role]["current_step"] -= 1
        st.rerun()
    
    def display_student_workflow(self):
        """Display student workflow steps"""
        st.subheader("📋 Student Placement Journey")
        
        workflow = st.session_state.workflows["student"]
        current_step = workflow["current_step"]
        
        # Progress bar
        progress = current_step / len(workflow["steps"])
        st.progress(progress)
        
        # Display steps
        for step in workflow["steps"]:
            status_icon = "✅" if step["id"] < current_step else "🔄" if step["id"] == current_step else "⏳"
            status_color = "green" if step["id"] < current_step else "blue" if step["id"] == current_step else "gray"
            
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color}; padding-left: 10px; margin: 10px 0;">
                <b>{status_icon} Step {step['id']}: {step['name']}</b>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation with callback functions
        col1, col2 = st.columns(2)
        
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="prev_student_btn"):
                    self._update_step("student", "prev")
        
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_student_btn"):
                    self._update_step("student", "next")
    
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
                if st.button("⬅️ Previous Step", key="prev_college_btn"):
                    self._update_step("college", "prev")
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_college_btn"):
                    self._update_step("college", "next")
    
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
                    st.markdown(f"""
                    <div style='background-color: #4CAF50; color: white; padding: 10px; 
                    border-radius: 5px; text-align: center;'>
                        <b>✅ {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
                elif step["id"] == current_step:
                    st.markdown(f"""
                    <div style='background-color: #2196F3; color: white; padding: 10px; 
                    border-radius: 5px; text-align: center;'>
                        <b>🔄 {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background-color: #e0e0e0; padding: 10px; 
                    border-radius: 5px; text-align: center;'>
                        <b>⏳ {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="prev_recruiter_btn"):
                    self._update_step("recruiter", "prev")
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="next_recruiter_btn"):
                    self._update_step("recruiter", "next")
    
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
            student_workflow = st.session_state.workflows["student"]
            student_current = student_workflow["current_step"]
            for step in student_workflow["steps"]:
                if step["id"] < student_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == student_current:
                    st.write(f"🔄 {step['name']} (Current)")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col2:
            st.subheader("🏫 College Process")
            college_workflow = st.session_state.workflows["college"]
            college_current = college_workflow["current_step"]
            for step in college_workflow["steps"]:
                if step["id"] < college_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == college_current:
                    st.write(f"🔄 {step['name']} (Current)")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col3:
            st.subheader("💼 Recruiter Flow")
            recruiter_workflow = st.session_state.workflows["recruiter"]
            recruiter_current = recruiter_workflow["current_step"]
            for step in recruiter_workflow["steps"]:
                if step["id"] < recruiter_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == recruiter_current:
                    st.write(f"🔄 {step['name']} (Current)")
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


# TEST FUNCTION - Use this to test the workflow
def test_workflow_app():
    """Test the workflow functionality"""
    st.set_page_config(layout="wide")
    st.title("🚀 Placement Platform Workflow Manager")
    
    # Initialize workflow manager
    wm = WorkflowManager()
    
    # Sidebar for navigation
    st.sidebar.header("Navigation")
    selected_role = st.sidebar.radio(
        "Select Role to View:",
        ["Student", "College", "Recruiter", "Observer"],
        index=0
    )
    
    # Reset button in sidebar
    if st.sidebar.button("🔄 Reset All Workflows"):
        if 'workflows' in st.session_state:
            del st.session_state.workflows
        st.rerun()
    
    # Display current step info
    st.sidebar.subheader("Current Status")
    if 'workflows' in st.session_state:
        for role, data in st.session_state.workflows.items():
            st.sidebar.write(f"**{role.title()}**: Step {data['current_step']} of {len(data['steps'])}")
    
    # Main content area
    if selected_role == "Student":
        wm.display_student_workflow()
    elif selected_role == "College":
        wm.display_college_workflow()
    elif selected_role == "Recruiter":
        wm.display_recruiter_workflow()
    else:
        wm.display_observer_view()
    
    # Debug information (optional)
    with st.expander("Debug Info"):
        st.write("Session state:", st.session_state)
        if 'workflows' in st.session_state:
            st.write("Workflows data:", st.session_state.workflows)


# Run the test app if this file is executed directly
if __name__ == "__main__":
    test_workflow_app()
