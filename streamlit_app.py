import streamlit as st
import pandas as pd
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Page configuration - MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="AI Campus Placement Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state FIRST
if 'selected_role' not in st.session_state:
    st.session_state.selected_role = None
if 'demo_mode' not in st.session_state:
    st.session_state.demo_mode = False
if 'current_step_student' not in st.session_state:
    st.session_state.current_step_student = 1
if 'current_step_college' not in st.session_state:
    st.session_state.current_step_college = 1

# Title and description
st.title("🎓 AI-Powered Campus Placement Management System")
st.markdown("""
### National Level Hackathon Project
**A Systematic End-to-End Placement Management Platform**
""")

# Sidebar for workflow selection
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/graduation-cap.png", width=100)
    st.title("Platform Navigation")
    
    # Role selection
    st.subheader("Select Your Role")
    
    # Use radio buttons for role selection
    role = st.radio(
        "Choose your role:",
        ["👨‍🎓 Student", "🏫 College Admin", "💼 Recruiter", "👀 Observer"],
        key="role_selection",
        label_visibility="collapsed"
    )
    
    # Store selected role in session state
    if role != st.session_state.get('selected_role'):
        st.session_state.selected_role = role
        st.rerun()
    
    st.divider()
    
    # Show workflow based on selected role - SIMPLIFIED
    if st.session_state.selected_role == "👨‍🎓 Student":
        st.subheader("👨‍🎓 Student Dashboard")
        st.write("📝 **1. Profile Setup**")
        st.write("📄 **2. Resume Builder**")
        st.write("💼 **3. Job Search**")
        st.write("📊 **4. Analytics**")
        
        # Step navigation for student
        st.divider()
        st.subheader("Progress")
        step = st.selectbox(
            "Go to step:",
            [1, 2, 3, 4],
            index=st.session_state.current_step_student-1,
            key="student_step_nav"
        )
        if step != st.session_state.current_step_student:
            st.session_state.current_step_student = step
            st.rerun()
        
    elif st.session_state.selected_role == "🏫 College Admin":
        st.subheader("🏫 College Admin Dashboard")
        st.write("👨‍🎓 **1. Student Management**")
        st.write("🏢 **2. Company Registration**")
        st.write("📅 **3. Campus Drives**")
        st.write("📈 **4. Analytics**")
        
        # Step navigation for college admin
        st.divider()
        st.subheader("Progress")
        step = st.selectbox(
            "Go to step:",
            [1, 2, 3, 4],
            index=st.session_state.current_step_college-1,
            key="college_step_nav"
        )
        if step != st.session_state.current_step_college:
            st.session_state.current_step_college = step
            st.rerun()
        
    elif st.session_state.selected_role == "💼 Recruiter":
        st.subheader("💼 Recruiter Dashboard")
        st.write("🏢 **1. Company Profile**")
        st.write("📋 **2. Post Jobs**")
        st.write("👥 **3. View Applicants**")
        st.write("📅 **4. Schedule Interviews**")
        
    else:
        st.subheader("👀 Observer View")
        st.write("📊 **Platform Overview**")
        st.write("🎮 **Feature Demos**")
        st.write("📈 **Statistics**")
    
    # Demo mode toggle
    st.divider()
    if st.button("🎮 Toggle Demo Mode", use_container_width=True):
        st.session_state.demo_mode = not st.session_state.demo_mode
        st.rerun()
    
    if st.session_state.demo_mode:
        st.success("✅ Demo Mode Active")
    else:
        st.info("🌐 Live Mode Active")
    
    # Quick stats
    st.divider()
    st.subheader("Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Students", "1,250", "+45")
    with col2:
        st.metric("Companies", "85", "+12")
    
    # Footer
    st.divider()
    st.caption("🎓 Hackathon Project 2024 | AI Campus Placement Platform")

