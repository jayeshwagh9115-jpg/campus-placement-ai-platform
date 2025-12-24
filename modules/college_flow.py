def display(self):
    """Display complete college admin workflow"""
    st.header("🏫 College Placement Management System")
    
    # Get current step from session state
    current_step = st.session_state.get('current_step_college', 1)
    self.current_step = current_step
    
    # Display step header with better styling
    step_names = {
        1: "👨‍🎓 Student Database",
        2: "📊 Analytics Dashboard",
        3: "🏢 Company Registration",
        4: "📅 Drive Scheduling",
        5: "🎯 Student-Company Matching",
        6: "📝 Interview Management",
        7: "✅ Placement Records",
        8: "📈 Performance Reports"
    }
    
    # Create a nice header with step information
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Step {current_step}: {step_names[current_step]}")
    with col2:
        total_steps = 8
        progress = current_step / total_steps
        st.progress(progress)
        st.caption(f"Step {current_step} of {total_steps}")
    
    # Display appropriate step
    if current_step == 1:
        self.step1_student_database()
    elif current_step == 2:
        self.step2_analytics_dashboard()
    elif current_step == 3:
        self.step3_company_registration()
    elif current_step == 4:
        self.step4_drive_scheduling()
    elif current_step == 5:
        self.step5_student_company_matching()
    elif current_step == 6:
        self.step6_interview_management()
    elif current_step == 7:
        self.step7_placement_records()
    elif current_step == 8:
        self.step8_performance_reports()
    
    # Navigation buttons at bottom
    st.divider()
    self.display_workflow_navigation(current_step)
