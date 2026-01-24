import streamlit as st

class WorkflowManager:
    def __init__(self):
        # Initialize workflows in session state if they don't exist
        if 'workflows' not in st.session_state:
            st.session_state.workflows = self.initialize_workflows()
        
        # Store button callbacks in session state
        if 'workflow_callbacks' not in st.session_state:
            st.session_state.workflow_callbacks = {}
    
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
    
    def update_student_step(self, direction):
        """Update student workflow step"""
        if direction == "next":
            if st.session_state.workflows["student"]["current_step"] < len(st.session_state.workflows["student"]["steps"]):
                st.session_state.workflows["student"]["current_step"] += 1
        elif direction == "prev":
            if st.session_state.workflows["student"]["current_step"] > 1:
                st.session_state.workflows["student"]["current_step"] -= 1
    
    def update_college_step(self, direction):
        """Update college workflow step"""
        if direction == "next":
            if st.session_state.workflows["college"]["current_step"] < len(st.session_state.workflows["college"]["steps"]):
                st.session_state.workflows["college"]["current_step"] += 1
        elif direction == "prev":
            if st.session_state.workflows["college"]["current_step"] > 1:
                st.session_state.workflows["college"]["current_step"] -= 1
    
    def update_recruiter_step(self, direction):
        """Update recruiter workflow step"""
        if direction == "next":
            if st.session_state.workflows["recruiter"]["current_step"] < len(st.session_state.workflows["recruiter"]["steps"]):
                st.session_state.workflows["recruiter"]["current_step"] += 1
        elif direction == "prev":
            if st.session_state.workflows["recruiter"]["current_step"] > 1:
                st.session_state.workflows["recruiter"]["current_step"] -= 1
    
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
        
        # Navigation - Using columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            # Previous button
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="student_prev", 
                           disabled=(current_step <= 1),
                           use_container_width=True):
                    self.update_student_step("prev")
                    st.rerun()
            else:
                st.button("⬅️ Previous Step", key="student_prev_disabled", 
                         disabled=True, use_container_width=True)
        
        with col2:
            # Next button
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="student_next",
                           disabled=(current_step >= len(workflow["steps"])),
                           use_container_width=True):
                    self.update_student_step("next")
                    st.rerun()
            else:
                st.button("Next Step ➡️", key="student_next_disabled", 
                         disabled=True, use_container_width=True)
        
        # Step indicator
        st.caption(f"**Current Step: {current_step} of {len(workflow['steps'])}**")
    
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
                st.warning(f"🔄 {step['name']}")
            else:
                st.info(f"⏳ {step['name']}")
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="college_prev",
                           use_container_width=True):
                    self.update_college_step("prev")
                    st.rerun()
            else:
                st.button("⬅️ Previous Step", key="college_prev_disabled",
                         disabled=True, use_container_width=True)
        
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="college_next",
                           use_container_width=True):
                    self.update_college_step("next")
                    st.rerun()
            else:
                st.button("Next Step ➡️", key="college_next_disabled",
                         disabled=True, use_container_width=True)
        
        # Step indicator
        st.caption(f"**Current Step: {current_step} of {len(workflow['steps'])}**")
    
    def display_recruiter_workflow(self):
        """Display recruiter workflow"""
        st.subheader("💼 Recruiter Hiring Process")
        
        workflow = st.session_state.workflows["recruiter"]
        current_step = workflow["current_step"]
        
        # Visual timeline - use tabs for better mobile view
        tab_cols = st.columns(len(workflow["steps"]))
        for idx, step in enumerate(workflow["steps"]):
            with tab_cols[idx]:
                if step["id"] < current_step:
                    st.markdown(f"""
                    <div style='background-color: #4CAF50; color: white; padding: 8px; 
                    border-radius: 5px; text-align: center; margin: 2px; font-size: 12px;'>
                        <b>✅ {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
                elif step["id"] == current_step:
                    st.markdown(f"""
                    <div style='background-color: #2196F3; color: white; padding: 8px; 
                    border-radius: 5px; text-align: center; margin: 2px; font-size: 12px;'>
                        <b>🔄 {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background-color: #e0e0e0; padding: 8px; 
                    border-radius: 5px; text-align: center; margin: 2px; font-size: 12px;'>
                        <b>⏳ {step['id']}</b><br>
                        {step['name'].split()[0]}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2 = st.columns(2)
        
        with col1:
            if current_step > 1:
                if st.button("⬅️ Previous Step", key="recruiter_prev",
                           use_container_width=True):
                    self.update_recruiter_step("prev")
                    st.rerun()
            else:
                st.button("⬅️ Previous Step", key="recruiter_prev_disabled",
                         disabled=True, use_container_width=True)
        
        with col2:
            if current_step < len(workflow["steps"]):
                if st.button("Next Step ➡️", key="recruiter_next",
                           use_container_width=True):
                    self.update_recruiter_step("next")
                    st.rerun()
            else:
                st.button("Next Step ➡️", key="recruiter_next_disabled",
                         disabled=True, use_container_width=True)
        
        # Step indicator
        st.caption(f"**Current Step: {current_step} of {len(workflow['steps'])}**")
    
    def display_observer_dashboard(self):
        """Dashboard for observers/judges"""
        st.subheader("👀 Platform Overview")
        st.info("Select a role to explore the systematic workflows")
        
        # Show all workflows
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👨‍🎓 Student")
            student_flow = st.session_state.workflows["student"]
            st.write(f"**Step:** {student_flow['current_step']}/8")
            st.progress(student_flow['current_step']/8)
        
        with col2:
            st.subheader("🏫 College")
            college_flow = st.session_state.workflows["college"]
            st.write(f"**Step:** {college_flow['current_step']}/8")
            st.progress(college_flow['current_step']/8)
        
        with col3:
            st.subheader("💼 Recruiter")
            recruiter_flow = st.session_state.workflows["recruiter"]
            st.write(f"**Step:** {recruiter_flow['current_step']}/8")
            st.progress(recruiter_flow['current_step']/8)
        
        # Reset all button
        if st.button("🔄 Reset All Workflows", key="reset_all_workflows"):
            st.session_state.workflows["student"]["current_step"] = 1
            st.session_state.workflows["college"]["current_step"] = 1
            st.session_state.workflows["recruiter"]["current_step"] = 1
            st.rerun()
    
    def display_observer_view(self):
        """Observer view of the entire system"""
        st.header("🌐 Complete System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👨‍🎓 Student Journey")
            student_steps = st.session_state.workflows["student"]["steps"]
            student_current = st.session_state.workflows["student"]["current_step"]
            for step in student_steps:
                if step["id"] < student_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == student_current:
                    st.write(f"🔄 **{step['name']}** (Current)")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col2:
            st.subheader("🏫 College Process")
            college_steps = st.session_state.workflows["college"]["steps"]
            college_current = st.session_state.workflows["college"]["current_step"]
            for step in college_steps:
                if step["id"] < college_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == college_current:
                    st.write(f"🔄 **{step['name']}** (Current)")
                else:
                    st.write(f"⏳ {step['name']}")
        
        with col3:
            st.subheader("💼 Recruiter Flow")
            recruiter_steps = st.session_state.workflows["recruiter"]["steps"]
            recruiter_current = st.session_state.workflows["recruiter"]["current_step"]
            for step in recruiter_steps:
                if step["id"] < recruiter_current:
                    st.write(f"✅ {step['name']}")
                elif step["id"] == recruiter_current:
                    st.write(f"🔄 **{step['name']}** (Current)")
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


# Test function to verify it works
if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Workflow Test")
    st.title("🧪 Workflow Manager Test")
    
    # Initialize workflow manager
    wm = WorkflowManager()
    
    # Role selection
    role = st.radio("Select Role:", ["Student", "College", "Recruiter", "Observer"], 
                   horizontal=True, index=0)
    
    # Display the selected workflow
    if role == "Student":
        wm.display_student_workflow()
    elif role == "College":
        wm.display_college_workflow()
    elif role == "Recruiter":
        wm.display_recruiter_workflow()
    else:
        wm.display_observer_view()
    
    # Show debug info
    with st.expander("Debug Info"):
        st.write("Session State Workflows:", st.session_state.workflows)
        st.write("Student Current Step:", st.session_state.workflows["student"]["current_step"])
        st.write("College Current Step:", st.session_state.workflows["college"]["current_step"])
        st.write("Recruiter Current Step:", st.session_state.workflows["recruiter"]["current_step"])
