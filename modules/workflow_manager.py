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
