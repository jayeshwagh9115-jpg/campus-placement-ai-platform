import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, List, Optional

class StudentFlow:
    def __init__(self):
        self.student_data = self.initialize_student_data()
        self.current_step = 1  # Initialize with default step
    
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
    
    # ==================== DATABASE METHODS ====================
    
    def save_to_database(self, data_type: str, data: Dict) -> bool:
        """Save data to Supabase database"""
        if st.session_state.demo_mode:
            return False  # Will save to session state instead
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return False
        
        try:
            if data_type == 'student_profile':
                result = db.create_student(data)
            elif data_type == 'student_resume':
                # Store resume in student record
                student_id = self.get_current_student_id()
                if student_id:
                    result = db.update('students', student_id, {'resume_data': data})
                else:
                    return False
            elif data_type == 'application':
                result = db.create_application(data)
            elif data_type == 'interview':
                result = db.insert('interviews', data)
            else:
                return False
            
            return result is not None
        except Exception as e:
            st.error(f"Database error: {e}")
            return False
    
    def get_current_student_id(self) -> Optional[str]:
        """Get current student's ID from database"""
        if st.session_state.demo_mode:
            return None
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return None
        
        try:
            # Try to find student by email from session state
            if 'student_email' in st.session_state:
                students = db.get_students()
                student = next((s for s in students if s.get('email') == st.session_state.student_email), None)
                return student.get('id') if student else None
        except:
            return None
        return None
    
    def get_student_from_db(self, email: str) -> Optional[Dict]:
        """Get student data from database"""
        if st.session_state.demo_mode:
            return None
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return None
        
        try:
            students = db.get_students()
            return next((s for s in students if s.get('email') == email), None)
        except:
            return None
    
    def save_student_profile_to_db(self, profile_data: Dict) -> bool:
        """Save student profile to database"""
        if st.session_state.demo_mode:
            # Save to session state for demo
            if 'students' not in st.session_state:
                st.session_state.students = []
            st.session_state.students.append(profile_data)
            return True
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return False
        
        try:
            # Check if student already exists
            existing = self.get_student_from_db(profile_data.get('email'))
            if existing:
                # Update existing record
                result = db.update('students', existing['id'], profile_data)
            else:
                # Create new record
                result = db.create_student(profile_data)
            
            return result is not None
        except Exception as e:
            st.error(f"Error saving profile: {e}")
            return False
    
    def get_available_jobs_from_db(self) -> List[Dict]:
        """Get available jobs from database"""
        if st.session_state.demo_mode:
            return []
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return []
        
        try:
            return db.get_jobs()
        except:
            return []
    
    def apply_to_job(self, job_id: str, cover_letter: str = "") -> bool:
        """Apply to a job"""
        if st.session_state.demo_mode:
            return True
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return False
        
        try:
            student_id = self.get_current_student_id()
            if not student_id:
                st.error("Student profile not found. Please complete your profile first.")
                return False
            
            application_data = {
                'student_id': student_id,
                'job_id': job_id,
                'status': 'pending',
                'applied_at': datetime.now().isoformat(),
                'cover_letter': cover_letter
            }
            
            result = db.create_application(application_data)
            return result is not None
        except Exception as e:
            st.error(f"Error applying to job: {e}")
            return False
    
    def get_student_applications(self) -> List[Dict]:
        """Get applications for current student"""
        if st.session_state.demo_mode:
            return []
        
        db = st.session_state.get('db_manager')
        if not db or not db.is_connected:
            return []
        
        try:
            student_id = self.get_current_student_id()
            if student_id:
                return db.get_applications(student_id=student_id)
            return []
        except:
            return []
    
    # ==================== DISPLAY METHODS ====================
    
    def display(self):
        """Display complete student workflow"""
        st.header("👨‍🎓 Student Placement Journey")
        
        # Get current step from session state
        current_step = st.session_state.get('current_step_student', 1)
        self.current_step = current_step
        
        # Display step header
        step_names = {
            1: "🎯 Profile Creation",
            2: "📝 AI Resume Building", 
            3: "📚 NEP Course Planning",
            4: "💼 PM Internship Match",
            5: "🎯 Career Path Planning",
            6: "📊 Placement Prediction",
            7: "🤝 Interview Preparation",
            8: "✅ Placement Tracking"
        }
        
        # Create a progress header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"Step {current_step}: {step_names[current_step]}")
        with col2:
            progress = current_step / 8
            st.progress(progress)
            st.caption(f"Step {current_step} of 8")
        
        # Display database status
        if not st.session_state.demo_mode and st.session_state.get('db_manager') and st.session_state.db_manager.is_connected:
            st.success("✅ Connected to Live Database")
        
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
        
        # Display navigation at the bottom
        self.display_workflow_navigation(current_step)
    
    def step1_profile_creation(self):
        """Step 1: Student Profile Creation"""
        st.info("Create your student profile to get started with placement preparation")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*", placeholder="Enter your full name")
                roll_no = st.text_input("Roll Number*", placeholder="e.g., 20BCS001")
                email = st.text_input("Email*", placeholder="student@college.edu")
                phone = st.text_input("Phone Number", placeholder="+91 9876543210")
                
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
            
            # Career interests
            st.subheader("Career Interests")
            career_interests = st.multiselect("Areas of Interest",
                ["Software Development", "Data Science", "Product Management",
                 "Research", "Consulting", "Entrepreneurship", "Higher Studies"])
            
            if st.form_submit_button("✅ Save Profile & Continue", width='stretch'):
                # Prepare profile data
                profile_data = {
                    "full_name": name,
                    "roll_number": roll_no,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "semester": semester,
                    "cgpa": float(cgpa),
                    "backlogs": backlogs,
                    "skills": technical_skills,
                    "interests": career_interests,
                    "created_at": datetime.now().isoformat()
                }
                
                # Save to database
                success = self.save_student_profile_to_db(profile_data)
                
                if success or st.session_state.demo_mode:
                    # Save to session state
                    self.student_data["profile"] = profile_data
                    st.session_state.student_email = email  # Store email for future reference
                    
                    st.success("✅ Profile created successfully!")
                    if not st.session_state.demo_mode:
                        st.success("✅ Profile saved to database!")
                    st.balloons()
                    
                    # Update workflow step
                    st.session_state.current_step_student = 2
                    st.rerun()
                else:
                    st.error("❌ Failed to save profile to database. Please try again.")
    
    def step2_resume_building(self):
        """Step 2: AI Resume Building"""
        st.info("Build your professional resume with AI assistance")
        
        # Show profile summary if exists
        if self.student_data["profile"]:
            with st.expander("📋 Your Profile Summary", expanded=False):
                profile = self.student_data["profile"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {profile.get('full_name', 'N/A')}")
                    st.write(f"**Roll No:** {profile.get('roll_number', 'N/A')}")
                    st.write(f"**Department:** {profile.get('department', 'N/A')}")
                with col2:
                    st.write(f"**CGPA:** {profile.get('cgpa', 'N/A')}")
                    skills = profile.get('skills', [])
                    if isinstance(skills, list):
                        st.write(f"**Skills:** {', '.join(skills[:3])}")
                    else:
                        st.write(f"**Skills:** {skills}")
        
        # Simple resume builder
        st.subheader("Build Your Resume")
        
        with st.form("resume_form"):
            # Education
            st.write("**Education Details**")
            college = st.text_input("College/University", "ABC Engineering College")
            degree = st.text_input("Degree", "Bachelor of Technology")
            specialization = st.text_input("Specialization", "Computer Science")
            graduation_year = st.number_input("Graduation Year", 2020, 2030, 2024)
            
            # Projects
            st.write("**Projects**")
            project1 = st.text_input("Project 1 Title", "AI Placement Predictor")
            project1_desc = st.text_area("Project 1 Description", 
                "Developed an AI model to predict placement probability based on student profile")
            
            # Skills
            st.write("**Skills**")
            skills = st.text_area("Your Skills (comma-separated)", 
                "Python, Machine Learning, Data Analysis, SQL, Communication")
            
            # Achievements
            st.write("**Achievements**")
            achievements = st.text_area("Achievements and Awards", 
                "Dean's List, Hackathon Winner, Research Paper Published")
            
            if st.form_submit_button("💾 Generate Resume Preview", width='stretch'):
                resume_data = {
                    "education": {
                        "college": college,
                        "degree": degree,
                        "specialization": specialization,
                        "graduation_year": graduation_year
                    },
                    "projects": [
                        {"title": project1, "description": project1_desc}
                    ],
                    "skills": [s.strip() for s in skills.split(",")],
                    "achievements": [a.strip() for a in achievements.split(",")],
                    "updated_at": datetime.now().isoformat()
                }
                
                # Save to session state
                self.student_data["resume"] = resume_data
                
                # Save to database if not in demo mode
                if not st.session_state.demo_mode:
                    db_success = self.save_to_database('student_resume', resume_data)
                    if db_success:
                        st.success("✅ Resume saved to database!")
                    else:
                        st.error("❌ Failed to save resume to database")
                else:
                    st.success("✅ Resume details saved!")
        
        # Show resume preview if data exists
        if self.student_data.get("resume"):
            with st.expander("👀 Resume Preview", expanded=True):
                self.preview_resume()
    
    def preview_resume(self):
        """Preview the resume"""
        profile = self.student_data.get("profile", {})
        resume = self.student_data.get("resume", {})
        
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: white;">
            <h1 style="color: #2c3e50;">{profile.get('full_name', 'Your Name')}</h1>
            <p>{profile.get('email', 'email@example.com')} • {profile.get('phone', 'Phone')} • {profile.get('department', 'Department')}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Education</h2>
            <p><strong>{resume.get('education', {}).get('degree', 'Degree')} in {resume.get('education', {}).get('specialization', 'Specialization')}</strong></p>
            <p>{resume.get('education', {}).get('college', 'College')} • CGPA: {profile.get('cgpa', 'N/A')} • Graduation: {resume.get('education', {}).get('graduation_year', 'Year')}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Skills</h2>
            <p>{', '.join(resume.get('skills', ['Skills']))}</p>
            
            <h2 style="color: #3498db; border-bottom: 2px solid #3498db;">Projects</h2>
            <p><strong>{resume.get('projects', [{}])[0].get('title', 'Project Title')}:</strong> {resume.get('projects', [{}])[0].get('description', 'Project Description')}</p>
        </div>
        """
        
        st.markdown(html, unsafe_allow_html=True)
    
    def step3_course_planning(self):
        """Step 3: NEP Course Planning"""
        st.info("Plan your courses according to NEP 2020 guidelines")
        
        department = self.student_data["profile"].get("department", "Computer Science")
        
        st.write(f"**Recommended Course Plan for {department}**")
        
        # Simple course selection
        major_courses = st.multiselect("Major Courses",
            ["Data Structures", "Algorithms", "Database Systems", "Computer Networks", 
             "Operating Systems", "Software Engineering"],
            default=["Data Structures", "Algorithms", "Database Systems"])
        
        minor_options = ["Business Management", "Data Science", "Psychology", "Economics"]
        minor_selected = st.selectbox("Minor Specialization", minor_options)
        
        skill_courses = st.multiselect("Skill Enhancement Courses",
            ["Entrepreneurship", "Communication Skills", "Research Methodology", "Project Management"])
        
        if st.button("💾 Save Course Plan", width='stretch'):
            self.student_data["courses"] = {
                "major_courses": major_courses,
                "minor": minor_selected,
                "skill_courses": skill_courses
            }
            st.success("Course plan saved!")
    
    def step4_internship_matching(self):
        """Step 4: PM Internship Matching"""
        st.info("Find Product Management internship opportunities")
        
        # Get jobs from database
        jobs = self.get_available_jobs_from_db()
        
        if not jobs and not st.session_state.demo_mode:
            st.info("No internships available at the moment. Check back later!")
            return
        
        # If no jobs in DB, show sample data
        if not jobs and st.session_state.demo_mode:
            jobs = [
                {"id": "1", "title": "APM Intern", "company": "Google", "location": "Bangalore", "description": "Product Management Internship"},
                {"id": "2", "title": "Product Intern", "company": "Microsoft", "location": "Hyderabad", "description": "Summer Internship"},
                {"id": "3", "title": "PM Intern", "company": "Amazon", "location": "Mumbai", "description": "Product Management Role"}
            ]
        
        for job in jobs:
            with st.expander(f"{job.get('company', 'Company')} - {job.get('title', 'Role')}"):
                st.write(f"**Location:** {job.get('location', 'N/A')}")
                st.write(f"**Description:** {job.get('description', 'No description available')}")
                
                if st.button(f"Apply to {job.get('company', 'Company')}", key=f"apply_{job.get('id', '0')}", width='stretch'):
                    # Apply to job
                    success = self.apply_to_job(job.get('id', ''), f"Application for {job.get('title', '')}")
                    
                    if success or st.session_state.demo_mode:
                        st.success(f"✅ Application started for {job.get('title', 'Role')}!")
                        if not st.session_state.demo_mode:
                            st.success("✅ Application saved to database!")
                    else:
                        st.error("❌ Failed to submit application")
    
    def step5_career_planning(self):
        """Step 5: Career Path Planning"""
        st.info("Plan your career path based on your profile")
        
        profile = self.student_data.get("profile", {})
        
        st.write("**Recommended Career Paths:**")
        
        # Simple career recommendations
        interests = profile.get('interests', [])
        if isinstance(interests, str):
            interests = [interests]
        
        if "Software Development" in interests or not interests:
            with st.container():
                st.success("**Software Development Engineer**")
                st.write("Path: Junior Developer → Senior Developer → Tech Lead → Engineering Manager")
                st.write("Avg Package: 8-15 LPA (Entry) → 30-50+ LPA (Senior)")
                st.progress(0.7)
        
        if "Data Science" in interests:
            with st.container():
                st.info("**Data Scientist**")
                st.write("Path: Data Analyst → Data Scientist → Senior Data Scientist → Head of Analytics")
                st.write("Avg Package: 6-12 LPA (Entry) → 25-40+ LPA (Senior)")
                st.progress(0.6)
        
        # Career goal setting
        st.subheader("Set Your Career Goals")
        target_role = st.text_input("Target Role", "Software Development Engineer")
        timeline = st.selectbox("Timeline", ["6 months", "1 year", "2 years", "3 years"])
        
        if st.button("🎯 Save Career Goals", width='stretch'):
            self.student_data["career_plan"] = {
                "target_role": target_role,
                "timeline": timeline,
                "set_date": datetime.now().isoformat()
            }
            st.success("Career goals saved!")
    
    def step6_placement_prediction(self):
        """Step 6: Placement Prediction"""
        st.info("Predict your placement probability")
        
        profile = self.student_data.get("profile", {})
        
        # Simple prediction based on CGPA
        cgpa = profile.get("cgpa", 7.0)
        if cgpa >= 8.5:
            probability = "85-95%"
            recommendation = "🎉 Excellent! High chance of placement in top companies"
            color = "green"
        elif cgpa >= 7.5:
            probability = "70-85%"
            recommendation = "📈 Good potential with proper preparation"
            color = "blue"
        elif cgpa >= 6.5:
            probability = "50-70%"
            recommendation = "📚 Needs focused effort and skill improvement"
            color = "orange"
        else:
            probability = "30-50%"
            recommendation = "🎯 Requires immediate action on academics and skills"
            color = "red"
        
        # Display metric with color
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f8f9fa;">
            <h1 style="color: {color}; font-size: 48px; margin: 0;">{probability}</h1>
            <p style="font-size: 18px; margin: 10px 0 0 0;">Placement Probability</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(recommendation)
        
        # Save prediction
        self.student_data["placement_prediction"] = {
            "probability": probability,
            "recommendation": recommendation,
            "calculated_date": datetime.now().isoformat()
        }
        
        # Show applications if any
        applications = self.get_student_applications()
        if applications:
            st.subheader("📋 Your Applications")
            for app in applications:
                status = app.get('status', 'pending')
                status_color = {
                    'pending': '🟡',
                    'accepted': '🟢',
                    'rejected': '🔴',
                    'interview': '🔵'
                }.get(status, '⚪')
                
                st.write(f"{status_color} {app.get('job_title', 'Job')} - {status}")
    
    def step7_interview_preparation(self):
        """Step 7: Interview Preparation"""
        st.info("Prepare for technical and HR interviews")
        
        # Show upcoming interviews from database
        if not st.session_state.demo_mode:
            applications = self.get_student_applications()
            upcoming_interviews = [app for app in applications if app.get('status') == 'interview']
            
            if upcoming_interviews:
                st.subheader("📅 Upcoming Interviews")
                for interview in upcoming_interviews:
                    st.info(f"**{interview.get('job_title', 'Job')}** - Scheduled")
        
        st.write("**Common Interview Questions:**")
        
        questions = [
            "Tell me about yourself",
            "Why do you want to work here?",
            "What are your strengths and weaknesses?",
            "Explain a challenging project you worked on"
        ]
        
        for q in questions:
            with st.expander(f"❓ {q}"):
                answer = st.text_area("Your Answer", key=f"answer_{q}", height=100)
                if st.button("Get AI Feedback", key=f"feedback_{q}", width='stretch'):
                    st.info("""
                    **AI Feedback:**
                    - Structure your answer clearly
                    - Provide specific examples
                    - Connect to the company's values
                    - Practice with mock interviews
                    """)
    
    def step8_placement_tracking(self):
        """Step 8: Placement Tracking"""
        st.success("🎉 Congratulations! You've completed your placement journey")
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Profile", "✅ Complete")
        with col2:
            st.metric("Resume", "✅ Built")
        with col3:
            st.metric("Career Plan", "✅ Set")
        
        # Show real applications if any
        if not st.session_state.demo_mode:
            applications = self.get_student_applications()
            if applications:
                st.subheader("📊 Your Application Status")
                status_counts = {}
                for app in applications:
                    status = app.get('status', 'pending')
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                for status, count in status_counts.items():
                    st.write(f"• {status.title()}: {count}")
        
        # Final recommendations
        st.subheader("🎯 Final Recommendations")
        st.write("1. ✅ Continue skill development")
        st.write("2. ✅ Network with professionals")
        st.write("3. ✅ Prepare for interviews")
        st.write("4. ✅ Stay updated with industry trends")
        
        # Database connection status
        if not st.session_state.demo_mode:
            st.info("💾 Your data is saved in the cloud database!")
        
        # Restart option
        if st.button("🔄 Start New Journey", width='stretch'):
            self.student_data = self.initialize_student_data()
            st.session_state.current_step_student = 1
            st.rerun()
    
    def display_workflow_navigation(self, current_step):
        """Display navigation buttons"""
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_step > 1 and st.button("⬅️ Previous Step", width='stretch'):
                st.session_state.current_step_student = current_step - 1
                st.rerun()
        
        with col3:
            if current_step < 8 and st.button("Next Step ➡️", width='stretch'):
                st.session_state.current_step_student = current_step + 1
                st.rerun()
        
        # Add database status in the middle column
        with col2:
            if not st.session_state.demo_mode and st.session_state.get('db_manager') and st.session_state.db_manager.is_connected:
                st.caption("💾 Connected to Live Database")
            elif st.session_state.demo_mode:
                st.caption("⚠️ Demo Mode - Data not saved")