# Main content area - Show selected workflow
if st.session_state.selected_role == "👨‍🎓 Student":
    
    # Student dashboard header
    st.header(f"👨‍🎓 Student Dashboard - Step {st.session_state.current_step_student}")
    
    # Progress bar
    progress = st.session_state.current_step_student / 4
    st.progress(progress)
    
    # Student workflow steps
    if st.session_state.current_step_student == 1:
        # Step 1: Profile Setup
        st.subheader("📝 Student Profile Setup")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.form("student_profile_form"):
                st.write("### Basic Information")
                full_name = st.text_input("Full Name", "Rahul Sharma")
                roll_number = st.text_input("Roll Number", "CS2021001")
                email = st.text_input("Email", "rahul.sharma@college.edu")
                phone = st.text_input("Phone", "+91 9876543210")
                
                st.write("### Academic Information")
                department = st.selectbox(
                    "Department",
                    ["Computer Science", "Information Technology", "Electronics", 
                     "Mechanical", "Civil", "Electrical"]
                )
                semester = st.slider("Semester", 1, 10, 6)
                cgpa = st.slider("CGPA", 0.0, 10.0, 8.5, 0.1)
                graduation_year = st.selectbox("Graduation Year", [2024, 2025, 2026, 2027])
                
                submitted = st.form_submit_button("Save Profile", type="primary")
                if submitted:
                    st.success(f"✅ Profile saved for {full_name}")
                    if st.button("Next Step →"):
                        st.session_state.current_step_student = 2
                        st.rerun()
        
        with col2:
            st.write("### Quick Stats")
            st.metric("Profile Completion", "75%", "25%")
            st.metric("Placement Ready Score", "68/100", "+8")
            
            st.write("### Skills Preview")
            skills = ["Python", "Java", "SQL", "Machine Learning", "Web Development"]
            for skill in skills:
                st.write(f"✅ {skill}")
            
            st.write("### Quick Actions")
            if st.button("📄 Upload Resume"):
                st.info("Resume upload feature coming soon")
            if st.button("🎯 Set Career Goals"):
                st.info("Career goals feature coming soon")
    
    elif st.session_state.current_step_student == 2:
        # Step 2: Resume Builder
        st.subheader("📄 AI Resume Builder")
        
        tab1, tab2, tab3 = st.tabs(["Build Resume", "Templates", "ATS Score"])
        
        with tab1:
            st.write("### Create Your Resume")
            
            # Resume sections
            with st.expander("Personal Information", expanded=True):
                name = st.text_input("Name", "Rahul Sharma")
                email = st.text_input("Email", "rahul.sharma@college.edu")
                phone = st.text_input("Phone", "+91 9876543210")
                linkedin = st.text_input("LinkedIn Profile", "linkedin.com/in/rahulsharma")
                github = st.text_input("GitHub", "github.com/rahulsharma")
            
            with st.expander("Education"):
                col1, col2 = st.columns(2)
                with col1:
                    degree = st.text_input("Degree", "B.Tech Computer Science")
                    university = st.text_input("University", "ABC University")
                with col2:
                    cgpa_resume = st.text_input("CGPA", "8.5/10")
                    year = st.text_input("Year", "2020-2024")
            
            with st.expander("Skills"):
                skills = st.text_area("Enter your skills (comma separated)", 
                                    "Python, Java, SQL, Machine Learning, Data Structures, Web Development")
            
            with st.expander("Projects"):
                project1 = st.text_input("Project 1", "AI Resume Screening System")
                project1_desc = st.text_area("Description", "Built an AI-powered system to screen resumes using machine learning algorithms")
                
                project2 = st.text_input("Project 2", "E-commerce Website")
                project2_desc = st.text_area("Description 2", "Developed a full-stack e-commerce website with payment integration")
            
            if st.button("Generate Resume", type="primary"):
                st.success("✅ Resume generated successfully!")
                st.balloons()
                
                # Preview
                st.subheader("Resume Preview")
                st.markdown(f"""
                ## {name}
                **Contact:** {email} | {phone}  
                **LinkedIn:** {linkedin} | **GitHub:** {github}
                
                ---
                
                ### Education
                **{degree}** - {university}  
                CGPA: {cgpa_resume} | {year}
                
                ---
                
                ### Skills
                {skills}
                
                ---
                
                ### Projects
                **{project1}**  
                {project1_desc}
                
                **{project2}**  
                {project2_desc}
                """)
        
        with tab2:
            st.write("### Resume Templates")
            cols = st.columns(3)
            templates = [
                ("Professional", "Clean corporate style"),
                ("Modern", "Contemporary design"),
                ("Creative", "For design roles")
            ]
            
            for idx, (name, desc) in enumerate(templates):
                with cols[idx]:
                    st.write(f"#### {name}")
                    st.write(desc)
                    if st.button(f"Use {name}", key=f"template_{idx}"):
                        st.success(f"Selected {name} template")
        
        with tab3:
            st.write("### ATS Score Checker")
            st.info("Upload or paste your resume to check ATS compatibility")
            
            resume_text = st.text_area("Paste your resume text here", height=200)
            if st.button("Check ATS Score", type="primary"):
                # Simulate ATS score
                import random
                score = random.randint(65, 95)
                st.metric("ATS Score", f"{score}/100")
                
                if score >= 80:
                    st.success("✅ Excellent! Your resume is ATS-friendly")
                elif score >= 60:
                    st.warning("⚠️ Good, but could be improved")
                else:
                    st.error("❌ Needs significant improvement")
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_student = 1
                st.rerun()
        with col3:
            if st.button("Next Step →"):
                st.session_state.current_step_student = 3
                st.rerun()
    
    elif st.session_state.current_step_student == 3:
        # Step 3: Job Search
        st.subheader("💼 Job Opportunities")
        
        # Search filters
        col1, col2, col3 = st.columns(3)
        with col1:
            job_type = st.selectbox("Job Type", ["All", "Full-time", "Internship", "Part-time"])
        with col2:
            location = st.selectbox("Location", ["All", "Bangalore", "Hyderabad", "Pune", "Remote"])
        with col3:
            min_salary = st.slider("Minimum Salary (LPA)", 0, 50, 5)
        
        # Sample job listings
        jobs = [
            {
                "title": "Software Development Engineer",
                "company": "Google",
                "location": "Bangalore",
                "type": "Full-time",
                "salary": "15-30 LPA",
                "skills": "Python, Java, SQL",
                "description": "Develop and maintain software applications for Google's core products."
            },
            {
                "title": "Product Manager Intern",
                "company": "Microsoft",
                "location": "Hyderabad",
                "type": "Internship",
                "salary": "7-10 LPA",
                "skills": "Product Management, Analytics",
                "description": "Assist in product development and strategy planning."
            },
            {
                "title": "Data Scientist",
                "company": "Amazon",
                "location": "Bangalore",
                "type": "Full-time",
                "salary": "18-35 LPA",
                "skills": "Python, ML, Statistics",
                "description": "Build machine learning models for e-commerce recommendations."
            },
            {
                "title": "Frontend Developer",
                "company": "Startup XYZ",
                "location": "Remote",
                "type": "Full-time",
                "salary": "10-20 LPA",
                "skills": "React, JavaScript, CSS",
                "description": "Build responsive web applications for our SaaS platform."
            }
        ]
        
        # Display jobs
        for idx, job in enumerate(jobs):
            with st.expander(f"**{job['title']}** - {job['company']} ({job['location']})", expanded=idx==0):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Type:** {job['type']}")
                    st.write(f"**Salary:** {job['salary']}")
                    st.write(f"**Skills Required:** {job['skills']}")
                    st.write(f"**Description:** {job['description']}")
                with col2:
                    if st.button(f"Apply Now", key=f"apply_{idx}", type="primary"):
                        st.success(f"✅ Applied for {job['title']} at {job['company']}!")
                        st.balloons()
                
                st.divider()
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_student = 2
                st.rerun()
        with col3:
            if st.button("Next Step →"):
                st.session_state.current_step_student = 4
                st.rerun()
    
    elif st.session_state.current_step_student == 4:
        # Step 4: Analytics
        st.subheader("📊 Placement Analytics & Predictions")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Applications", "12", "+3")
        with col2:
            st.metric("Interviews", "4", "+1")
        with col3:
            st.metric("Offers", "1", "0")
        with col4:
            st.metric("Success Rate", "8.3%", "+2.1%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Application Status")
            status_data = pd.DataFrame({
                'Status': ['Applied', 'Shortlisted', 'Rejected', 'Interview', 'Selected'],
                'Count': [5, 3, 2, 1, 1]
            })
            st.bar_chart(status_data.set_index('Status'))
        
        with col2:
            st.write("### Placement Probability")
            # Simulated prediction
            import random
            probability = random.randint(65, 95)
            st.metric("AI Prediction", f"{probability}%")
            
            if probability >= 85:
                st.success("🎯 High chance of placement!")
                st.write("**Predicted Companies:** Google, Microsoft, Amazon")
                st.write("**Expected Package:** 15-25 LPA")
            elif probability >= 70:
                st.warning("📈 Good potential, keep applying!")
                st.write("**Predicted Companies:** TCS, Infosys, Wipro")
                st.write("**Expected Package:** 8-15 LPA")
            else:
                st.info("📚 Focus on skill development")
                st.write("**Suggestions:** Improve CGPA, add projects, learn new skills")
        
        # Skill gap analysis
        st.write("### 🔍 Skill Gap Analysis")
        skill_gaps = {
            "Python": "Advanced",
            "Machine Learning": "Intermediate",
            "System Design": "Beginner",
            "Cloud Computing": "Beginner",
            "Communication": "Intermediate"
        }
        
        for skill, level in skill_gaps.items():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(f"**{skill}**")
            with col2:
                if level == "Advanced":
                    st.progress(0.9)
                elif level == "Intermediate":
                    st.progress(0.6)
                else:
                    st.progress(0.3)
                st.caption(f"Current: {level}")
        
        # Recommendations
        st.write("### 💡 Personalized Recommendations")
        recommendations = [
            "✅ Complete 2 more projects for your portfolio",
            "✅ Practice coding problems daily (LeetCode/HackerRank)",
            "✅ Attend mock interviews weekly",
            "✅ Network with alumni in target companies",
            "✅ Update LinkedIn profile with new skills"
        ]
        
        for rec in recommendations:
            st.write(rec)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_student = 3
                st.rerun()
        with col2:
            if st.button("🎯 Complete Setup", type="primary"):
                st.success("🎉 Student profile setup completed!")
                st.balloons()
                st.session_state.current_step_student = 1  # Reset to step 1
                st.rerun()

