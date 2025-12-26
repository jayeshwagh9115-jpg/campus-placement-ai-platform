# Main content area - Show selected workflow
if st.session_state.selected_role == "👨‍🎓 Student":
    # Get current step and display appropriate module
    current_step = st.session_state.get('current_step_student', 1)
    st.session_state.student_flow.current_step = current_step
    st.session_state.student_flow.display()
    
elif st.session_state.selected_role == "🏫 College Admin":
    # Get current step and display appropriate module
    current_step = st.session_state.get('current_step_college', 1)
    st.session_state.college_flow.current_step = current_step
    st.session_state.college_flow.display()
    
elif st.session_state.selected_role == "💼 Recruiter":
    st.session_state.recruiter_flow.display()
    
else:
    # Observer view
    st.session_state.workflow_manager.display_observer_view()
    
    # Add platform overview for observers
    st.header("🚀 Platform Features Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 👨‍🎓 Student Features")
        features = [
            "✅ AI Resume Builder",
            "✅ Career Path Planning",
            "✅ Placement Prediction",
            "✅ Interview Preparation",
            "✅ NEP Course Advisor",
            "✅ PM Internship Match"
        ]
        for feature in features:
            st.write(feature)
    
    with col2:
        st.markdown("### 🏫 College Admin Features")
        features = [
            "✅ Student Database",
            "✅ Analytics Dashboard",
            "✅ Company Registration",
            "✅ Drive Scheduling",
            "✅ Student-Company Matching",
            "✅ Interview Management",
            "✅ Placement Records",
            "✅ Performance Reports"
        ]
        for feature in features:
            st.write(feature)
    
    with col3:
        st.markdown("### 💼 Recruiter Features")
        features = [
            "✅ Company Profile",
            "✅ Job Posting",
            "✅ Candidate Search",
            "✅ AI Screening",
            "✅ Interview Scheduling",
            "✅ Offer Management",
            "✅ Hiring Analytics"
        ]
        for feature in features:
            st.write(feature)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project</p>
    <p>Built with ❤️ using Streamlit & Python | Database Integrated | Systematic Workflow</p>
</div>
""", unsafe_allow_html=True)
