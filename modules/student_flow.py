import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

class StudentFlow:
    def __init__(self):
        self.student_data = self.initialize_student_data()
        self.current_step = 1
    
    def initialize_student_data(self):
        """Initialize student profile data"""
        return {
            "profile": {},
            "resume": {},
            "courses": {},
            "internships": [],
            "career_plan": {},
            "placement_prediction": {},
            "interviews": [],
            "placement_status": {}
        }
    
    def display(self):
        """Display complete student workflow"""
        st.header("👨‍🎓 Student Placement Journey")
        
        # Get current step from workflow manager
        from modules.workflow_manager import WorkflowManager
        workflow = WorkflowManager()
        current_step = workflow.workflows["student"]["current_step"]
        
        # Display appropriate step
        if current_step == 1:
            self.step1_profile_creation()
        elif current_step == 2:
            self.step2_resume_building()
        elif current_step == 3:
            self.step3_course_planning()
        elif current_step == 4:
            self.step4_internship_matching()
        elif current_step == 5:
            self.step5_career_planning()
        elif current_step == 6:
            self.step6_placement_prediction()
        elif current_step == 7:
            self.step7_interview_preparation()
        elif current_step == 8:
            self.step8_placement_tracking()
    
    def step1_profile_creation(self):
        """Step 1: Student Profile Creation"""
        st.subheader("🎯 Step 1: Create Your Profile")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*")
                roll_no = st.text_input("Roll Number*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number")
                
            with col2:
                department = st.selectbox("Department*", 
                    ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                     "Civil Engineering", "Information Technology", "Electronics"])
                semester = st.number_input("Current Semester*", 1, 10, 6)
                cgpa = st.number_input("Current CGPA*", 0.0, 10.0, 8.0, 0.1)
                backlogs = st.number_input("Number of Backlogs", 0, 10, 0)
            
            # Skills assessment
            st.subheader("Skills Assessment")
            technical_skills = st.multiselect("Technical Skills",
                ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL",
                 "Machine Learning", "Data Analysis", "AWS", "Docker", "Git"],
                default=["Python", "SQL"])
            
            soft_skills = st.multiselect("Soft Skills",
                ["Communication", "Leadership", "Teamwork", "Problem Solving",
                 "Time Management", "Adaptability", "Creativity"],
                default=["Communication", "Teamwork"])
            
            # Career interests
            st.subheader("Career Interests")
            career_interests = st.multiselect("Areas of Interest",
                ["Software Development", "Data Science", "Product Management",
                 "Research", "Consulting", "Entrepreneurship", "Higher Studies"])
            
            target_companies = st.text_input("Target Companies (comma-separated)")
            preferred_location = st.multiselect("Preferred Location",
                ["Metro Cities", "Tier 2 Cities", "Remote", "International"])
            
            if st.form_submit_button("✅ Save Profile & Continue"):
                # Save profile data
                self.student_data["profile"] = {
                    "name": name,
                    "roll_no": roll_no,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "semester": semester,
                    "cgpa": cgpa,
                    "backlogs": backlogs,
                    "technical_skills": technical_skills,
                    "soft_skills": soft_skills,
                    "career_interests": career_interests,
                    "target_companies": [c.strip() for c in target_companies.split(",")] if target_companies else [],
                    "preferred_location": preferred_location,
                    "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                st.success("Profile created successfully! Moving to Resume Building...")
                st.balloons()
                # Update workflow step
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = 2
                st.rerun()
    
    def step2_resume_building(self):
        """Step 2: AI Resume Building"""
        st.subheader("📝 Step 2: AI-Powered Resume Building")
        
        # Show profile summary
        if self.student_data["profile"]:
            with st.expander("📋 Your Profile Summary", expanded=True):
                profile = self.student_data["profile"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {profile['name']}")
                    st.write(f"**Roll No:** {profile['roll_no']}")
                    st.write(f"**Department:** {profile['department']}")
                    st.write(f"**CGPA:** {profile['cgpa']}")
                with col2:
                    st.write(f"**Technical Skills:** {', '.join(profile['technical_skills'][:5])}")
                    st.write(f"**Career Interests:** {', '.join(profile['career_interests'])}")
        
        # Resume builder interface
        st.subheader("Build Your Resume")
        
        tab1, tab2, tab3 = st.tabs(["📋 Fill Details", "🤖 AI Suggestions", "👀 Preview"])
        
        with tab1:
            with st.form("resume_details_form"):
                # Education details
                st.markdown("### Education Details")
                college = st.text_input("College/University*", "Indian Institute of Technology")
                degree = st.text_input("Degree*", "Bachelor of Technology")
                specialization = st.text_input("Specialization*", "Computer Science and Engineering")
                graduation_year = st.number_input("Graduation Year*", 2020, 2030, 2024)
                
                # Projects
                st.markdown("### Academic Projects")
                project_count = st.number_input("Number of Projects", 0, 5, 2)
                
                projects = []
                for i in range(project_count):
                    with st.expander(f"Project {i+1}", expanded=i==0):
                        proj_title = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
                        proj_desc = st.text_area(f"Description {i+1}", 
                            key=f"proj_desc_{i}",
                            height=100,
                            value="• Developed a [technology] application for [purpose]\n• Implemented [key features]\n• Technologies used: [list technologies]")
                        projects.append({"title": proj_title, "description": proj_desc})
                
                # Achievements
                st.markdown("### Achievements & Extracurricular")
                achievements = st.text_area("Achievements (one per line)",
                    value="• Won coding competition 2023\n• Published research paper\n• Volunteer at tech community")
                
                if st.form_submit_button("💾 Save Resume Details"):
                    self.student_data["resume"] = {
                        "education": {
                            "college": college,
                            "degree": degree,
                            "specialization": specialization,
                            "graduation_year": graduation_year
                        },
                        "projects": projects,
                        "achievements": achievements.split("\n") if achievements else []
                    }
                    st.success("Resume details saved!")
        
        with tab2:
            st.info("🤖 AI Resume Optimization")
            
            if self.student_data.get("resume"):
                # Show AI suggestions
                st.write("**AI Suggestions for Your Resume:**")
                
                suggestions = [
                    "✅ **Add quantifiable metrics:** Instead of 'worked on project', use 'improved performance by 30%'",
                    "✅ **Use action verbs:** Start bullet points with words like 'Developed', 'Implemented', 'Optimized'",
                    "✅ **Tailor for target roles:** Add keywords from your target job descriptions",
                    "✅ **Highlight achievements:** Move accomplishments to the top",
                    "✅ **Keep it concise:** Aim for 1-2 pages maximum"
                ]
                
                for suggestion in suggestions:
                    st.write(suggestion)
                
                if st.button("🔄 Apply AI Suggestions"):
                    st.success("AI suggestions applied to your resume!")
            else:
                st.warning("Please fill resume details first")
        
        with tab3:
            if self.student_data.get("resume"):
                # Show resume preview
                self.preview_resume()
            else:
                st.info("Complete resume details to see preview")
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Back to Profile"):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = 1
                st.rerun()
        
        with col3:
            if st.button("Continue to Course Planning ➡️"):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = 3
                st.rerun()
    
    def preview_resume(self):
        """Preview the resume"""
        profile = self.student_data["profile"]
        resume = self.student_data["resume"]
        
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h1 style="color: #2c3e50;">{profile['name']}</h1>
            <p>{profile['email']} • {profile['phone']} • {profile['department']}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Education</h2>
            <p><strong>{resume['education']['degree']} in {resume['education']['specialization']}</strong></p>
            <p>{resume['education']['college']} • CGPA: {profile['cgpa']} • Graduation: {resume['education']['graduation_year']}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Skills</h2>
            <p><strong>Technical:</strong> {', '.join(profile['technical_skills'])}</p>
            <p><strong>Soft Skills:</strong> {', '.join(profile['soft_skills'])}</p>
        """
        
        if resume.get("projects"):
            html += "<h2 style='color: #3498db; border-bottom: 2px solid #3498db;'>Projects</h2>"
            for proj in resume["projects"]:
                html += f"<p><strong>{proj['title']}</strong><br>{proj['description'].replace('•', '•')}</p>"
        
        html += "</div>"
        
        st.markdown(html, unsafe_allow_html=True)
    
    def step3_course_planning(self):
        """Step 3: NEP Course Planning"""
        st.subheader("📚 Step 3: NEP-Aligned Course Planning")
        
        st.info("""
        **National Education Policy 2020 Guidelines:**
        - Multidisciplinary education
        - Multiple entry/exit options
        - Credit-based flexible system
        - Major + Minor combination
        """)
        
        # Get student's department
        department = self.student_data["profile"].get("department", "Computer Science")
        
        # NEP Course recommendations
        nep_recommendations = {
            "Computer Science": {
                "major_courses": ["Data Structures", "Algorithms", "Database Systems", 
                                 "Computer Networks", "Operating Systems", "Software Engineering"],
                "minor_options": [
                    {"name": "Business Management", "courses": ["Economics", "Marketing", "Finance"]},
                    {"name": "Data Science", "courses": ["Statistics", "Machine Learning", "Data Visualization"]},
                    {"name": "Psychology", "courses": ["Cognitive Science", "Human-Computer Interaction"]}
                ],
                "skill_courses": ["Entrepreneurship", "Communication Skills", "Research Methodology"]
            },
            "Electrical Engineering": {
                "major_courses": ["Circuit Theory", "Electronics", "Power Systems", 
                                 "Control Systems", "Signals & Systems"],
                "minor_options": [
                    {"name": "Computer Science", "courses": ["Programming", "Data Structures", "Algorithms"]},
                    {"name": "Renewable Energy", "courses": ["Solar Energy", "Wind Energy", "Energy Management"]}
                ],
                "skill_courses": ["Project Management", "Technical Writing", "IoT Basics"]
            }
        }
        
        recommendations = nep_recommendations.get(department, nep_recommendations["Computer Science"])
        
        # Display course planning interface
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Major Courses (Core)")
            for course in recommendations["major_courses"]:
                st.checkbox(course, value=True)
            
            st.subheader("Skill Enhancement Courses")
            for course in recommendations["skill_courses"]:
                st.checkbox(course)
        
        with col2:
            st.subheader("Minor Specialization")
            minor_selected = st.selectbox("Choose Minor",
                [m["name"] for m in recommendations["minor_options"]])
            
            # Show courses for selected minor
            selected_minor = next((m for m in recommendations["minor_options"] 
                                 if m["name"] == minor_selected), None)
            
            if selected_minor:
                st.write(f"**Courses in {minor_selected}:**")
                for course in selected_minor["courses"]:
                    st.checkbox(course)
        
        # Credit calculator
        st.subheader("📊 Credit Calculator")
        total_credits = st.slider("Target Total Credits", 120, 200, 160)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            major_credits = st.number_input("Major Credits", 0, 100, 80)
        with col2:
            minor_credits = st.number_input("Minor Credits", 0, 60, 40)
        with col3:
            skill_credits = st.number_input("Skill Credits", 0, 40, 20)
        
        remaining = total_credits - (major_credits + minor_credits + skill_credits)
        
        if remaining == 0:
            st.success(f"✅ Perfect! {total_credits} credits planned")
        elif remaining > 0:
            st.warning(f"⚠️ Need {remaining} more credits")
        else:
            st.error(f"❌ {abs(remaining)} credits over limit")
        
        # Save course plan
        if st.button("💾 Save Course Plan"):
            self.student_data["courses"] = {
                "major_courses": recommendations["major_courses"],
                "minor_selected": minor_selected,
                "minor_courses": selected_minor["courses"] if selected_minor else [],
                "skill_courses": recommendations["skill_courses"],
                "credits": {
                    "total": total_credits,
                    "major": major_credits,
                    "minor": minor_credits,
                    "skill": skill_credits
                }
            }
            st.success("Course plan saved!")
        
        # Navigation
        self.display_workflow_navigation(3)
    
    def step4_internship_matching(self):
        """Step 4: PM Internship Matching"""
        st.subheader("💼 Step 4: PM Internship Opportunities")
        
        # Show student's profile for context
        profile = self.student_data["profile"]
        
        # PM Internship opportunities
        internships = [
            {
                "company": "Google", 
                "role": "APM Intern",
                "location": "Bangalore",
                "duration": "3 months",
                "stipend": "₹80,000/month",
                "requirements": "Strong analytical skills, SQL, 3rd/4th year",
                "match_score": 85
            },
            {
                "company": "Microsoft", 
                "role": "Product Intern",
                "location": "Hyderabad",
                "duration": "6 months",
                "stipend": "₹70,000/month",
                "requirements": "Product thinking, communication skills",
                "match_score": 78
            },
            {
                "company": "Amazon", 
                "role": "Product Management Intern",
                "location": "Mumbai",
                "duration": "4 months",
                "stipend": "₹65,000/month",
                "requirements": "Technical background, customer obsession",
                "match_score": 72
            }
        ]
        
        # Display internships with match scores
        st.subheader("Recommended PM Internships")
        
        for intern in internships:
            with st.expander(f"{intern['company']} - {intern['role']} (Match: {intern['match_score']}%)", 
                           expanded=intern['match_score'] > 80):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Location:** {intern['location']}")
                    st.write(f"**Duration:** {intern['duration']}")
                    st.write(f"**Stipend:** {intern['stipend']}")
                with col2:
                    st.write(f"**Requirements:** {intern['requirements']}")
                    st.write(f"**Match Score:** {intern['match_score']}%")
                
                # Show why it matches
                st.info(f"**Why this matches you:** CGPA {profile['cgpa']}+, Skills: {', '.join(profile['technical_skills'][:3])}")
                
                if st.button(f"Apply to {intern['company']}", key=f"apply_{intern['company']}"):
                    st.success(f"Application started for {intern['role']} at {intern['company']}!")
                    self.student_data.setdefault("internships", []).append({
                        "company": intern["company"],
                        "role": intern["role"],
                        "applied_date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Applied"
                    })
        
        # PM Skill assessment
        st.subheader("🤖 PM Skill Gap Analysis")
        
        pm_skills = ["Product Strategy", "User Research", "Data Analysis", 
                    "Stakeholder Management", "Roadmapping", "A/B Testing"]
        
        user_skill_levels = {}
        for skill in pm_skills:
            user_skill_levels[skill] = st.select_slider(
                skill,
                options=["Beginner", "Intermediate", "Advanced"],
                value="Beginner"
            )
        
        # Calculate PM readiness score
        if st.button("🔍 Calculate PM Readiness"):
            score_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
            total_score = sum(score_map[level] for level in user_skill_levels.values())
            max_score = len(pm_skills) * 3
            readiness = (total_score / max_score) * 100
            
            st.subheader(f"PM Readiness Score: {readiness:.1f}%")
            st.progress(readiness / 100)
            
            if readiness < 50:
                st.error("**Focus Areas:** Improve Product Strategy and Data Analysis skills")
            elif readiness < 75:
                st.warning("**Good Progress:** Work on Stakeholder Management")
            else:
                st.success("**Ready for PM roles!** Focus on interview preparation")
        
        self.display_workflow_navigation(4)
    
    def step5_career_planning(self):
        """Step 5: Career Path Planning"""
        st.subheader("🎯 Step 5: Career Path Planning")
        
        profile = self.student_data["profile"]
        
        # Career path recommendations based on profile
        career_paths = {
            "Software Development": {
                "entry": ["Software Engineer", "Frontend Developer", "Backend Developer"],
                "mid": ["Senior Developer", "Tech Lead", "Architect"],
                "senior": ["Engineering Manager", "CTO"],
                "skills_match": len(set(profile["technical_skills"]) & {"Python", "Java", "JavaScript", "React"}),
                "salary_range": "8-15 LPA (Entry) → 30-50+ LPA (Senior)",
                "growth": "High"
            },
            "Data Science": {
                "entry": ["Data Analyst", "Business Analyst", "Junior Data Scientist"],
                "mid": ["Data Scientist", "ML Engineer"],
                "senior": ["Lead Data Scientist", "Head of Analytics"],
                "skills_match": len(set(profile["technical_skills"]) & {"Python", "SQL", "Machine Learning", "Statistics"}),
                "salary_range": "6-12 LPA (Entry) → 25-40+ LPA (Senior)",
                "growth": "Very High"
            },
            "Product Management": {
                "entry": ["Associate Product Manager", "Product Analyst"],
                "mid": ["Product Manager", "Senior PM"],
                "senior": ["Director of Product", "VP Product"],
                "skills_match": len(set(profile["technical_skills"]) & {"SQL", "Data Analysis"}) + 
                              len(set(profile["soft_skills"]) & {"Communication", "Leadership"}),
                "salary_range": "10-18 LPA (Entry) → 40-70+ LPA (Senior)",
                "growth": "High"
            }
        }
        
        # Display career paths
        st.subheader("Recommended Career Paths")
        
        for career, details in career_paths.items():
            match_percentage = (details["skills_match"] / 8) * 100
            
            with st.expander(f"{career} (Match: {match_percentage:.0f}%)", 
                           expanded=match_percentage > 70):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Career Progression:**")
                    st.write(f"• **Entry:** {', '.join(details['entry'][:2])}")
                    st.write(f"• **Mid:** {', '.join(details['mid'][:2])}")
                    st.write(f"• **Senior:** {', '.join(details['senior'][:2])}")
                
                with col2:
                    st.write(f"**Salary Range:** {details['salary_range']}")
                    st.write(f"**Growth Potential:** {details['growth']}")
                    st.write(f"**Skills Match:** {match_percentage:.0f}%")
                
                # Action plan
                st.info(f"""
                **Action Plan for {career}:**
                1. Complete 2-3 projects in this domain
                2. Get relevant certifications
                3. Network with professionals
                4. Apply for entry-level roles
                """)
        
        # Career goal setting
        st.subheader("🎯 Set Your Career Goals")
        
        with st.form("career_goals_form"):
            target_role = st.selectbox("Target Role in 1-2 years",
                ["Software Development Engineer", "Data Scientist", 
                 "Product Manager", "Consultant", "Researcher"])
            
            timeline = st.select_slider("Target Timeline",
                options=["6 months", "1 year", "2 years", "3 years", "5 years"],
                value="2 years")
            
            target_salary = st.number_input("Target Salary (LPA)", 5.0, 50.0, 15.0, 1.0)
            
            if st.form_submit_button("💾 Save Career Goals"):
                self.student_data["career_plan"] = {
                    "target_role": target_role,
                    "timeline": timeline,
                    "target_salary": target_salary,
                    "set_date": datetime.now().strftime("%Y-%m-%d")
                }
                st.success("Career goals saved!")
        
        self.display_workflow_navigation(5)
    
    def step6_placement_prediction(self):
        """Step 6: Placement Prediction"""
        st.subheader("📊 Step 6: Placement Probability Prediction")
        
        profile = self.student_data["profile"]
        
        # Placement prediction factors
        st.subheader("Your Placement Factors")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("CGPA", f"{profile['cgpa']}/10.0", 
                     delta="+15%" if profile['cgpa'] > 8.0 else "-5%" if profile['cgpa'] < 7.0 else "Average")
            
            st.metric("Technical Skills", f"{len(profile['technical_skills'])}", 
                     delta="Strong" if len(profile['technical_skills']) > 5 else "Needs work")
        
        with col2:
            st.metric("Backlogs", profile['backlogs'], 
                     delta="Critical" if profile['backlogs'] > 2 else "Good" if profile['backlogs'] == 0 else "Warning")
            
            st.metric("Soft Skills", f"{len(profile['soft_skills'])}", 
                     delta="Good" if len(profile['soft_skills']) > 3 else "Develop more")
        
        # Calculate placement probability
        st.subheader("🎯 Placement Probability Calculator")
        
        # Interactive factors
        cgpa_weight = st.slider("CGPA Weight", 0.0, 1.0, 0.3, 0.05)
        skills_weight = st.slider("Skills Weight", 0.0, 1.0, 0.25, 0.05)
        projects_weight = st.slider("Projects Weight", 0.0, 1.0, 0.2, 0.05)
        internships_weight = st.slider("Internships Weight", 0.0, 1.0, 0.15, 0.05)
        backlogs_penalty = st.slider("Backlogs Penalty", 0.0, 0.5, 0.1, 0.05)
        
        # Calculate score
        cgpa_score = (profile['cgpa'] / 10.0) * cgpa_weight
        skills_score = (min(len(profile['technical_skills']), 10) / 10.0) * skills_weight
        projects_score = (len(self.student_data.get("resume", {}).get("projects", [])) / 5.0) * projects_weight
        internships_score = (len(self.student_data.get("internships", [])) / 3.0) * internships_weight
        backlogs_score = max(0, 1 - (profile['backlogs'] * backlogs_penalty))
        
        total_score = (cgpa_score + skills_score + projects_score + internships_score) * backlogs_score
        placement_probability = min(100, total_score * 100)
        
        # Display result
        st.subheader(f"Predicted Placement Probability: {placement_probability:.1f}%")
        st.progress(placement_probability / 100)
        
        # Interpretation
        if placement_probability >= 80:
            st.success("🎉 **Excellent!** High chance of placement in top companies")
            st.info("**Focus:** Interview preparation, company research")
        elif placement_probability >= 60:
            st.warning("📈 **Good Potential** Strong chance with preparation")
            st.info("**Focus:** Skill improvement, project building")
        elif placement_probability >= 40:
            st.info("📚 **Needs Work** Can improve with focused effort")
            st.info("**Focus:** CGPA improvement, skill development")
        else:
            st.error("🎯 **Requires Immediate Action**")
            st.info("**Focus:** Academic improvement, basic skill building")
        
        # Save prediction
        self.student_data["placement_prediction"] = {
            "probability": placement_probability,
            "factors": {
                "cgpa": cgpa_score,
                "skills": skills_score,
                "projects": projects_score,
                "internships": internships_score,
                "backlogs_impact": backlogs_score
            },
            "calculated_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.display_workflow_navigation(6)
    
    def step7_interview_preparation(self):
        """Step 7: Interview Preparation"""
        st.subheader("🤝 Step 7: Interview Preparation")
        
        st.info("Prepare for technical and HR interviews with AI-powered tools")
        
        # Interview preparation modules
        tab1, tab2, tab3 = st.tabs(["💻 Technical Prep", "🗣️ HR Interview", "🎯 Mock Interviews"])
        
        with tab1:
            st.subheader("Technical Interview Preparation")
            
            # Technical topics based on career interests
            career_interests = self.student_data["profile"].get("career_interests", [])
            
            technical_topics = {
                "Software Development": ["Data Structures", "Algorithms", "System Design", "OOP", "Databases"],
                "Data Science": ["Statistics", "Machine Learning", "SQL", "Python", "Case Studies"],
                "Product Management": ["Product Design", "Case Studies", "Analytics", "Strategy", "Behavioral"]
            }
            
            selected_topics = []
            for interest in career_interests:
                if interest in technical_topics:
                    selected_topics.extend(technical_topics[interest][:3])
            
            if selected_topics:
                st.write("**Recommended Topics:**")
                for topic in set(selected_topics):
                    with st.expander(f"📚 {topic}"):
                        st.write(f"**Common Questions:**")
                        st.write(f"• Explain {topic} concepts")
                        st.write(f"• Solve {topic} problems")
                        st.write(f"• Real-world applications")
                        
                        if st.button(f"Practice {topic}", key=f"practice_{topic}"):
                            st.info(f"Opening {topic} practice problems...")
            else:
                st.write("Select career interests in Profile to get topic recommendations")
        
        with tab2:
            st.subheader("HR Interview Preparation")
            
            hr_questions = [
                "Tell me about yourself",
                "Why do you want to work here?",
                "What are your strengths and weaknesses?",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?"
            ]
            
            for question in hr_questions:
                with st.expander(f"❓ {question}"):
                    st.text_area("Your Answer", key=f"hr_answer_{question}", height=100)
                    
                    if st.button(f"Get AI Feedback", key=f"feedback_{question}"):
                        st.success("""
                        **AI Feedback:**
                        - Structure your answer clearly
                        - Provide specific examples
                        - Connect to the company's values
                        - Keep it concise (1-2 minutes)
                        """)
        
        with tab3:
            st.subheader("Mock Interview Scheduler")
            
            # Mock interview slots
            interview_slots = [
                {"date": "2024-03-20", "time": "10:00 AM", "type": "Technical", "mentor": "Senior Engineer"},
                {"date": "2024-03-21", "time": "2:00 PM", "type": "HR", "mentor": "HR Manager"},
                {"date": "2024-03-22", "time": "4:00 PM", "type": "Product", "mentor": "Product Manager"}
            ]
            
            for slot in interview_slots:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{slot['type']} Interview** with {slot['mentor']}")
                    st.write(f"{slot['date']} at {slot['time']}")
                with col3:
                    if st.button("Book", key=f"book_{slot['date']}_{slot['time']}"):
                        st.success(f"Booked {slot['type']} interview!")
                        self.student_data.setdefault("interviews", []).append({
                            "type": slot["type"],
                            "date": slot["date"],
                            "time": slot["time"],
                            "mentor": slot["mentor"],
                            "status": "Scheduled"
                        })
        
        self.display_workflow_navigation(7)
    
    def step8_placement_tracking(self):
        """Step 8: Placement Tracking"""
        st.subheader("✅ Step 8: Placement Tracking & Results")
        
        # Summary of journey
        st.success("🎉 **Congratulations! You've completed your placement journey**")
        
        # Display journey summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Profile Completed", "✅")
            st.metric("Resume Built", "✅")
        
        with col2:
            st.metric("Course Planned", "✅")
            st.metric("Internships Applied", len(self.student_data.get("internships", [])))
        
        with col3:
            st.metric("Career Plan Set", "✅" if self.student_data.get("career_plan") else "⏳")
            st.metric("Placement Probability", f"{self.student_data.get('placement_prediction', {}).get('probability', 0):.1f}%")
        
        # Placement status tracking
        st.subheader("📊 Your Placement Status")
        
        # Mock placement offers (in real app, this would come from database)
        placement_offers = [
            {"company": "Google", "role": "Software Engineer", "package": "18 LPA", "status": "Final Round"},
            {"company": "Microsoft", "role": "Product Intern", "package": "70,000/month", "status": "Offer Received"},
            {"company": "Amazon", "role": "SDE Intern", "package": "65,000/month", "status": "Interview Scheduled"}
        ]
        
        for offer in placement_offers:
            with st.expander(f"{offer['company']} - {offer['role']} ({offer['status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Role:** {offer['role']}")
                    st.write(f"**Package:** {offer['package']}")
                with col2:
                    st.write(f"**Status:** {offer['status']}")
                    if offer['status'] == "Offer Received":
                        st.success("🎊 Congratulations!")
                    elif offer['status'] == "Final Round":
                        st.warning("Last round - Prepare well!")
                    else:
                        st.info("Upcoming - Good luck!")
        
        # Final recommendations
        st.subheader("🎯 Final Recommendations")
        
        recommendations = [
            "✅ **Continue skill development** even after placement",
            "✅ **Network with alumni** in your target companies",
            "✅ **Prepare for onboarding** and first 90 days",
            "✅ **Consider higher studies** if aligned with long-term goals",
            "✅ **Give back** by mentoring juniors"
        ]
        
        for rec in recommendations:
            st.write(rec)
        
        # Export journey data
        if st.button("📥 Export Placement Journey Report"):
            st.success("Report generated! (In production, this would create a PDF report)")
        
        # Restart journey or view dashboard
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Start New Journey"):
                # Reset student data
                self.student_data = self.initialize_student_data()
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = 1
                st.rerun()
        
        with col2:
            if st.button("📈 View Analytics Dashboard"):
                st.info("Opening dashboard...")
    
    def display_workflow_navigation(self, current_step):
        """Display navigation buttons for workflow"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_step > 1 and st.button("⬅️ Previous Step"):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = current_step - 1
                st.rerun()
        
        with col3:
            if current_step < 8 and st.button("Next Step ➡️"):
                from modules.workflow_manager import WorkflowManager
                workflow = WorkflowManager()
                workflow.workflows["student"]["current_step"] = current_step + 1
                st.rerun()