elif st.session_state.selected_role == "🏫 College Admin":
    
    # College Admin dashboard
    st.header(f"🏫 College Admin Dashboard - Step {st.session_state.current_step_college}")
    
    # Progress bar
    progress = st.session_state.current_step_college / 4
    st.progress(progress)
    
    # College workflow steps
    if st.session_state.current_step_college == 1:
        # Step 1: Student Management
        st.subheader("👨‍🎓 Student Management")
        
        tab1, tab2, tab3 = st.tabs(["All Students", "Add Student", "Bulk Upload"])
        
        with tab1:
            st.write("### Student Database")
            
            # Sample student data
            students = pd.DataFrame({
                'Roll No': ['CS2021001', 'CS2021002', 'CS2021003', 'IT2021001', 'IT2021002'],
                'Name': ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Singh', 'Rajesh Verma'],
                'Department': ['CS', 'CS', 'CS', 'IT', 'IT'],
                'Semester': [6, 6, 6, 5, 5],
                'CGPA': [8.5, 8.2, 7.9, 8.8, 8.1],
                'Placement Status': ['Placed', 'Not Placed', 'Interview', 'Placed', 'Not Placed'],
                'Company': ['Google', '-', 'Microsoft', 'Amazon', '-']
            })
            
            st.dataframe(students, use_container_width=True)
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                department_filter = st.multiselect(
                    "Filter by Department",
                    ['CS', 'IT', 'ECE', 'EEE', 'Mechanical'],
                    default=['CS', 'IT']
                )
            with col2:
                status_filter = st.multiselect(
                    "Filter by Placement Status",
                    ['Placed', 'Not Placed', 'Interview', 'Intern'],
                    default=['Placed', 'Not Placed', 'Interview']
                )
        
        with tab2:
            st.write("### Add New Student")
            
            with st.form("add_student_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Full Name")
                    roll_no = st.text_input("Roll Number")
                    email = st.text_input("Email")
                    phone = st.text_input("Phone")
                
                with col2:
                    department = st.selectbox(
                        "Department",
                        ["Computer Science", "Information Technology", "Electronics", 
                         "Mechanical", "Civil", "Electrical"]
                    )
                    semester = st.number_input("Semester", 1, 10, 6)
                    cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0, 0.1)
                    graduation_year = st.selectbox("Graduation Year", [2024, 2025, 2026, 2027])
                
                submitted = st.form_submit_button("Add Student", type="primary")
                if submitted:
                    st.success(f"✅ Student {name} added successfully!")
        
        with tab3:
            st.write("### Bulk Upload Students")
            uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                st.write("Preview:")
                st.dataframe(df.head())
                
                if st.button("Process Upload", type="primary"):
                    st.success(f"✅ {len(df)} students uploaded successfully!")
        
        # Navigation
        col1, col2 = st.columns(2)
        with col2:
            if st.button("Next Step →"):
                st.session_state.current_step_college = 2
                st.rerun()
    
    elif st.session_state.current_step_college == 2:
        # Step 2: Company Registration
        st.subheader("🏢 Company Registration")
        
        tab1, tab2 = st.tabs(["Register Company", "Company Database"])
        
        with tab1:
            st.write("### Register New Company")
            
            with st.form("company_registration"):
                col1, col2 = st.columns(2)
                
                with col1:
                    company_name = st.text_input("Company Name")
                    industry = st.selectbox(
                        "Industry",
                        ["IT", "Finance", "E-commerce", "Manufacturing", "Healthcare", "Education"]
                    )
                    website = st.text_input("Website")
                    headquarters = st.text_input("Headquarters")
                
                with col2:
                    contact_person = st.text_input("Contact Person")
                    contact_email = st.text_input("Contact Email")
                    contact_phone = st.text_input("Contact Phone")
                    hr_email = st.text_input("HR Email")
                
                description = st.text_area("Company Description", height=100)
                
                submitted = st.form_submit_button("Register Company", type="primary")
                if submitted:
                    st.success(f"✅ {company_name} registered successfully!")
        
        with tab2:
            st.write("### Registered Companies")
            
            # Sample company data
            companies = pd.DataFrame({
                'Company': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys'],
                'Industry': ['IT', 'IT', 'E-commerce', 'IT', 'IT'],
                'Contact': ['hr@google.com', 'hr@microsoft.com', 'hr@amazon.com', 'hr@tcs.com', 'hr@infosys.com'],
                'Status': ['Verified', 'Verified', 'Verified', 'Pending', 'Verified'],
                'Drives': [3, 2, 4, 1, 2]
            })
            
            st.dataframe(companies, use_container_width=True)
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_college = 1
                st.rerun()
        with col3:
            if st.button("Next Step →"):
                st.session_state.current_step_college = 3
                st.rerun()
    
    elif st.session_state.current_step_college == 3:
        # Step 3: Campus Drives
        st.subheader("📅 Campus Drive Management")
        
        # Create new drive
        with st.expander("📝 Schedule New Campus Drive", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                company = st.selectbox("Select Company", ["Google", "Microsoft", "Amazon", "TCS", "Infosys"])
                drive_date = st.date_input("Drive Date")
                drive_mode = st.selectbox("Mode", ["Online", "Offline", "Hybrid"])
            
            with col2:
                coordinator = st.text_input("Coordinator Name")
                coordinator_contact = st.text_input("Coordinator Contact")
                registration_deadline = st.date_input("Registration Deadline")
            
            if st.button("Schedule Drive", type="primary"):
                st.success(f"✅ Campus drive scheduled for {company} on {drive_date}")
        
        # Existing drives
        st.write("### Upcoming Drives")
        drives = pd.DataFrame({
            'Company': ['Google', 'Microsoft', 'Amazon'],
            'Date': ['2024-03-15', '2024-03-20', '2024-03-25'],
            'Mode': ['Online', 'Offline', 'Hybrid'],
            'Registered': [150, 120, 180],
            'Status': ['Scheduled', 'Scheduled', 'Scheduled']
        })
        
        st.dataframe(drives, use_container_width=True)
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_college = 2
                st.rerun()
        with col3:
            if st.button("Next Step →"):
                st.session_state.current_step_college = 4
                st.rerun()
    
    elif st.session_state.current_step_college == 4:
        # Step 4: Analytics
        st.subheader("📈 Placement Analytics Dashboard")
        
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", "1,250", "+45")
        with col2:
            st.metric("Placed Students", "850", "+32")
        with col3:
            st.metric("Placement Rate", "68%", "+2.1%")
        with col4:
            st.metric("Avg Package", "12.5 LPA", "+1.2 LPA")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Placement by Department")
            dept_data = pd.DataFrame({
                'Department': ['CS', 'IT', 'ECE', 'EEE', 'Mechanical'],
                'Placed': [220, 180, 150, 120, 90],
                'Total': [300, 250, 200, 150, 120]
            })
            st.bar_chart(dept_data.set_index('Department'))
        
        with col2:
            st.write("### Top Recruiters")
            recruiter_data = pd.DataFrame({
                'Company': ['Google', 'Microsoft', 'Amazon', 'TCS', 'Infosys'],
                'Hires': [45, 38, 42, 65, 55]
            })
            st.bar_chart(recruiter_data.set_index('Company'))
        
        # Placement trends
        st.write("### 📊 Monthly Placement Trends")
        trend_data = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            'Placements': [120, 145, 180, 160, 195, 210],
            'Interviews': [350, 380, 420, 400, 450, 480]
        })
        st.line_chart(trend_data.set_index('Month'))
        
        # Department-wise analysis
        st.write("### 🔍 Department-wise Analysis")
        cols = st.columns(5)
        departments = [
            ("CS", "85%", "15.2 LPA"),
            ("IT", "82%", "14.8 LPA"),
            ("ECE", "78%", "12.5 LPA"),
            ("EEE", "75%", "11.2 LPA"),
            ("Mechanical", "70%", "10.5 LPA")
        ]
        
        for idx, (dept, rate, package) in enumerate(departments):
            with cols[idx]:
                st.metric(f"{dept} Dept", rate, package)
        
        # Navigation
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Previous Step"):
                st.session_state.current_step_college = 3
                st.rerun()
        with col2:
            if st.button("🏁 Complete Setup", type="primary"):
                st.success("🎉 College admin setup completed!")
                st.balloons()
                st.session_state.current_step_college = 1  # Reset to step 1
                st.rerun()

