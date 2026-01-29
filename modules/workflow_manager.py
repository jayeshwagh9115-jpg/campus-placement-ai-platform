import streamlit as st
import pandas as pd

class WorkflowManager:
    def __init__(self):
        # Initialize workflows but sync with session state if available
        self.workflows = self.initialize_workflows()
        self.sync_with_session_state()
    
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
    
    def sync_with_session_state(self):
        """Sync workflows with session state if available"""
        if 'workflows' in st.session_state:
            # Update current steps from session state
            for role in ["student", "college", "recruiter"]:
                if role in st.session_state.workflows:
                    self.workflows[role]["current_step"] = st.session_state.workflows[role]["current_step"]
    
    def save_to_session_state(self):
        """Save current workflow state to session state"""
        if 'workflows' not in st.session_state:
            st.session_state.workflows = {}
        
        for role in ["student", "college", "recruiter"]:
            st.session_state.workflows[role] = {
                "current_step": self.workflows[role]["current_step"]
            }
    
    def get_current_step(self, role):
        """Get current step for a specific role"""
        if role in self.workflows:
            return self.workflows[role]["current_step"]
        return 1
    
    def set_current_step(self, role, step):
        """Set current step for a specific role"""
        if role in self.workflows and 1 <= step <= 8:
            self.workflows[role]["current_step"] = step
            # Also update session state
            self.save_to_session_state()
            return True
        return False
    
    def display_student_workflow(self):
        """Display student workflow steps - NO NAVIGATION BUTTONS"""
        st.subheader("📋 Student Placement Journey")
        
        workflow = self.workflows["student"]
        current_step = workflow["current_step"]
        
        # Progress bar
        progress = current_step / len(workflow["steps"])
        st.progress(progress)
        
        # Display current step info
        st.write(f"**Current Step:** {current_step}/8")
        
        # Display steps with status
        for step in workflow["steps"]:
            status_icon = "✅" if step["id"] < current_step else "🔄" if step["id"] == current_step else "⏳"
            status_color = "green" if step["id"] < current_step else "blue" if step["id"] == current_step else "gray"
            
            if step["id"] == current_step:
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 10px; margin: 10px 0; background-color: #f0f8ff;">
                    <b>{status_icon} Step {step['id']}: {step['name']}</b>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="border-left: 4px solid {status_color}; padding-left: 10px; margin: 10px 0;">
                    {status_icon} Step {step['id']}: {step['name']}
                </div>
                """, unsafe_allow_html=True)
        
        # NO NAVIGATION BUTTONS HERE - They are handled in main app
        
        # Save to session state
        self.save_to_session_state()
    
    def display_college_workflow(self):
        """Display college admin workflow - NO NAVIGATION BUTTONS"""
        st.subheader("🏫 College Placement Management")
        
        workflow = self.workflows["college"]
        current_step = workflow["current_step"]
        
        # Display current step info
        st.write(f"**Current Step:** {current_step}/8")
        
        # Display as a timeline
        for step in workflow["steps"]:
            if step["id"] == current_step:
                st.success(f"🔄 **Step {step['id']}: {step['name']}**")
            elif step["id"] < current_step:
                st.write(f"✅ Step {step['id']}: {step['name']}")
            else:
                st.info(f"⏳ Step {step['id']}: {step['name']}")
        
        # NO NAVIGATION BUTTONS HERE - They are handled in main app
        
        # Save to session state
        self.save_to_session_state()
    
    def display_recruiter_workflow(self):
        """Display recruiter workflow - NO NAVIGATION BUTTONS"""
        st.subheader("💼 Recruiter Hiring Process")
        
        workflow = self.workflows["recruiter"]
        current_step = workflow["current_step"]
        
        # Display current step info
        st.write(f"**Current Step:** {current_step}/8")
        
        # Simple list display instead of visual timeline (to avoid complex HTML)
        for step in workflow["steps"]:
            if step["id"] == current_step:
                st.markdown(f"**🔄 Step {step['id']}: {step['name']}**")
            elif step["id"] < current_step:
                st.markdown(f"✅ Step {step['id']}: {step['name']}")
            else:
                st.markdown(f"⏳ Step {step['id']}: {step['name']}")
        
        # NO NAVIGATION BUTTONS HERE - They are handled in main app
        
        # Save to session state
        self.save_to_session_state()
    
    def display_observer_dashboard(self):
        """Dashboard for observers/judges - NO NAVIGATION BUTTONS"""
        st.subheader("👀 Platform Overview")
        st.info("Monitor platform workflows - Use main content for navigation")
        
        # Show quick stats for all workflows
        col1, col2, col3 = st.columns(3)
        with col1:
            current_step = self.workflows['student']['current_step']
            st.metric("Student Progress", 
                     f"Step {current_step}/8",
                     f"{current_step*12.5}%")
        with col2:
            current_step = self.workflows['college']['current_step']
            st.metric("College Progress", 
                     f"Step {current_step}/8",
                     f"{current_step*12.5}%")
        with col3:
            current_step = self.workflows['recruiter']['current_step']
            st.metric("Recruiter Progress", 
                     f"Step {current_step}/8",
                     f"{current_step*12.5}%")
        
        # Quick navigation note
        st.caption("💡 Navigation buttons are in the main content area")
    
    def display_observer_view(self):
        """Observer view of the entire system"""
        st.header("🌐 Complete System Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("👨‍🎓 Student Journey")
            student_steps = self.workflows["student"]["steps"]
            current_student_step = self.workflows["student"]["current_step"]
            
            for step in student_steps:
                status = "✅" if step["id"] < current_student_step else "🔄" if step["id"] == current_student_step else "⏳"
                st.write(f"{status} **Step {step['id']}:** {step['name']}")
        
        with col2:
            st.subheader("🏫 College Process")
            college_steps = self.workflows["college"]["steps"]
            current_college_step = self.workflows["college"]["current_step"]
            
            for step in college_steps:
                status = "✅" if step["id"] < current_college_step else "🔄" if step["id"] == current_college_step else "⏳"
                st.write(f"{status} **Step {step['id']}:** {step['name']}")
        
        with col3:
            st.subheader("💼 Recruiter Flow")
            recruiter_steps = self.workflows["recruiter"]["steps"]
            current_recruiter_step = self.workflows["recruiter"]["current_step"]
            
            for step in recruiter_steps:
                status = "✅" if step["id"] < current_recruiter_step else "🔄" if step["id"] == current_recruiter_step else "⏳"
                st.write(f"{status} **Step {step['id']}:** {step['name']}")
        
        # System statistics
        st.subheader("📊 System Statistics")
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        with metrics_col1:
            st.metric("Total Workflows", "3")
        with metrics_col2:
            total_steps = 0
            for workflow in self.workflows.values():
                total_steps += len(workflow["steps"])
            st.metric("Process Steps", total_steps)
        with metrics_col3:
            st.metric("Active Users", "1,250")
        with metrics_col4:
            st.metric("Success Rate", "92%")
        
        # Add reset button for judges
        st.divider()
        if st.button("🔄 Reset All Workflows", key="observer_reset_all"):
            self.workflows["student"]["current_step"] = 1
            self.workflows["college"]["current_step"] = 1
            self.workflows["recruiter"]["current_step"] = 1
            self.save_to_session_state()
            st.success("All workflows reset to Step 1!")
            st.rerun()
