import streamlit as st
import pandas as pd
import json

class StudentFlow:
    def __init__(self):
        self.current_step = 1
        self.db_manager = None
        self.demo_mode = True
        
        # Initialize session state for student data
        if 'student_data' not in st.session_state:
            st.session_state.student_data = {
                "personal_info": {},
                "education": {},
                "skills": [],
                "projects": [],
                "internships": [],
                "career_preferences": {},
                "resume_data": {}
            }
    
    def set_database_manager(self, db_manager, demo_mode):
        """Set database manager and demo mode"""
        self.db_manager = db_manager
        self.demo_mode = demo_mode
    
    def display(self):
        """Main display method that routes to appropriate step"""
        st.header(f"👨‍🎓 Student Placement Journey - Step {self.current_step}")
        
        # Route to appropriate step method
        if self.current_step == 1:
            self.step1_profile_creation()
        elif self.current_step == 2:
            self.step2_ai_resume_building()
        elif self.current_step == 3:
            self.step3_nep_course_planning()
        elif self.current_step == 4:
            self.step4_internship_match()
        elif self.current_step == 5:
            self.step5_career_path_planning()
        elif self.current_step == 6:
            self.step6_placement_prediction()
        elif self.current_step == 7:
            self.step7_interview_preparation()
        elif self.current_step == 8:
            self.step8_placement_tracking()
        else:
            st.error("Invalid step number")
    
    def step1_profile_creation(self):
        """Step 1: Profile Creation"""
        st.subheader("🎯 Profile Creation")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*", value=st.session_state.student_data["personal_info"].get("full_name", ""))
                email = st.text_input("Email*", value=st.session_state.student_data["personal_info"].get("email", ""))
                phone = st.text_input("Phone Number", value=st.session_state.student_data["personal_info"].get("phone", ""))
                dob = st.date_input("Date of Birth", value=pd.to_datetime(st.session_state.student_data["personal_info"].get("dob", "2000-01-01")))
            
            with col2:
                roll_number = st.text_input("Roll Number*", value=st.session_state.student_data["personal_info"].get("roll_number", ""))
                department = st.selectbox("Department*", 
                                         ["Computer Science", "Electronics", "Mechanical", "Civil", 
                                          "Electrical", "Information Technology", "Other"],
                                         index=0)
                year_of_study = st.selectbox("Year of Study*", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Final Year"])
                cgpa = st.slider("Current CGPA", 0.0, 10.0, value=float(st.session_state.student_data["personal_info"].get("cgpa", 7.5)))
            
            address = st.text_area("Address", value=st.session_state.student_data["personal_info"].get("address", ""))
            
            submitted = st.form_submit_button("Save Profile")
            
            if submitted:
                if full_name and email and roll_number and department:
                    # Save to session state
                    st.session_state.student_data["personal_info"] = {
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "dob": str(dob),
                        "roll_number": roll_number,
                        "department": department,
                        "year_of_study": year_of_study,
                        "cgpa": cgpa,
                        "address": address
                    }
                    
                    # Save to database if available
                    if not self.demo_mode and self.db_manager and self.db_manager.is_connected:
                        try:
                            # Check if student already exists
                            existing = self.db_manager.select('students', where=f"roll_number='{roll_number}'")
                            student_data = {
                                "full_name": full_name,
                                "email": email,
                                "phone": phone,
                                "dob": str(dob),
                                "roll_number": roll_number,
                                "department": department,
                                "year_of_study": year_of_study,
                                "cgpa": cgpa,
                                "address": address,
                                "status": "active"
                            }
                            
                            if existing and len(existing) > 0:
                                # Update existing record
                                result = self.db_manager.update('students', 
                                                               student_data, 
                                                               where=f"roll_number='{roll_number}'")
                                st.success("✅ Profile updated successfully!")
                            else:
                                # Insert new record
                                result = self.db_manager.insert('students', student_data)
                                st.success("✅ Profile created successfully!")
                                
                            st.balloons()
                        except Exception as e:
                            st.error(f"Database error: {e}")
                            st.info("Profile saved locally (Demo Mode)")
                    else:
                        st.success("✅ Profile saved locally (Demo Mode)")
                else:
                    st.error("Please fill all required fields (*)")
        
        # Show current profile data
        with st.expander("📋 View Current Profile"):
            if st.session_state.student_data["personal_info"]:
                st.write(st.session_state.student_data["personal_info"])
            else:
                st.info("No profile data yet")
    
    def step2_ai_resume_building(self):
        """Step 2: AI Resume Building"""
        st.subheader("📝 AI Resume Building")
        
        tab1, tab2, tab3 = st.tabs(["📚 Education", "💼 Experience", "🛠️ Skills"])
        
        with tab1:
            st.subheader("Education Details")
            
            with st.form("education_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    institution = st.text_input("Institution*", value=st.session_state.student_data["education"].get("institution", ""))
                    degree = st.text_input("Degree*", value=st.session_state.student_data["education"].get("degree", ""))
                
                with col2:
                    field_of_study = st.text_input("Field of Study", value=st.session_state.student_data["education"].get("field_of_study", ""))
                    graduation_year = st.number_input("Graduation Year", min_value=2000, max_value=2030, 
                                                     value=int(st.session_state.student_data["education"].get("graduation_year", 2024)))
                
                percentage = st.slider("Percentage/CGPA", 0.0, 100.0, value=float(st.session_state.student_data["education"].get("percentage", 75.0)))
                achievements = st.text_area("Achievements/Awards", value=st.session_state.student_data["education"].get("achievements", ""))
                
                submitted = st.form_submit_button("Save Education")
                
                if submitted and institution and degree:
                    st.session_state.student_data["education"] = {
                        "institution": institution,
                        "degree": degree,
                        "field_of_study": field_of_study,
                        "graduation_year": graduation_year,
                        "percentage": percentage,
                        "achievements": achievements
                    }
                    st.success("✅ Education details saved!")
        
        with tab2:
            st.subheader("Projects & Internships")
            
            # Projects
            st.write("#### 🏆 Projects")
            project_name = st.text_input("Project Name")
            project_desc = st.text_area("Project Description")
            project_tech = st.text_input("Technologies Used")
            
            if st.button("Add Project"):
                if project_name and project_desc:
                    st.session_state.student_data["projects"].append({
                        "name": project_name,
                        "description": project_desc,
                        "technologies": project_tech
                    })
                    st.success("Project added!")
            
            # Display projects
            if st.session_state.student_data["projects"]:
                for i, project in enumerate(st.session_state.student_data["projects"]):
                    with st.expander(f"Project {i+1}: {project['name']}"):
                        st.write(f"**Description:** {project['description']}")
                        st.write(f"**Technologies:** {project['technologies']}")
                        
                        if st.button(f"Remove Project {i+1}", key=f"remove_project_{i}"):
                            st.session_state.student_data["projects"].pop(i)
                            st.rerun()
        
        with tab3:
            st.subheader("Skills")
            
            # Skill categories
            skill_categories = {
                "Programming Languages": ["Python", "Java", "C++", "JavaScript", "SQL"],
                "Web Technologies": ["HTML/CSS", "React", "Node.js", "Django", "Flask"],
                "Data Science": ["Machine Learning", "Data Analysis", "Statistics", "Deep Learning"],
                "Tools": ["Git", "Docker", "AWS", "Tableau", "JIRA"]
            }
            
            selected_skills = st.multiselect(
                "Select your skills:",
                [skill for skills in skill_categories.values() for skill in skills],
                default=st.session_state.student_data.get("skills", [])
            )
            
            custom_skill = st.text_input("Add custom skill")
            if st.button("Add Custom Skill") and custom_skill:
                selected_skills.append(custom_skill)
            
            if st.button("Save Skills"):
                st.session_state.student_data["skills"] = selected_skills
                st.success(f"✅ {len(selected_skills)} skills saved!")
            
            # Display skills by category
            if st.session_state.student_data["skills"]:
                st.write("#### Your Skills:")
                for category, skills in skill_categories.items():
                    category_skills = [skill for skill in st.session_state.student_data["skills"] if skill in skills]
                    if category_skills:
                        st.write(f"**{category}:** {', '.join(category_skills)}")
        
        # Resume Preview
        st.divider()
        if st.button("🔄 Generate Resume Preview"):
            self.generate_resume_preview()
    
    def step3_nep_course_planning(self):
        """Step 3: NEP Course Planning"""
        st.subheader("📚 NEP Course Planning")
        
        st.info("""
        **National Education Policy (NEP) 2020** emphasizes:
        - Multidisciplinary education
        - Flexible curriculum
        - Skill-based learning
        - Credit transfer system
        """)
        
        # Course selection
        st.write("### Select Your Courses")
        
        courses_by_semester = {
            "Semester 1": ["Mathematics I", "Physics", "Programming Fundamentals", "English Communication"],
            "Semester 2": ["Mathematics II", "Chemistry", "Data Structures", "Environmental Science"],
            "Semester 3": ["Discrete Mathematics", "Digital Electronics", "OOP with Java", "Economics"],
            "Semester 4": ["Database Systems", "Computer Networks", "Algorithm Design", "Business Management"],
            "Electives": ["Machine Learning", "Web Development", "Cloud Computing", "Cyber Security", 
                         "IoT", "Blockchain", "Mobile App Development"]
        }
        
        selected_courses = {}
        
        for semester, courses in courses_by_semester.items():
            selected = st.multiselect(
                f"{semester} Courses:",
                courses,
                default=st.session_state.student_data.get("courses", {}).get(semester, courses[:2] if semester != "Electives" else [])
            )
            selected_courses[semester] = selected
        
        if st.button("Save Course Plan"):
            st.session_state.student_data["courses"] = selected_courses
            st.success("✅ Course plan saved!")
        
        # Credit calculation
        st.divider()
        st.write("### Credit Analysis")
        
        if "courses" in st.session_state.student_data:
            total_credits = 0
            for semester, courses in st.session_state.student_data["courses"].items():
                credits = len(courses) * 4  # Assuming 4 credits per course
                total_credits += credits
                st.write(f"{semester}: {len(courses)} courses ({credits} credits)")
            
            st.metric("Total Credits", total_credits)
            
            if total_credits < 160:
                st.warning("⚠️ You need at least 160 credits for graduation")
            else:
                st.success("✅ You have sufficient credits for graduation")
        
        # Career-relevant courses recommendation
        st.divider()
        st.write("### Career-focused Course Recommendations")
        
        career_tracks = {
            "Software Developer": ["OOP with Java", "Data Structures", "Algorithm Design", "Database Systems"],
            "Data Scientist": ["Mathematics I & II", "Statistics", "Machine Learning", "Data Analysis"],
            "Web Developer": ["Web Development", "JavaScript", "Database Systems", "Cloud Computing"],
            "Cyber Security": ["Computer Networks", "Cyber Security", "Blockchain", "Digital Electronics"]
        }
        
        selected_track = st.selectbox("Choose your career track:", list(career_tracks.keys()))
        
        if selected_track:
            st.write(f"**Recommended courses for {selected_track}:**")
            for course in career_tracks[selected_track]:
                st.write(f"• {course}")
    
    def step4_internship_match(self):
        """Step 4: Internship Matching"""
        st.subheader("💼 PM Internship Match")
        
        # Internship preferences
        st.write("### Set Your Internship Preferences")
        
        with st.form("internship_preferences"):
            col1, col2 = st.columns(2)
            
            with col1:
                internship_type = st.selectbox(
                    "Internship Type",
                    ["Summer Internship", "Winter Internship", "Semester Internship", "Virtual Internship", "Any"]
                )
                duration = st.selectbox(
                    "Preferred Duration",
                    ["1-2 months", "3-4 months", "6 months", "Flexible"]
                )
                stipend_exp = st.selectbox(
                    "Stipend Expectation",
                    ["Unpaid", "₹5,000-10,000", "₹10,000-20,000", "₹20,000-30,000", "₹30,000+", "Negotiable"]
                )
            
            with col2:
                location_pref = st.multiselect(
                    "Location Preference",
                    ["Work From Home", "On-site", "Hybrid", "Bangalore", "Delhi", "Mumbai", "Chennai", "Pune", "Any"]
                )
                role_pref = st.multiselect(
                    "Role Preference",
                    ["Software Development", "Data Analysis", "Web Development", "Mobile App Dev", 
                     "Machine Learning", "UI/UX Design", "Digital Marketing", "Business Analyst"]
                )
                company_size = st.selectbox(
                    "Company Size Preference",
                    ["Startup", "Small & Medium", "Large Corporation", "MNC", "Any"]
                )
            
            skills_to_highlight = st.multiselect(
                "Skills to Highlight",
                st.session_state.student_data.get("skills", []),
                default=st.session_state.student_data.get("skills", [])[:3]
            )
            
            submitted = st.form_submit_button("Save Preferences")
            
            if submitted:
                st.session_state.student_data["internship_prefs"] = {
                    "internship_type": internship_type,
                    "duration": duration,
                    "stipend_exp": stipend_exp,
                    "location_pref": location_pref,
                    "role_pref": role_pref,
                    "company_size": company_size,
                    "skills_to_highlight": skills_to_highlight
                }
                st.success("✅ Internship preferences saved!")
        
        # AI-based matching
        st.divider()
        st.write("### 🤖 AI-Powered Internship Matching")
        
        if st.button("Find Matching Internships"):
            # Simulated AI matching
            available_internships = [
                {
                    "company": "TechCorp Solutions",
                    "role": "Software Development Intern",
                    "location": "Bangalore/Hybrid",
                    "duration": "3 months",
                    "stipend": "₹20,000",
                    "match_score": 92,
                    "skills_required": ["Python", "Java", "Data Structures"]
                },
                {
                    "company": "DataAnalytics Inc.",
                    "role": "Data Science Intern",
                    "location": "Remote",
                    "duration": "6 months",
                    "stipend": "₹25,000",
                    "match_score": 85,
                    "skills_required": ["Python", "Machine Learning", "Statistics"]
                },
                {
                    "company": "WebCrafters",
                    "role": "Frontend Developer Intern",
                    "location": "Delhi",
                    "duration": "2 months",
                    "stipend": "₹15,000",
                    "match_score": 78,
                    "skills_required": ["JavaScript", "React", "HTML/CSS"]
                }
            ]
            
            for internship in available_internships:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{internship['company']}** - {internship['role']}")
                        st.write(f"📍 {internship['location']} | ⏱️ {internship['duration']} | 💰 {internship['stipend']}")
                        st.write(f"**Skills:** {', '.join(internship['skills_required'])}")
                    with col2:
                        st.metric("Match Score", f"{internship['match_score']}%")
                    with col3:
                        if st.button("Apply", key=f"apply_{internship['company']}"):
                            st.success(f"Applied to {internship['company']}!")
                    st.divider()
    
    def step5_career_path_planning(self):
        """Step 5: Career Path Planning"""
        st.subheader("🎯 Career Path Planning")
        
        # Career assessment
        st.write("### Career Assessment")
        
        interests = st.multiselect(
            "What are your interests?",
            ["Programming", "Data Analysis", "Design", "Management", "Research", "Teaching", "Entrepreneurship"],
            default=st.session_state.student_data.get("career_preferences", {}).get("interests", [])
        )
        
        work_env = st.selectbox(
            "Preferred work environment",
            ["Fast-paced Startup", "Stable Corporate", "Remote Work", "Research Lab", "Freelance"],
            index=0
        )
        
        salary_exp = st.slider("Expected starting salary (₹ per annum)", 300000, 2000000, 600000, step=50000)
        
        long_term_goal = st.text_area("Long-term career goal", 
                                     value=st.session_state.student_data.get("career_preferences", {}).get("long_term_goal", ""))
        
        if st.button("Save Career Preferences"):
            st.session_state.student_data["career_preferences"] = {
                "interests": interests,
                "work_env": work_env,
                "salary_exp": salary_exp,
                "long_term_goal": long_term_goal
            }
            st.success("✅ Career preferences saved!")
        
        # Career path recommendations
        st.divider()
        st.write("### Recommended Career Paths")
        
        career_paths = {
            "Software Engineer": {
                "path": "Junior Developer → Senior Developer → Tech Lead → Engineering Manager",
                "skills": ["Programming", "System Design", "Agile Methodology"],
                "avg_salary": "₹8-15 LPA"
            },
            "Data Scientist": {
                "path": "Data Analyst → Junior Data Scientist → Senior Data Scientist → Lead Data Scientist",
                "skills": ["Statistics", "Machine Learning", "Python/R"],
                "avg_salary": "₹10-20 LPA"
            },
            "Product Manager": {
                "path": "Associate PM → Product Manager → Senior PM → Director of Product",
                "skills": ["Communication", "Market Analysis", "Strategy"],
                "avg_salary": "₹12-25 LPA"
            }
        }
        
        for career, details in career_paths.items():
            with st.expander(f"📈 {career}"):
                st.write(f"**Career Path:** {details['path']}")
                st.write(f"**Key Skills:** {', '.join(details['skills'])}")
                st.write(f"**Average Salary:** {details['avg_salary']}")
                
                # Check match with student's skills
                student_skills = set(st.session_state.student_data.get("skills", []))
                required_skills = set(details['skills'])
                matched_skills = student_skills.intersection(required_skills)
                
                if matched_skills:
                    st.success(f"✅ You have {len(matched_skills)} matching skills: {', '.join(matched_skills)}")
                else:
                    st.warning("ℹ️ Consider developing these skills")
        
        # Gap analysis
        st.divider()
        if st.button("🔍 Analyze Skill Gaps"):
            self.analyze_skill_gaps()
    
    def step6_placement_prediction(self):
        """Step 6: Placement Prediction"""
        st.subheader("📊 Placement Prediction")
        
        st.info("""
        Our AI model predicts your placement chances based on:
        - Academic Performance
        - Skills & Projects
        - Internship Experience
        - Market Demand
        """)
        
        # Input factors for prediction
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA", 0.0, 10.0, 
                            value=float(st.session_state.student_data["personal_info"].get("cgpa", 7.5)), 
                            step=0.1)
            projects_count = st.slider("Number of Projects", 0, 10, 
                                      len(st.session_state.student_data.get("projects", [])), 
                                      step=1)
            internships_count = st.slider("Number of Internships", 0, 5, 
                                         len(st.session_state.student_data.get("internships", [])), 
                                         step=1)
        
        with col2:
            skills_count = st.slider("Number of Skills", 0, 20, 
                                    len(st.session_state.student_data.get("skills", [])), 
                                    step=1)
            coding_rating = st.slider("Coding Proficiency (1-10)", 1, 10, 5, step=1)
            communication_rating = st.slider("Communication Skills (1-10)", 1, 10, 6, step=1)
        
        # Predict button
        if st.button("🤖 Predict Placement Chances"):
            # Simple prediction algorithm (simplified)
            base_score = 50
            
            # CGPA contribution (up to 20 points)
            cgpa_score = (cgpa / 10.0) * 20
            
            # Projects contribution (up to 15 points)
            projects_score = min(projects_count * 3, 15)
            
            # Internships contribution (up to 15 points)
            internships_score = min(internships_count * 5, 15)
            
            # Skills contribution (up to 10 points)
            skills_score = min(skills_count * 0.5, 10)
            
            # Soft skills contribution (up to 10 points)
            soft_skills_score = (coding_rating + communication_rating) * 0.5
            
            total_score = base_score + cgpa_score + projects_score + internships_score + skills_score + soft_skills_score
            
            # Normalize to 0-100
            placement_probability = min(total_score, 100)
            
            # Display result
            st.subheader("📈 Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Placement Probability", f"{placement_probability:.1f}%")
            with col2:
                if placement_probability >= 80:
                    st.metric("Expected Package", "₹12-18 LPA")
                elif placement_probability >= 60:
                    st.metric("Expected Package", "₹8-12 LPA")
                else:
                    st.metric("Expected Package", "₹4-8 LPA")
            with col3:
                if placement_probability >= 80:
                    st.metric("Company Tier", "Tier 1")
                elif placement_probability >= 60:
                    st.metric("Company Tier", "Tier 2")
                else:
                    st.metric("Company Tier", "Tier 3")
            
            # Progress bar
            st.progress(placement_probability / 100)
            
            # Recommendations
            st.divider()
            st.write("### 📝 Recommendations to Improve")
            
            recommendations = []
            if cgpa < 8.0:
                recommendations.append("Improve your CGPA (target: 8.0+)")
            if projects_count < 2:
                recommendations.append("Complete at least 2 major projects")
            if internships_count < 1:
                recommendations.append("Secure at least 1 internship")
            if skills_count < 8:
                recommendations.append("Learn more technical skills")
            if coding_rating < 7:
                recommendations.append("Practice coding on platforms like LeetCode")
            if communication_rating < 7:
                recommendations.append("Improve communication skills through practice")
            
            if recommendations:
                st.warning("Areas for improvement:")
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.success("✅ You're on track for excellent placement!")
            
            # Save prediction
            st.session_state.student_data["placement_prediction"] = {
                "probability": placement_probability,
                "factors": {
                    "cgpa": cgpa,
                    "projects_count": projects_count,
                    "internships_count": internships_count,
                    "skills_count": skills_count,
                    "coding_rating": coding_rating,
                    "communication_rating": communication_rating
                }
            }
    
    def step7_interview_preparation(self):
        """Step 7: Interview Preparation"""
        st.subheader("🤝 Interview Preparation")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💻 Technical", "🗣️ HR", "📝 Mock Tests", "📚 Resources"])
        
        with tab1:
            st.write("### Technical Interview Preparation")
            
            # Technical topics by role
            role = st.selectbox("Select target role:", 
                               ["Software Developer", "Data Scientist", "Web Developer", 
                                "Mobile Developer", "DevOps Engineer", "Full Stack Developer"])
            
            if role:
                technical_topics = {
                    "Software Developer": ["Data Structures", "Algorithms", "OOP Concepts", "System Design", "DBMS"],
                    "Data Scientist": ["Statistics", "Machine Learning", "Python/R", "SQL", "Data Analysis"],
                    "Web Developer": ["HTML/CSS", "JavaScript", "React/Angular", "REST APIs", "Web Security"],
                    "Mobile Developer": ["Android/iOS", "React Native/Flutter", "Mobile UI/UX", "API Integration"],
                    "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS/GCP", "CI/CD"],
                    "Full Stack Developer": ["Frontend Technologies", "Backend Development", "Database", "Deployment", "Security"]
                }
                
                topics = technical_topics.get(role, [])
                st.write(f"**Key topics for {role}:**")
                for topic in topics:
                    with st.expander(f"📖 {topic}"):
                        # Simulated content - in real app, this would have detailed content
                        st.write(f"Study resources and common questions for {topic}")
                        if st.button(f"Practice {topic} Questions", key=f"practice_{topic}"):
                            st.info(f"Starting {topic} practice session...")
        
        with tab2:
            st.write("### HR Interview Preparation")
            
            common_questions = [
                "Tell me about yourself",
                "Why do you want to work for our company?",
                "What are your strengths and weaknesses?",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?",
                "Describe a challenging situation and how you handled it"
            ]
            
            for question in common_questions:
                with st.expander(f"❓ {question}"):
                    answer = st.text_area("Your answer:", key=f"hr_{question}", height=100)
                    if st.button("Get Feedback", key=f"feedback_{question}"):
                        if len(answer) > 50:
                            st.success("Good! Make sure to include specific examples.")
                        else:
                            st.warning("Try to elaborate more with specific examples.")
        
        with tab3:
            st.write("### Mock Tests")
            
            test_types = ["Aptitude Test", "Technical Test", "Coding Test", "Personality Test"]
            
            for test_type in test_types:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{test_type}**")
                    st.write("Duration: 30 mins | Questions: 20")
                with col2:
                    if st.button("Start Test", key=f"start_{test_type}"):
                        st.info(f"Starting {test_type}...")
                        # In a real app, this would launch the test
        
        with tab4:
            st.write("### Learning Resources")
            
            resources = {
                "LeetCode": "Practice coding problems",
                "HackerRank": "Coding challenges and contests",
                "GeeksforGeeks": "Technical articles and tutorials",
                "InterviewBit": "Company-specific questions",
                "Glassdoor": "Company reviews and interview experiences",
                "YouTube": "Free interview preparation videos"
            }
            
            for platform, description in resources.items():
                st.write(f"🔗 **{platform}**: {description}")
    
    def step8_placement_tracking(self):
        """Step 8: Placement Tracking"""
        st.subheader("✅ Placement Tracking")
        
        # Application tracker
        st.write("### 📋 Application Tracker")
        
        # Sample applications (in real app, this would come from database)
        applications = [
            {"company": "TechCorp", "position": "Software Engineer", "status": "Applied", "date": "2024-01-15"},
            {"company": "DataAnalytics Inc.", "position": "Data Analyst", "status": "Interview Scheduled", "date": "2024-01-20"},
            {"company": "WebCrafters", "position": "Frontend Developer", "status": "Under Review", "date": "2024-01-18"},
            {"company": "CloudSystems", "position": "DevOps Engineer", "status": "Rejected", "date": "2024-01-10"},
            {"company": "AI Innovations", "position": "ML Engineer", "status": "Offer Received", "date": "2024-01-25"}
        ]
        
        # Add new application
        with st.expander("➕ Add New Application"):
            col1, col2 = st.columns(2)
            with col1:
                new_company = st.text_input("Company Name")
                new_position = st.text_input("Position")
            with col2:
                new_status = st.selectbox("Status", ["Applied", "Under Review", "Interview Scheduled", 
                                                   "Technical Round", "HR Round", "Offer Received", "Rejected"])
                new_date = st.date_input("Application Date")
            
            if st.button("Add Application") and new_company and new_position:
                applications.append({
                    "company": new_company,
                    "position": new_position,
                    "status": new_status,
                    "date": str(new_date)
                })
                st.success("Application added!")
        
        # Display applications
        st.write("#### Your Applications")
        for app in applications:
            status_color = {
                "Applied": "blue",
                "Under Review": "orange",
                "Interview Scheduled": "green",
                "Offer Received": "darkgreen",
                "Rejected": "red"
            }.get(app["status"], "gray")
            
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color}; padding: 10px; margin: 5px 0; background-color: #f9f9f9;">
                <b>{app['company']}</b> - {app['position']}<br>
                📅 {app['date']} | 📊 Status: <b>{app['status']}</b>
            </div>
            """, unsafe_allow_html=True)
        
        # Statistics
        st.divider()
        st.write("### 📊 Placement Statistics")
        
        total_apps = len(applications)
        interviews = len([a for a in applications if "Interview" in a["status"]])
        offers = len([a for a in applications if a["status"] == "Offer Received"])
        rejections = len([a for a in applications if a["status"] == "Rejected"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Applications", total_apps)
        with col2:
            st.metric("Interviews", interviews)
        with col3:
            st.metric("Offers", offers)
        with col4:
            st.metric("Success Rate", f"{offers/total_apps*100:.1f}%" if total_apps > 0 else "0%")
        
        # Offer details
        st.divider()
        if offers > 0:
            st.write("### 🎉 Congratulations! Offer Details")
            
            offers_received = [a for a in applications if a["status"] == "Offer Received"]
            for offer in offers_received:
                with st.expander(f"Offer from {offer['company']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        package = st.number_input("Package (₹ LPA)", min_value=3.0, max_value=50.0, 
                                                 value=8.0, step=0.5, key=f"package_{offer['company']}")
                        location = st.text_input("Location", value="Bangalore", key=f"loc_{offer['company']}")
                    with col2:
                        joining_date = st.date_input("Joining Date", key=f"join_{offer['company']}")
                        st.write(f"**Position:** {offer['position']}")
                    
                    if st.button("Accept Offer", key=f"accept_{offer['company']}"):
                        st.success(f"Congratulations! You've accepted the offer from {offer['company']}!")
                        st.balloons()
        
        # Export data
        st.divider()
        if st.button("📥 Export Placement Data"):
            # Create DataFrame
            df = pd.DataFrame(applications)
            csv = df.to_csv(index=False)
            
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="placement_applications.csv",
                mime="text/csv"
            )
    
    def generate_resume_preview(self):
        """Generate a resume preview"""
        st.subheader("📄 Resume Preview")
        
        if not st.session_state.student_data["personal_info"]:
            st.warning("Please complete your profile first")
            return
        
        # Create resume HTML preview
        resume_html = f"""
        <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background-color: white;">
            <h2 style="color: #2c3e50;">{st.session_state.student_data['personal_info'].get('full_name', 'Your Name')}</h2>
            <p style="color: #7f8c8d;">{st.session_state.student_data['personal_info'].get('email', '')} | 
               {st.session_state.student_data['personal_info'].get('phone', '')} | 
               {st.session_state.student_data['personal_info'].get('address', '')}</p>
            
            <h3 style="color: #3498db; border-bottom: 2px solid #3498db;">Education</h3>
            <p><b>{st.session_state.student_data['education'].get('institution', 'University')}</b><br>
               {st.session_state.student_data['education'].get('degree', 'Degree')} - 
               CGPA: {st.session_state.student_data['education'].get('percentage', 'N/A')}</p>
            
            <h3 style="color: #3498db; border-bottom: 2px solid #3498db;">Skills</h3>
            <p>{', '.join(st.session_state.student_data.get('skills', ['No skills added']))}</p>
            
            <h3 style="color: #3498db; border-bottom: 2px solid #3498db;">Projects</h3>
        """
        
        for project in st.session_state.student_data.get("projects", []):
            resume_html += f"""
            <p><b>{project.get('name', 'Project')}</b><br>
               {project.get('description', 'Description')}<br>
               <i>Technologies: {project.get('technologies', 'N/A')}</i></p>
            """
        
        resume_html += "</div>"
        
        st.markdown(resume_html, unsafe_allow_html=True)
        
        # Download button
        if st.button("📥 Download Resume (PDF)"):
            st.info("Resume PDF generation would be implemented here")
    
    def analyze_skill_gaps(self):
        """Analyze skill gaps for career paths"""
        st.subheader("🔍 Skill Gap Analysis")
        
        if not st.session_state.student_data.get("skills"):
            st.warning("Please add your skills first")
            return
        
        student_skills = set(st.session_state.student_data["skills"])
        
        # Target roles and their required skills
        target_roles = {
            "Software Developer": ["Python", "Java", "Data Structures", "Algorithms", "Git", "SQL"],
            "Data Scientist": ["Python", "Statistics", "Machine Learning", "Data Analysis", "SQL", "Mathematics"],
            "Web Developer": ["HTML/CSS", "JavaScript", "React", "Node.js", "Git", "REST APIs"],
            "DevOps Engineer": ["Linux", "Docker", "AWS", "Kubernetes", "CI/CD", "Python"]
        }
        
        for role, required_skills in target_roles.items():
            with st.expander(f"{role} Analysis"):
                required_set = set(required_skills)
                missing_skills = required_set - student_skills
                existing_skills = student_skills.intersection(required_set)
                
                if existing_skills:
                    st.success(f"✅ You have {len(existing_skills)} matching skills")
                    st.write(f"**Your skills:** {', '.join(existing_skills)}")
                
                if missing_skills:
                    st.warning(f"📚 Need to learn {len(missing_skills)} skills")
                    st.write(f"**Missing skills:** {', '.join(missing_skills)}")
                    
                    # Learning resources
                    st.write("**Learning resources:**")
                    for skill in missing_skills:
                        st.write(f"• {skill}: Online courses, tutorials, practice projects")
                else:
                    st.success("🎉 You have all required skills for this role!")