elif st.session_state.selected_role == "💼 Recruiter":
    
    # Recruiter dashboard
    st.header("💼 Recruiter Dashboard")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Jobs", "8", "+2")
    with col2:
        st.metric("Applications", "245", "+45")
    with col3:
        st.metric("Interviews", "32", "+8")
    with col4:
        st.metric("Hires", "12", "+3")
    
    # Tabs for different recruiter functions
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Company Profile", "📋 Post Jobs", "👥 View Applicants", "📅 Schedule Interviews"])
    
    with tab1:
        st.subheader("🏢 Company Profile")
        
        with st.form("company_profile"):
            col1, col2 = st.columns(2)
            
            with col1:
                company_name = st.text_input("Company Name", "TechCorp Solutions")
                industry = st.selectbox("Industry", ["IT", "Finance", "E-commerce", "Manufacturing"])
                founded_year = st.number_input("Founded Year", 1990, 2024, 2010)
                employee_count = st.selectbox("Employee Count", ["1-50", "51-200", "201-1000", "1000+"])
            
            with col2:
                website = st.text_input("Website", "https://techcorp.com")
                headquarters = st.text_input("Headquarters", "Bangalore, India")
                contact_email = st.text_input("Contact Email", "hr@techcorp.com")
                contact_phone = st.text_input("Contact Phone", "+91 80 1234 5678")
            
            description = st.text_area("Company Description", 
                                     "TechCorp Solutions is a leading technology company specializing in AI and cloud solutions...",
                                     height=150)
            
            if st.form_submit_button("Update Profile", type="primary"):
                st.success("✅ Company profile updated successfully!")
    
    with tab2:
        st.subheader("📋 Post New Job")
        
        with st.form("post_job"):
            col1, col2 = st.columns(2)
            
            with col1:
                job_title = st.text_input("Job Title", "Software Engineer")
                job_type = st.selectbox("Job Type", ["Full-time", "Internship", "Contract", "Part-time"])
                location = st.text_input("Location", "Bangalore")
                vacancies = st.number_input("Number of Vacancies", 1, 100, 5)
            
            with col2:
                salary_min = st.number_input("Minimum Salary (LPA)", 0, 100, 10)
                salary_max = st.number_input("Maximum Salary (LPA)", 0, 100, 25)
                min_cgpa = st.slider("Minimum CGPA", 0.0, 10.0, 7.0, 0.1)
                application_deadline = st.date_input("Application Deadline")
            
            required_skills = st.text_area("Required Skills (comma separated)", 
                                         "Python, Java, SQL, Algorithms, Data Structures")
            job_description = st.text_area("Job Description", 
                                         "We are looking for a talented Software Engineer to join our team...",
                                         height=150)
            
            if st.form_submit_button("Post Job", type="primary"):
                st.success("✅ Job posted successfully!")
                st.balloons()
    
    with tab3:
        st.subheader("👥 View Applications")
        
        # Sample applications
        applications = pd.DataFrame({
            'Name': ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Singh'],
            'Roll No': ['CS2021001', 'CS2021002', 'CS2021003', 'IT2021001'],
            'CGPA': [8.5, 8.2, 7.9, 8.8],
            'Skills': ['Python, Java, ML', 'Web Dev, React', 'Data Science, SQL', 'Cloud, DevOps'],
            'Status': ['Shortlisted', 'Applied', 'Rejected', 'Interview'],
            'Applied On': ['2024-01-15', '2024-01-16', '2024-01-14', '2024-01-17']
        })
        
        st.dataframe(applications, use_container_width=True)
        
        # Application filters
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                ['Applied', 'Shortlisted', 'Rejected', 'Interview', 'Selected'],
                default=['Applied', 'Shortlisted', 'Interview']
            )
        with col2:
            min_cgpa_filter = st.slider("Minimum CGPA Filter", 0.0, 10.0, 7.5, 0.1)
        
        # Action buttons for each application
        st.write("### Quick Actions")
        for idx, row in applications.iterrows():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{row['Name']}** ({row['Roll No']}) - CGPA: {row['CGPA']}")
            with col2:
                if st.button("View Resume", key=f"resume_{idx}"):
                    st.info(f"Showing resume for {row['Name']}")
            with col3:
                if st.button("Schedule Interview", key=f"interview_{idx}"):
                    st.success(f"Interview scheduled for {row['Name']}")
            with col4:
                if st.button("Reject", key=f"reject_{idx}"):
                    st.warning(f"Application rejected for {row['Name']}")
            st.divider()
    
    with tab4:
        st.subheader("📅 Interview Schedule")
        
        # Sample interviews
        interviews = pd.DataFrame({
            'Candidate': ['Rahul Sharma', 'Priya Patel', 'Amit Kumar'],
            'Position': ['Software Engineer', 'Frontend Developer', 'Data Scientist'],
            'Date': ['2024-01-20 10:00 AM', '2024-01-21 02:30 PM', '2024-01-22 11:00 AM'],
            'Mode': ['Online', 'Offline', 'Online'],
            'Status': ['Scheduled', 'Completed', 'Scheduled'],
            'Interviewer': ['John Doe', 'Jane Smith', 'Mike Johnson']
        })
        
        st.dataframe(interviews, use_container_width=True)
        
        # Schedule new interview
        st.write("### Schedule New Interview")
        col1, col2 = st.columns(2)
        with col1:
            candidate = st.selectbox("Select Candidate", ['Rahul Sharma', 'Priya Patel', 'Amit Kumar', 'Sneha Singh'])
            interview_date = st.date_input("Interview Date")
        with col2:
            interview_time = st.time_input("Interview Time")
            interview_mode = st.selectbox("Mode", ["Online", "Offline"])
            interviewer = st.text_input("Interviewer Name")
        
        if st.button("Schedule Interview", type="primary"):
            st.success(f"✅ Interview scheduled for {candidate} on {interview_date} at {interview_time}")

