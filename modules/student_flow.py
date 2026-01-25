import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import json
import traceback

class StudentFlow:
    def __init__(self):
        self.current_step = 1
        self.total_steps = 8
        self.db_manager = None
        self.demo_mode = True
        
        # Initialize student data structure for all 8 steps
        self.student_data = {
            "profile": {
                "full_name": "",
                "email": "",
                "phone": "",
                "college_id": "",
                "roll_number": "",
                "department": "",
                "year": "",
                "cgpa": 0.0,
                "backlogs": 0,
                "skills": [],
                "technical_skills": [],
                "career_interests": [],
                "resume_url": "",
                "profile_picture_url": "",
                "portfolio_link": "",
                "linkedin_profile": "",
                "github_profile": "",
                "semester": 6
            },
            "education": [],
            "resume": {},
            "courses": {},
            "projects": [],
            "internships": [],
            "certifications": [],
            "career_plan": {},
            "placement_prediction": {},
            "interview_preparation": {},
            "job_applications": [],
            "placement_status": {}
        }
        
        # Load demo data if no db connection
        if self.demo_mode:
            self.load_demo_data()
    
    def set_database_manager(self, db_manager, demo_mode=False):
        """Set the database manager for this flow"""
        self.db_manager = db_manager
        self.demo_mode = demo_mode
        
        # If we have a db manager, try to load data
        if not self.demo_mode and self.db_manager:
            self.load_from_database()
        else:
            self.load_demo_data()
    
    def load_demo_data(self):
        """Load demo data for testing"""
        self.student_data = {
            "profile": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+91 9876543210",
                "college_id": "IITB2023",
                "roll_number": "2023CS001",
                "department": "Computer Science",
                "year": "Final Year",
                "semester": 8,
                "cgpa": 8.5,
                "backlogs": 0,
                "skills": ["Python", "Java", "SQL", "React", "Machine Learning"],
                "technical_skills": ["Python", "Machine Learning", "Data Analysis", "SQL"],
                "career_interests": ["Software Development", "Data Science", "Product Management"],
                "resume_url": "",
                "profile_picture_url": "https://randomuser.me/api/portraits/men/32.jpg",
                "portfolio_link": "https://johndoe.dev",
                "linkedin_profile": "https://linkedin.com/in/johndoe",
                "github_profile": "https://github.com/johndoe"
            },
            "education": [
                {
                    "degree": "B.Tech Computer Science",
                    "institution": "IIT Bombay",
                    "year": "2023",
                    "percentage": 85.5,
                    "description": "Major in AI and Machine Learning"
                }
            ],
            "resume": {
                "education": {
                    "college": "IIT Bombay",
                    "degree": "Bachelor of Technology",
                    "specialization": "Computer Science",
                    "graduation_year": 2024
                },
                "projects": [
                    {
                        "title": "AI-Powered Placement Platform",
                        "description": "Developed a full-stack platform for campus placements",
                        "technologies": ["Python", "Streamlit", "Supabase", "Machine Learning"]
                    }
                ],
                "skills": ["Python", "Machine Learning", "Data Analysis", "SQL"]
            },
            "courses": {
                "major_courses": ["Data Structures", "Algorithms", "Database Systems"],
                "minor": "Data Science",
                "skill_courses": ["Entrepreneurship", "Communication Skills"]
            },
            "projects": [
                {
                    "title": "AI-Powered Placement Platform",
                    "description": "Developed a full-stack platform for campus placements",
                    "technologies": ["Python", "Streamlit", "Supabase", "Machine Learning"],
                    "duration": "6 months",
                    "github_link": "https://github.com/johndoe/placement-platform"
                }
            ],
            "internships": [
                {
                    "company": "Google",
                    "role": "Software Engineering Intern",
                    "duration": "3 months",
                    "description": "Worked on Google Search algorithms"
                }
            ],
            "certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "year": "2023"
                }
            ],
            "career_plan": {
                "target_role": "Software Development Engineer",
                "timeline": "1 year"
            },
            "placement_prediction": {
                "probability": "85-95%",
                "calculated_date": "2024-01-25"
            },
            "interview_preparation": {},
            "job_applications": [],
            "placement_status": {}
        }
    
    def load_from_database(self):
        """Load student data from database"""
        try:
            if self.db_manager and hasattr(self.db_manager, 'get_student_profile'):
                # Try to get student profile from database
                profile = self.db_manager.get_student_profile(st.session_state.get('student_email', ''))
                if profile:
                    self.student_data["profile"] = profile
                    
                    # Load other data
                    self.student_data["education"] = self.db_manager.get_student_education(profile.get('id', ''))
                    self.student_data["projects"] = self.db_manager.get_student_projects(profile.get('id', ''))
                    self.student_data["internships"] = self.db_manager.get_student_internships(profile.get('id', ''))
                    self.student_data["certifications"] = self.db_manager.get_student_certifications(profile.get('id', ''))
                    self.student_data["job_applications"] = self.db_manager.get_student_applications(profile.get('id', ''))
        except Exception as e:
            st.error(f"Error loading from database: {e}")
            self.load_demo_data()
    
    def save_profile_to_database(self):
        """Save student profile to database"""
        try:
            if self.demo_mode or not self.db_manager:
                st.warning("⚠️ Running in demo mode - Profile saved locally only")
                return True
        
            # Check if we have required methods
            if not hasattr(self.db_manager, 'save_student_profile'):
                st.error(f"Database manager doesn't support saving student profiles. Available methods: {[m for m in dir(self.db_manager) if not m.startswith('_')]}")
                return False
        
            # Prepare profile data
            profile_data = self.student_data["profile"].copy()
        
            # Debug: Show what we're trying to save
            st.info(f"🔍 Trying to save profile data: {json.dumps(profile_data, indent=2)}")
        
            # Add student ID if available in session state
            student_id = st.session_state.get('student_id')
            if student_id:
                profile_data['id'] = student_id
            
            # Validate data before saving
            if hasattr(self.db_manager, 'validate_student_data'):
                validation = self.db_manager.validate_student_data(profile_data)
                if not validation['valid']:
                    st.error(f"❌ Data validation failed: {', '.join(validation['errors'])}")
                    if validation['warnings']:
                        st.warning(f"⚠️ Warnings: {', '.join(validation['warnings'])}")
                    return False
        
            # Try to save profile
            st.info("💾 Attempting to save to database...")
        
            # Check database connection status
            if not self.db_manager.is_connected:
                st.error("❌ Database is not connected")
                return False
        
            # Save profile
            success = self.db_manager.save_student_profile(profile_data)
        
            if success:
                st.success("✅ Profile saved to database successfully!")
            
                # Save related data
                student_id = profile_data.get('id') or self.get_student_id_from_db()
            
                if student_id:
                    st.info(f"📝 Student ID: {student_id}")
                
                    # Save education
                    if self.student_data["education"]:
                        for edu in self.student_data["education"]:
                            edu['student_id'] = student_id
                            if hasattr(self.db_manager, 'save_student_education'):
                                self.db_manager.save_student_education(edu)
                
                    # Save projects
                    if self.student_data["projects"]:
                        for project in self.student_data["projects"]:
                            project['student_id'] = student_id
                            if hasattr(self.db_manager, 'save_student_project'):
                                self.db_manager.save_student_project(project)
                
                    # Save internships
                    if self.student_data["internships"]:
                        for internship in self.student_data["internships"]:
                            internship['student_id'] = student_id
                            if hasattr(self.db_manager, 'save_student_internship'):
                                self.db_manager.save_student_internship(internship)
                
                    # Save certifications
                    if self.student_data["certifications"]:
                        for cert in self.student_data["certifications"]:
                            cert['student_id'] = student_id
                            if hasattr(self.db_manager, 'save_student_certification'):
                                self.db_manager.save_student_certification(cert)
            
                return True
            else:
                st.error("❌ Failed to save profile to database")
            
                # Try to get more detailed error
                try:
                    # Test if we can insert a simple record
                    test_data = {
                        "full_name": "Test Student",
                        "email": f"test{random.randint(1000, 9999)}@test.com",
                        "roll_number": f"TEST{random.randint(1000, 9999)}"
                    }
                    test_result = self.db_manager.insert('students', test_data)
                    if test_result:
                        st.success("✅ Can insert test data - issue might be with your data")
                        st.info(f"Test insert returned: {test_result}")
                    else:
                        st.error("❌ Cannot insert any data - database issue")
                except Exception as e:
                    st.error(f"❌ Database error: {str(e)}")
            
                return False
                
        except Exception as e:
            st.error(f"❌ Error saving to database: {str(e)}")
            st.code(traceback.format_exc())
            return False
    
    def get_student_id_from_db(self):
        """Get student ID from database based on email"""
        try:
            if self.db_manager and hasattr(self.db_manager, 'get_student_by_email'):
                student = self.db_manager.get_student_by_email(self.student_data["profile"]["email"])
                return student.get('id') if student else None
        except:
            return None
        return None
    
    def display(self):
        """Main display method"""
        st.header("👨‍🎓 Student Placement Journey")
        
        # Display current step
        self.display_progress_bar()
        
        # Display step content
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
        st.info("Create your student profile to get started with placement preparation")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*", 
                                         value=self.student_data["profile"]["full_name"],
                                         placeholder="Enter your full name")
                email = st.text_input("Email*", 
                                     value=self.student_data["profile"]["email"],
                                     placeholder="student@college.edu")
                phone = st.text_input("Phone Number", 
                                     value=self.student_data["profile"]["phone"],
                                     placeholder="+91 9876543210")
                roll_number = st.text_input("Roll Number*", 
                                           value=self.student_data["profile"]["roll_number"],
                                           placeholder="e.g., 20BCS001")
            
            with col2:
                college_id = st.text_input("College ID", 
                                          value=self.student_data["profile"]["college_id"])
                department = st.selectbox("Department*",
                    ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                     "Civil Engineering", "Information Technology", "Electronics", "Others"],
                    index=["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                          "Civil Engineering", "Information Technology", "Electronics", "Others"]
                          .index(self.student_data["profile"]["department"]) 
                          if self.student_data["profile"]["department"] in 
                          ["Computer Science", "Electrical Engineering", "Mechanical Engineering",
                           "Civil Engineering", "Information Technology", "Electronics", "Others"] else 0)
                year = st.selectbox("Year of Study*",
                    ["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"],
                    index=["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"]
                          .index(self.student_data["profile"]["year"]) 
                          if self.student_data["profile"]["year"] in 
                          ["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"] else 3)
                semester = st.number_input("Current Semester*", 1, 10, 
                                          self.student_data["profile"]["semester"])
            
            col3, col4 = st.columns(2)
            with col3:
                cgpa = st.number_input("CGPA*", 0.0, 10.0, 
                                      float(self.student_data["profile"]["cgpa"]), 0.1)
            with col4:
                backlogs = st.number_input("Active Backlogs", 0, 20, 
                                          self.student_data["profile"]["backlogs"])
            
            # Skills assessment - FIXED: Removed "Communication" from technical skills
            st.subheader("Skills Assessment")
            technical_skills_options = ["Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL",
                                       "Machine Learning", "Data Analysis", "AWS", "Docker", "Git",
                                       "Flutter", "Android", "iOS", "PHP", "Angular", "Vue.js", "TypeScript",
                                       "MongoDB", "PostgreSQL", "Redis", "Kubernetes", "Terraform"]
            
            # Filter demo skills to only include valid options
            valid_default_skills = [skill for skill in self.student_data["profile"]["technical_skills"] 
                                  if skill in technical_skills_options]
            
            technical_skills = st.multiselect("Technical Skills*",
                technical_skills_options,
                default=valid_default_skills)
            
            # Career interests
            st.subheader("Career Interests")
            career_interests_options = ["Software Development", "Data Science", "Product Management",
                                       "Research", "Consulting", "Entrepreneurship", "Higher Studies",
                                       "Web Development", "Mobile Development", "DevOps", "Cloud Computing",
                                       "UI/UX Design", "Cybersecurity", "AI/ML Engineering"]
            
            valid_default_interests = [interest for interest in self.student_data["profile"]["career_interests"] 
                                     if interest in career_interests_options]
            
            career_interests = st.multiselect("Areas of Interest*",
                career_interests_options,
                default=valid_default_interests)
            
            # Social Links
            st.subheader("🔗 Social Links")
            linkedin = st.text_input("LinkedIn Profile", 
                                    value=self.student_data["profile"]["linkedin_profile"])
            github = st.text_input("GitHub Profile", 
                                  value=self.student_data["profile"]["github_profile"])
            portfolio = st.text_input("Portfolio Website", 
                                     value=self.student_data["profile"]["portfolio_link"])
            
            # FIXED: Added submit button
            submitted = st.form_submit_button("💾 Save Profile & Continue")
            
            if submitted:
                # Validate required fields
                if not all([full_name, email, roll_number, department, year]):
                    st.error("Please fill in all required fields (*)")
                else:
                    # Update student data
                    self.student_data["profile"].update({
                        "full_name": full_name,
                        "email": email,
                        "phone": phone,
                        "roll_number": roll_number,
                        "college_id": college_id,
                        "department": department,
                        "year": year,
                        "semester": semester,
                        "cgpa": cgpa,
                        "backlogs": backlogs,
                        "technical_skills": technical_skills,
                        "career_interests": career_interests,
                        "skills": technical_skills,  # Keep backward compatibility
                        "linkedin_profile": linkedin,
                        "github_profile": github,
                        "portfolio_link": portfolio,
                        "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                    
                    # Try to save to database
                    save_success = self.save_profile_to_database()
                    
                    if save_success:
                        st.success("✅ Profile saved successfully!")
                        st.balloons()
                    else:
                        st.info("Profile saved locally (demo mode)")
                    
                    # Display profile summary
                    self.display_profile_summary()
    
    def step2_ai_resume_building(self):
        """Step 2: AI Resume Building"""
        st.subheader("📝 AI Resume Building")
        st.info("Build your professional resume with AI assistance")
        
        # Show profile summary if exists
        if self.student_data["profile"]:
            with st.expander("📋 Your Profile Summary", expanded=False):
                profile = self.student_data["profile"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Name:** {profile['full_name']}")
                    st.write(f"**Roll No:** {profile['roll_number']}")
                    st.write(f"**Department:** {profile['department']}")
                with col2:
                    st.write(f"**CGPA:** {profile['cgpa']}")
                    st.write(f"**Skills:** {', '.join(profile['technical_skills'][:3])}")
                    st.write(f"**Interests:** {', '.join(profile['career_interests'])}")
        
        # Resume builder
        st.subheader("Build Your Resume")
        
        with st.form("resume_form"):
            # Education
            st.write("**Education Details**")
            college = st.text_input("College/University", 
                                   self.student_data["resume"].get("education", {}).get("college", "ABC Engineering College"))
            degree = st.text_input("Degree", 
                                  self.student_data["resume"].get("education", {}).get("degree", "Bachelor of Technology"))
            specialization = st.text_input("Specialization", 
                                          self.student_data["resume"].get("education", {}).get("specialization", "Computer Science"))
            graduation_year = st.number_input("Graduation Year", 2020, 2030, 
                                             self.student_data["resume"].get("education", {}).get("graduation_year", 2024))
            
            # Projects
            st.write("**Projects**")
            project1 = st.text_input("Project 1 Title", 
                                    self.student_data["resume"].get("projects", [{}])[0].get("title", "AI Placement Predictor"))
            project1_desc = st.text_area("Project 1 Description", 
                                        self.student_data["resume"].get("projects", [{}])[0].get("description", "Developed an AI model to predict placement probability"))
            
            # Skills
            st.write("**Skills**")
            skills_text = ", ".join(self.student_data["resume"].get("skills", self.student_data["profile"].get("technical_skills", ["Python", "SQL"])))
            skills = st.text_area("Your Skills (comma-separated)", 
                                 skills_text)
            
            # Achievements
            st.write("**Achievements**")
            achievements = st.text_area("Academic/Extracurricular Achievements",
                                      value=self.student_data["resume"].get("achievements", ""),
                                      placeholder="List your achievements, awards, etc.")
            
            # FIXED: Added submit button
            submitted = st.form_submit_button("💾 Generate Resume Preview")
            
            if submitted:
                self.student_data["resume"] = {
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
                    "achievements": achievements
                }
                st.success("Resume details saved!")
        
        # Show resume preview if data exists
        if self.student_data.get("resume"):
            with st.expander("👀 Resume Preview", expanded=True):
                self.preview_resume()
    
    def step3_nep_course_planning(self):
        """Step 3: NEP Course Planning"""
        st.subheader("📚 NEP Course Planning")
        st.info("Plan your courses according to NEP 2020 guidelines")
        
        department = self.student_data["profile"].get("department", "Computer Science")
        
        st.write(f"**Recommended Course Plan for {department}**")
        
        # Course selection based on department
        if "Computer" in department or "IT" in department:
            major_options = ["Data Structures", "Algorithms", "Database Systems", "Computer Networks", 
                           "Operating Systems", "Software Engineering", "AI/ML", "Web Technologies"]
            minor_options = ["Business Management", "Data Science", "Psychology", "Economics", "Entrepreneurship"]
        else:
            major_options = ["Core Engineering Subjects", "Applied Mathematics", "Engineering Design", 
                           "Professional Ethics", "Research Methodology"]
            minor_options = ["Computer Basics", "Data Analytics", "Management", "Communication Skills"]
        
        # Simple course selection
        major_courses = st.multiselect("Major Courses",
            major_options,
            default=self.student_data["courses"].get("major_courses", ["Data Structures", "Algorithms"]))
        
        minor_index = 0
        if self.student_data["courses"].get("minor") in minor_options:
            minor_index = minor_options.index(self.student_data["courses"].get("minor"))
        
        minor_selected = st.selectbox("Minor Specialization", 
                                     minor_options,
                                     index=minor_index)
        
        skill_courses = st.multiselect("Skill Enhancement Courses",
            ["Entrepreneurship", "Communication Skills", "Research Methodology", "Project Management",
             "Professional Ethics", "Leadership", "Team Management", "Critical Thinking"],
            default=self.student_data["courses"].get("skill_courses", ["Entrepreneurship", "Communication Skills"]))
        
        # Credit calculation
        st.subheader("📊 Credit Analysis")
        total_credits = (len(major_courses) * 4) + (2 if minor_selected else 0) + (len(skill_courses) * 2)
        st.metric("Total Credits", total_credits)
        
        if total_credits < 160:
            st.warning("⚠️ You need at least 160 credits for graduation (NEP requirement)")
        else:
            st.success("✅ You have sufficient credits for graduation")
        
        # FIXED: Added proper button (not in form)
        if st.button("💾 Save Course Plan", key="save_course_plan"):
            self.student_data["courses"] = {
                "major_courses": major_courses,
                "minor": minor_selected,
                "skill_courses": skill_courses,
                "total_credits": total_credits
            }
            st.success("Course plan saved!")
    
    def step4_internship_match(self):
        """Step 4: PM Internship Match"""
        st.subheader("💼 PM Internship Match")
        st.info("Find internship opportunities matching your profile")
        
        # Student profile for matching
        profile = self.student_data["profile"]
        
        # Sample internships with matching logic
        internships = [
            {
                "company": "Google", 
                "role": "APM Intern", 
                "location": "Bangalore", 
                "requirements": ["Product Management", "Analytical Skills", "Communication"],
                "match": "85%" if "Product Management" in profile.get("career_interests", []) else "75%"
            },
            {
                "company": "Microsoft", 
                "role": "Software Engineering Intern", 
                "location": "Hyderabad", 
                "requirements": ["Python", "C++", "Data Structures"],
                "match": "92%" if any(skill in profile.get("technical_skills", []) for skill in ["Python", "C++"]) else "78%"
            },
            {
                "company": "Amazon", 
                "role": "Data Science Intern", 
                "location": "Mumbai", 
                "requirements": ["Machine Learning", "Python", "Statistics"],
                "match": "88%" if "Machine Learning" in profile.get("technical_skills", []) else "72%"
            },
            {
                "company": "Adobe", 
                "role": "UX Design Intern", 
                "location": "Noida", 
                "requirements": ["Design Thinking", "Figma", "UI/UX"],
                "match": "65%"
            }
        ]
        
        # Filter by student interests
        user_interests = profile.get("career_interests", [])
        filtered_internships = []
        
        for intern in internships:
            # Simple matching logic
            if any(interest in str(intern.values()) for interest in user_interests):
                filtered_internships.append(intern)
        
        if not filtered_internships:
            filtered_internships = internships[:2]  # Show some anyway
        
        st.write(f"**Found {len(filtered_internships)} internship opportunities**")
        
        for intern in filtered_internships:
            with st.expander(f"{intern['company']} - {intern['role']} (Match: {intern['match']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Location:** {intern['location']}")
                    st.write(f"**Requirements:** {', '.join(intern['requirements'])}")
                with col2:
                    st.metric("Match Score", intern['match'])
                
                if st.button(f"Apply to {intern['company']}", key=f"apply_{intern['company']}"):
                    # Add to applications
                    application = {
                        "company": intern['company'],
                        "role": intern['role'],
                        "applied_date": datetime.now().strftime("%Y-%m-%d"),
                        "status": "Applied"
                    }
                    self.student_data["job_applications"].append(application)
                    st.success(f"Application started for {intern['role']} at {intern['company']}!")
                    st.rerun()
    
    def step5_career_path_planning(self):
        """Step 5: Career Path Planning"""
        st.subheader("🎯 Career Path Planning")
        st.info("Plan your career path based on your profile")
        
        profile = self.student_data.get("profile", {})
        
        st.write("**Recommended Career Paths:**")
        
        # Career recommendations based on interests and skills
        recommendations = []
        
        if "Software Development" in profile.get("career_interests", []):
            recommendations.append({
                "title": "Software Development Engineer",
                "path": "Junior Developer → Senior Developer → Tech Lead → Engineering Manager",
                "skills_needed": ["Programming", "System Design", "Algorithms", "Agile Methodology"],
                "avg_package": "8-15 LPA (Entry) → 30-50+ LPA (Senior)",
                "match": "90%" if any(skill in profile.get("technical_skills", []) for skill in ["Python", "Java", "C++"]) else "70%"
            })
        
        if "Data Science" in profile.get("career_interests", []):
            recommendations.append({
                "title": "Data Scientist",
                "path": "Data Analyst → Junior Data Scientist → Senior Data Scientist → Head of Analytics",
                "skills_needed": ["Statistics", "Machine Learning", "Python/R", "SQL", "Data Visualization"],
                "avg_package": "6-12 LPA (Entry) → 25-40+ LPA (Senior)",
                "match": "85%" if any(skill in profile.get("technical_skills", []) for skill in ["Machine Learning", "Data Analysis", "Python"]) else "65%"
            })
        
        if "Product Management" in profile.get("career_interests", []):
            recommendations.append({
                "title": "Product Manager",
                "path": "Associate PM → Product Manager → Senior PM → Director of Product",
                "skills_needed": ["Communication", "Market Analysis", "Strategy", "User Research"],
                "avg_package": "10-18 LPA (Entry) → 35-60+ LPA (Senior)",
                "match": "80%" if "Communication" in str(profile.get("skills", [])) else "60%"
            })
        
        # Display recommendations
        for rec in recommendations:
            with st.expander(f"{rec['title']} (Match: {rec['match']})"):
                st.write(f"**Career Path:** {rec['path']}")
                st.write(f"**Key Skills Needed:** {', '.join(rec['skills_needed'])}")
                st.write(f"**Average Package:** {rec['avg_package']}")
                
                # Check skill gaps
                student_skills = set(profile.get("technical_skills", []))
                needed_skills = set(rec['skills_needed'])
                missing_skills = needed_skills - student_skills
                
                if missing_skills:
                    st.warning(f"**Skill Gaps:** {', '.join(missing_skills)}")
                else:
                    st.success("✅ You have all the key skills needed!")
        
        # Career goal setting
        st.subheader("Set Your Career Goals")
        col1, col2 = st.columns(2)
        with col1:
            target_role = st.text_input("Target Role", 
                                       self.student_data["career_plan"].get("target_role", "Software Development Engineer"))
            timeline = st.selectbox("Timeline", 
                                   ["6 months", "1 year", "2 years", "3 years", "5 years"],
                                   index=["6 months", "1 year", "2 years", "3 years", "5 years"]
                                          .index(self.student_data["career_plan"].get("timeline", "1 year"))
                                          if self.student_data["career_plan"].get("timeline") in 
                                          ["6 months", "1 year", "2 years", "3 years", "5 years"] else 1)
        with col2:
            target_company = st.text_input("Target Companies (comma-separated)",
                                          value=", ".join(self.student_data["career_plan"].get("target_company", ["Google", "Microsoft", "Amazon"])))
            desired_package = st.number_input("Desired Package (₹ LPA)", 5.0, 50.0, 
                                             float(self.student_data["career_plan"].get("desired_package", 12.0)), 1.0)
        
        # FIXED: Added proper button (not in form)
        if st.button("🎯 Save Career Goals", key="save_career_goals"):
            self.student_data["career_plan"] = {
                "target_role": target_role,
                "timeline": timeline,
                "target_company": [c.strip() for c in target_company.split(",")],
                "desired_package": desired_package,
                "set_date": datetime.now().strftime("%Y-%m-%d")
            }
            st.success("Career goals saved!")
    
    def step6_placement_prediction(self):
        """Step 6: Placement Prediction"""
        st.subheader("📊 Placement Prediction")
        st.info("Predict your placement probability based on your profile")
        
        profile = self.student_data.get("profile", {})
        
        # Input factors for prediction
        col1, col2 = st.columns(2)
        
        with col1:
            cgpa = st.slider("CGPA", 0.0, 10.0, 
                            float(profile.get("cgpa", 7.5)), 
                            step=0.1, key="cgpa_slider")
            projects_count = st.slider("Number of Projects", 0, 10, 
                                      len(self.student_data.get("projects", [])), 
                                      step=1, key="projects_slider")
            internships_count = st.slider("Number of Internships", 0, 5, 
                                         len(self.student_data.get("internships", [])), 
                                         step=1, key="internships_slider")
        
        with col2:
            skills_count = st.slider("Number of Skills", 0, 20, 
                                    len(profile.get("technical_skills", [])), 
                                    step=1, key="skills_slider")
            coding_rating = st.slider("Coding Proficiency (1-10)", 1, 10, 7, step=1, key="coding_slider")
            communication_rating = st.slider("Communication Skills (1-10)", 1, 10, 7, step=1, key="comm_slider")
        
        # Predict button - FIXED: Not in form
        if st.button("🤖 Predict Placement Chances", key="predict_button"):
            # Enhanced prediction algorithm
            base_score = 40
            
            # CGPA contribution (up to 25 points)
            cgpa_score = (cgpa / 10.0) * 25
            
            # Projects contribution (up to 20 points)
            projects_score = min(projects_count * 4, 20)
            
            # Internships contribution (up to 20 points)
            internships_score = min(internships_count * 6, 20)
            
            # Skills contribution (up to 15 points)
            skills_score = min(skills_count * 0.75, 15)
            
            # Soft skills contribution (up to 10 points)
            soft_skills_score = (coding_rating + communication_rating) * 0.5
            
            # Backlog penalty
            backlog_penalty = profile.get("backlogs", 0) * 3
            
            total_score = base_score + cgpa_score + projects_score + internships_score + skills_score + soft_skills_score - backlog_penalty
            
            # Normalize to 0-100
            placement_probability = min(max(total_score, 0), 100)
            
            # Display result
            st.subheader("📈 Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Placement Probability", f"{placement_probability:.1f}%")
            with col2:
                if placement_probability >= 85:
                    expected_package = "₹12-18 LPA"
                    company_tier = "Tier 1 (FAANG)"
                elif placement_probability >= 70:
                    expected_package = "₹8-12 LPA"
                    company_tier = "Tier 2"
                elif placement_probability >= 50:
                    expected_package = "₹5-8 LPA"
                    company_tier = "Tier 3"
                else:
                    expected_package = "₹3-5 LPA"
                    company_tier = "Startups/SMEs"
                    
                st.metric("Expected Package", expected_package)
            with col3:
                st.metric("Company Tier", company_tier)
            
            # Progress bar
            st.progress(placement_probability / 100)
            
            # Save prediction
            self.student_data["placement_prediction"] = {
                "probability": f"{placement_probability:.1f}%",
                "expected_package": expected_package,
                "company_tier": company_tier,
                "factors": {
                    "cgpa": cgpa,
                    "projects_count": projects_count,
                    "internships_count": internships_count,
                    "skills_count": skills_count,
                    "coding_rating": coding_rating,
                    "communication_rating": communication_rating
                },
                "calculated_date": datetime.now().strftime("%Y-%m-%d")
            }
            
            # Recommendations
            st.divider()
            st.write("### 📝 Recommendations to Improve")
            
            recommendations = []
            if cgpa < 8.0:
                recommendations.append("📚 Improve your CGPA (target: 8.0+)")
            if projects_count < 2:
                recommendations.append("💻 Complete at least 2 major projects")
            if internships_count < 1:
                recommendations.append("🏢 Secure at least 1 internship")
            if skills_count < 8:
                recommendations.append("🛠️ Learn more technical skills")
            if coding_rating < 7:
                recommendations.append("💡 Practice coding on platforms like LeetCode, HackerRank")
            if communication_rating < 7:
                recommendations.append("🗣️ Improve communication skills through practice sessions")
            if profile.get("backlogs", 0) > 0:
                recommendations.append("📖 Clear your backlogs as soon as possible")
            
            if recommendations:
                st.warning("**Areas for improvement:**")
                for rec in recommendations:
                    st.write(f"• {rec}")
            else:
                st.success("✅ You're on track for excellent placement!")
    
    def step7_interview_preparation(self):
        """Step 7: Interview Preparation"""
        st.subheader("🤝 Interview Preparation")
        st.info("Prepare for technical and HR interviews")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💻 Technical", "🗣️ HR", "📝 Mock Tests", "📚 Resources"])
        
        with tab1:
            st.write("### Technical Interview Preparation")
            
            role = st.selectbox("Select target role:", 
                               ["Software Developer", "Data Scientist", "Web Developer", 
                                "Mobile Developer", "DevOps Engineer", "Full Stack Developer",
                                "Product Manager", "UI/UX Designer"])
            
            if role:
                technical_topics = {
                    "Software Developer": ["Data Structures", "Algorithms", "OOP Concepts", "System Design", "DBMS", "OS Concepts"],
                    "Data Scientist": ["Statistics", "Machine Learning", "Python/R", "SQL", "Data Analysis", "Probability"],
                    "Web Developer": ["HTML/CSS", "JavaScript", "React/Angular/Vue", "REST APIs", "Web Security", "Browser APIs"],
                    "Mobile Developer": ["Android/iOS", "React Native/Flutter", "Mobile UI/UX", "API Integration", "Performance"],
                    "DevOps Engineer": ["Linux", "Docker", "Kubernetes", "AWS/GCP/Azure", "CI/CD", "Networking"],
                    "Full Stack Developer": ["Frontend Technologies", "Backend Development", "Database", "Deployment", "Security", "APIs"],
                    "Product Manager": ["Product Strategy", "User Research", "Metrics", "Prioritization", "Stakeholder Management"],
                    "UI/UX Designer": ["Design Principles", "Figma/Sketch", "User Research", "Wireframing", "Prototyping"]
                }
                
                topics = technical_topics.get(role, ["General Computer Science"])
                st.write(f"**Key topics for {role}:**")
                
                selected_topic = st.selectbox("Select topic to practice:", topics, key="tech_topic_select")
                
                if selected_topic:
                    st.write(f"**Sample Questions for {selected_topic}:**")
                    
                    # Sample questions based on topic
                    sample_questions = {
                        "Data Structures": [
                            "Explain time complexity of common algorithms",
                            "Difference between array and linked list",
                            "When to use hashmap vs array"
                        ],
                        "Machine Learning": [
                            "Explain bias-variance tradeoff",
                            "Difference between supervised and unsupervised learning",
                            "What is overfitting and how to prevent it?"
                        ],
                        "System Design": [
                            "Design a URL shortening service",
                            "How would you design Twitter?",
                            "Explain load balancing strategies"
                        ]
                    }
                    
                    questions = sample_questions.get(selected_topic, [
                        f"Explain key concepts in {selected_topic}",
                        f"Practical applications of {selected_topic}",
                        f"Common challenges in {selected_topic}"
                    ])
                    
                    for i, q in enumerate(questions):
                        with st.expander(f"Q{i+1}: {q}"):
                            answer = st.text_area("Your answer:", key=f"tech_{selected_topic}_{i}", height=100)
                            if st.button("Evaluate", key=f"eval_{selected_topic}_{i}"):
                                if len(answer) > 30:
                                    st.success("Good answer! Consider adding examples.")
                                else:
                                    st.warning("Try to elaborate more with specific examples.")
        
        with tab2:
            st.write("### HR Interview Preparation")
            
            common_questions = [
                "Tell me about yourself",
                "Why do you want to work for our company?",
                "What are your strengths and weaknesses?",
                "Where do you see yourself in 5 years?",
                "Why should we hire you?",
                "Describe a challenging situation and how you handled it",
                "What are your salary expectations?",
                "Do you have any questions for us?"
            ]
            
            for question in common_questions:
                with st.expander(f"❓ {question}"):
                    answer = st.text_area("Your answer:", key=f"hr_{question}", height=120)
                    tips = st.text_area("AI Tips (edit as needed):", 
                                       value="• Structure your answer: Situation-Action-Result\n• Be specific with examples\n• Connect to company values\n• Show enthusiasm for the role",
                                       height=100, key=f"tips_{question}")
                    
                    if st.button("Get AI Feedback", key=f"feedback_{question}"):
                        if len(answer) > 50:
                            st.success("✅ Good length! Make sure to:")
                            st.write("1. Include specific examples")
                            st.write("2. Show results/impact")
                            st.write("3. Be concise and clear")
                        else:
                            st.warning("⚠️ Try to elaborate more. Aim for 100-150 words.")
        
        with tab3:
            st.write("### Mock Tests")
            
            test_types = [
                {"name": "Aptitude Test", "duration": "30 mins", "questions": 20, "type": "Quant, Verbal, Logical"},
                {"name": "Technical Test", "duration": "60 mins", "questions": 15, "type": "Coding, MCQs"},
                {"name": "Coding Test", "duration": "90 mins", "questions": 3, "type": "Algorithms, Data Structures"},
                {"name": "Personality Test", "duration": "20 mins", "questions": 50, "type": "Behavioral"}
            ]
            
            for test in test_types:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{test['name']}**")
                    st.write(f"Duration: {test['duration']} | Questions: {test['questions']}")
                    st.caption(f"Type: {test['type']}")
                with col2:
                    score = st.select_slider(f"Score", 
                                            options=["0-20%", "21-40%", "41-60%", "61-80%", "81-100%"],
                                            key=f"score_{test['name']}")
                with col3:
                    if st.button("Start", key=f"start_{test['name']}"):
                        st.info(f"Starting {test['name']}...")
        
        with tab4:
            st.write("### Learning Resources")
            
            resources = {
                "LeetCode": "https://leetcode.com - Practice coding problems",
                "HackerRank": "https://hackerrank.com - Coding challenges and contests",
                "GeeksforGeeks": "https://geeksforgeeks.org - Technical articles and tutorials",
                "InterviewBit": "https://interviewbit.com - Company-specific questions",
                "Glassdoor": "https://glassdoor.com - Company reviews and interview experiences",
                "YouTube": "https://youtube.com - Free interview preparation videos",
                "Coursera": "https://coursera.org - Online courses for skill development",
                "Udemy": "https://udemy.com - Affordable courses on various topics"
            }
            
            for platform, description in resources.items():
                url = description.split(" - ")[0]
                desc = description.split(" - ")[1]
                st.write(f"🔗 **[{platform}]({url})**: {desc}")
    
    def step8_placement_tracking(self):
        """Step 8: Placement Tracking"""
        st.subheader("✅ Placement Tracking")
        st.success("🎉 Track your placement journey and applications")
        
        # Application tracker
        st.write("### 📋 Application Tracker")
        
        # Add new application - FIXED: Added form with submit button
        with st.expander("➕ Add New Application", expanded=True):
            with st.form("add_application_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_company = st.text_input("Company Name", key="new_company")
                    new_position = st.text_input("Position", key="new_position")
                with col2:
                    new_status = st.selectbox("Status", 
                                             ["Applied", "Under Review", "Online Test", 
                                              "Technical Round", "HR Round", "Offer Received", "Rejected"],
                                             key="new_status")
                    new_date = st.date_input("Application Date", key="new_date")
                
                # FIXED: Added submit button
                submitted = st.form_submit_button("Add Application")
                
                if submitted:
                    if new_company and new_position:
                        application = {
                            "company": new_company,
                            "position": new_position,
                            "status": new_status,
                            "date": str(new_date),
                            "added_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        self.student_data["job_applications"].append(application)
                        st.success(f"Added application to {new_company}")
                        st.rerun()
                    else:
                        st.error("Please fill in Company Name and Position")
        
        # Display applications
        if self.student_data["job_applications"]:
            st.write("#### Your Applications")
            
            # Add color coding for status
            def status_color(status):
                colors = {
                    "Applied": "#3498db",
                    "Under Review": "#f39c12",
                    "Online Test": "#9b59b6",
                    "Technical Round": "#2ecc71",
                    "HR Round": "#1abc9c",
                    "Offer Received": "#27ae60",
                    "Rejected": "#e74c3c"
                }
                return colors.get(status, "#95a5a6")
            
            # Display each application
            for i, app in enumerate(self.student_data["job_applications"]):
                color = status_color(app["status"])
                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 10px; margin: 5px 0; background-color: #f9f9f9;">
                    <b>{app['company']}</b> - {app['position']}<br>
                    📅 {app['date']} | 📊 Status: <b style="color: {color};">{app['status']}</b>
                </div>
                """, unsafe_allow_html=True)
            
            # Statistics
            st.divider()
            st.write("### 📊 Application Statistics")
            
            total_apps = len(self.student_data["job_applications"])
            interviews = len([a for a in self.student_data["job_applications"] if "Round" in a["status"]])
            offers = len([a for a in self.student_data["job_applications"] if a["status"] == "Offer Received"])
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Applications", total_apps)
            with col2:
                st.metric("Interviews", interviews)
            with col3:
                st.metric("Offers", offers)
            with col4:
                success_rate = (offers / total_apps * 100) if total_apps > 0 else 0
                st.metric("Success Rate", f"{success_rate:.1f}%")
            
            # Offer details
            if offers > 0:
                st.divider()
                st.write("### 🎉 Congratulations! Offer Details")
                
                offers_received = [a for a in self.student_data["job_applications"] if a["status"] == "Offer Received"]
                for i, offer in enumerate(offers_received):
                    with st.expander(f"Offer from {offer['company']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            package = st.number_input("Package (₹ LPA)", min_value=3.0, max_value=50.0, 
                                                     value=12.0, step=0.5, key=f"package_{i}")
                            location = st.text_input("Location", value="Bangalore", key=f"loc_{i}")
                        with col2:
                            joining_date = st.date_input("Joining Date", key=f"join_{i}")
                            st.write(f"**Position:** {offer['position']}")
                        
                        if st.button("Accept Offer", key=f"accept_{i}"):
                            self.student_data["placement_status"] = {
                                "company": offer['company'],
                                "position": offer['position'],
                                "package": package,
                                "location": location,
                                "joining_date": str(joining_date),
                                "acceptance_date": datetime.now().strftime("%Y-%m-%d")
                            }
                            st.success(f"🎉 Congratulations! You've accepted the offer from {offer['company']}!")
                            st.balloons()
        else:
            st.info("No applications added yet. Start by adding your first application!")
        
        # Export data
        st.divider()
        if st.button("📥 Export Placement Data", key="export_data"):
            if self.student_data["job_applications"]:
                # Create DataFrame
                df = pd.DataFrame(self.student_data["job_applications"])
                csv = df.to_csv(index=False)
                
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="placement_applications.csv",
                    mime="text/csv",
                    key="download_csv"
                )
            else:
                st.warning("No data to export")
        
        # Restart option
        st.divider()
        if st.button("🔄 Start New Journey", key="restart_journey"):
            # Reset student data
            self.student_data = {
                "profile": self.student_data["profile"],  # Keep profile
                "education": [],
                "resume": {},
                "courses": {},
                "projects": [],
                "internships": [],
                "certifications": [],
                "career_plan": {},
                "placement_prediction": {},
                "interview_preparation": {},
                "job_applications": [],
                "placement_status": {}
            }
            st.success("Journey reset! You can start again.")
            st.rerun()
    
    def preview_resume(self):
        """Preview the resume"""
        profile = self.student_data.get("profile", {})
        resume = self.student_data.get("resume", {})
        education = self.student_data.get("education", [{}])[0] if self.student_data.get("education") else {}
        
        html = f"""
        <div style="font-family: Arial, sans-serif; padding: 25px; border: 2px solid #3498db; border-radius: 15px; background: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <div style="text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 20px;">
                <h1 style="color: #2c3e50; margin-bottom: 5px;">{profile.get('full_name', 'Your Name')}</h1>
                <p style="color: #7f8c8d; margin: 5px 0;">
                    📧 {profile.get('email', 'email@example.com')} | 📱 {profile.get('phone', 'Phone')} |
                    🔗 {profile.get('linkedin_profile', 'LinkedIn')} | 🐙 {profile.get('github_profile', 'GitHub')}
                </p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">🎓 Education</h2>
                <p style="margin: 5px 0;"><strong>{resume.get('education', {{}}).get('degree', education.get('degree', 'Degree'))}</strong></p>
                <p style="margin: 5px 0; color: #555;">
                    {resume.get('education', {{}}).get('college', education.get('institution', 'College'))} | 
                    CGPA: {profile.get('cgpa', 'N/A')} | 
                    Graduation: {resume.get('education', {{}}).get('graduation_year', education.get('year', 'Year'))}
                </p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">🛠️ Skills</h2>
                <p style="margin: 5px 0;">{', '.join(resume.get('skills', profile.get('technical_skills', ['Skills'])))}</p>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">💼 Projects</h2>
                <p style="margin: 5px 0;"><strong>{resume.get('projects', [{{}}])[0].get('title', 'Project Title')}</strong></p>
                <p style="margin: 5px 0; color: #555;">{resume.get('projects', [{{}}])[0].get('description', 'Project description')}</p>
            </div>
        </div>
        """
        
        st.markdown(html, unsafe_allow_html=True)
        
        # Download button
        if st.button("📄 Download Resume (Text)", key="download_resume"):
            resume_text = f"""
            RESUME
            ======
            
            {profile.get('full_name', 'Your Name')}
            Email: {profile.get('email', '')}
            Phone: {profile.get('phone', '')}
            LinkedIn: {profile.get('linkedin_profile', '')}
            GitHub: {profile.get('github_profile', '')}
            
            EDUCATION
            ---------
            {resume.get('education', {{}}).get('degree', '')}
            {resume.get('education', {{}}).get('college', '')}
            CGPA: {profile.get('cgpa', '')}
            Graduation: {resume.get('education', {{}}).get('graduation_year', '')}
            
            SKILLS
            ------
            {', '.join(resume.get('skills', []))}
            
            PROJECTS
            --------
            {resume.get('projects', [{{}}])[0].get('title', '')}
            {resume.get('projects', [{{}}])[0].get('description', '')}
            """
            
            st.download_button(
                label="📥 Download Resume",
                data=resume_text,
                file_name=f"resume_{profile.get('full_name', 'student')}.txt",
                mime="text/plain",
                key="download_resume_file"
            )
    
    def display_progress_bar(self):
        """Display progress bar for current step"""
        progress = self.current_step / self.total_steps
        st.progress(progress)
        
        # Step names for display
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
        
        st.caption(f"Step {self.current_step} of {self.total_steps}: {step_names.get(self.current_step, '')}")
    
    def display_profile_summary(self):
        """Display profile summary"""
        with st.expander("👤 Profile Summary", expanded=False):
            profile = self.student_data["profile"]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {profile['full_name']}")
                st.write(f"**Email:** {profile['email']}")
                st.write(f"**College ID:** {profile['college_id']}")
                st.write(f"**Roll No:** {profile['roll_number']}")
                st.write(f"**Department:** {profile['department']}")
            
            with col2:
                st.write(f"**Year:** {profile['year']}")
                st.write(f"**Semester:** {profile['semester']}")
                st.write(f"**CGPA:** {profile['cgpa']}")
                st.write(f"**Backlogs:** {profile['backlogs']}")
                st.write(f"**Career Interests:** {', '.join(profile['career_interests'])}")
            
            if profile['technical_skills']:
                st.write(f"**Technical Skills:** {', '.join(profile['technical_skills'])}")