else:
    # Observer view
    st.header("👀 Platform Overview")
    
    # Platform stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", "1,250")
    with col2:
        st.metric("Registered Companies", "85")
    with col3:
        st.metric("Active Jobs", "245")
    with col4:
        st.metric("Placement Rate", "68%")
    
    st.divider()
    
    # Feature demos
    st.subheader("🎮 Feature Demos")
    
    demo_col1, demo_col2, demo_col3 = st.columns(3)
    
    with demo_col1:
        st.markdown("### 👨‍🎓 Student Features")
        if st.button("Try AI Resume Builder", use_container_width=True):
            st.session_state.selected_role = "👨‍🎓 Student"
            st.session_state.current_step_student = 2
            st.rerun()
        
        features = [
            "✅ AI Resume Builder with ATS scoring",
            "✅ Personalized career path planning",
            "✅ Placement probability prediction",
            "✅ Interview preparation simulator",
            "✅ NEP course advisor",
            "✅ PM internship matching"
        ]
        for feature in features:
            st.write(feature)
    
    with demo_col2:
        st.markdown("### 🏫 College Admin Features")
        if st.button("Try Student Analytics", use_container_width=True):
            st.session_state.selected_role = "🏫 College Admin"
            st.session_state.current_step_college = 4
            st.rerun()
        
        features = [
            "✅ Complete student database",
            "✅ Real-time analytics dashboard",
            "✅ Company registration portal",
            "✅ Campus drive scheduling",
            "✅ AI-based student-company matching",
            "✅ Interview management system",
            "✅ Placement records tracking",
            "✅ Performance reporting"
        ]
        for feature in features:
            st.write(feature)
    
    with demo_col3:
        st.markdown("### 💼 Recruiter Features")
        if st.button("Try Job Posting", use_container_width=True):
            st.session_state.selected_role = "💼 Recruiter"
            st.rerun()
        
        features = [
            "✅ Company profile management",
            "✅ Smart job posting system",
            "✅ AI-powered candidate screening",
            "✅ Interview scheduling automation",
            "✅ Offer management system",
            "✅ Hiring analytics dashboard"
        ]
        for feature in features:
            st.write(feature)
    
    st.divider()
    
    # Platform architecture
    st.subheader("🏗️ Platform Architecture")
    architecture = """
    ```
    ┌─────────────────────────────────────────────────────────────┐
    │                    Streamlit Frontend                       │
    ├─────────────────────────────────────────────────────────────┤
    │  • Student Flow      • College Flow     • Recruiter Flow    │
    ├─────────────────────────────────────────────────────────────┤
    │                 AI/ML Modules & Services                    │
    │  • Resume Analysis  • Placement Prediction • Skill Matching │
    ├─────────────────────────────────────────────────────────────┤
    │                SQLite Database (campus_placement.db)        │
    │  • Users           • Students          • Companies          │
    │  • Job Postings    • Applications      • Placements         │
    └─────────────────────────────────────────────────────────────┘
    ```
    """
    st.markdown(architecture)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center">
    <p>🎓 <b>AI Campus Placement Platform</b> | National Level Hackathon Project 2024</p>
    <p>Built with ❤️ using Streamlit & Python | Database Integrated | Systematic Workflow</p>
    <p>📍 <b>Features:</b> AI Resume Builder • Placement Prediction • NEP Advisor • Interview Prep • Analytics Dashboard</p>
</div>
""", unsafe_allow_html=True)

# Add some CSS for better appearance
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
    }
    .css-1d391kg {
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)
