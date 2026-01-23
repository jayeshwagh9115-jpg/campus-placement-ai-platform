import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random
import json

class StudentFlow:
    def __init__(self):
        self.current_step = 1
        self.total_steps = 5
        self.db_manager = None  # Initialize as None
        self.demo_mode = True  # Default to demo mode
        
        # Initialize student data structure
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
                "resume_url": "",
                "profile_picture_url": "",
                "portfolio_link": "",
                "linkedin_profile": "",
                "github_profile": ""
            },
            "education": [],
            "projects": [],
            "internships": [],
            "certifications": [],
            "job_applications": []
        }
        
        # Load demo data if no db connection
        if self.db_manager is None:
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
                "cgpa": 8.5,
                "backlogs": 0,
                "skills": ["Python", "Java", "SQL", "React", "Machine Learning"],
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
            "job_applications": []
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
            validation = self.db_manager.validate_student_data(profile_data)
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
        st.header("👨‍🎓 Student Dashboard")
        
        # Display current step
        self.display_progress_bar()
        
        # Display step content
        if self.current_step == 1:
            self.step1_profile_setup()
        elif self.current_step == 2:
            self.step2_education_details()
        elif self.current_step == 3:
            self.step3_skills_projects()
        elif self.current_step == 4:
            self.step4_job_search()
        elif self.current_step == 5:
            self.step5_applications_tracking()
    
    def step1_profile_setup(self):
        """Step 1: Profile Setup"""
        st.subheader("📝 Profile Setup")
        
        with st.form("student_profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*", 
                                         value=self.student_data["profile"]["full_name"])
                email = st.text_input("Email*", 
                                     value=self.student_data["profile"]["email"])
                phone = st.text_input("Phone Number*", 
                                     value=self.student_data["profile"]["phone"])
                roll_number = st.text_input("Roll Number*", 
                                           value=self.student_data["profile"]["roll_number"])
            
            with col2:
                college_id = st.text_input("College ID", 
                                          value=self.student_data["profile"]["college_id"])
                department = st.selectbox("Department",
                    ["Computer Science", "Electronics", "Mechanical", "Civil", 
                     "Electrical", "Chemical", "Biotechnology", "Others"],
                    index=["Computer Science", "Electronics", "Mechanical", "Civil", 
                          "Electrical", "Chemical", "Biotechnology", "Others"]
                          .index(self.student_data["profile"]["department"]) 
                          if self.student_data["profile"]["department"] in 
                          ["Computer Science", "Electronics", "Mechanical", "Civil", 
                           "Electrical", "Chemical", "Biotechnology", "Others"] else 0)
                year = st.selectbox("Year of Study",
                    ["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"],
                    index=["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"]
                          .index(self.student_data["profile"]["year"]) 
                          if self.student_data["profile"]["year"] in 
                          ["First Year", "Second Year", "Third Year", "Final Year", "Post Graduate"] else 3)
            
            col3, col4 = st.columns(2)
            with col3:
                cgpa = st.number_input("CGPA*", 0.0, 10.0, 
                                      float(self.student_data["profile"]["cgpa"]), 0.1)
            with col4:
                backlogs = st.number_input("Active Backlogs", 0, 20, 
                                          self.student_data["profile"]["backlogs"])
            
            # Social Links
            st.subheader("🔗 Social Links")
            linkedin = st.text_input("LinkedIn Profile", 
                                    value=self.student_data["profile"]["linkedin_profile"])
            github = st.text_input("GitHub Profile", 
                                  value=self.student_data["profile"]["github_profile"])
            portfolio = st.text_input("Portfolio Website", 
                                     value=self.student_data["profile"]["portfolio_link"])
            
            if st.form_submit_button("💾 Save Profile"):
                # Validate required fields
                if not all([full_name, email, phone, roll_number]):
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
                        "cgpa": cgpa,
                        "backlogs": backlogs,
                        "linkedin_profile": linkedin,
                        "github_profile": github,
                        "portfolio_link": portfolio
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
    
    def step2_education_details(self):
        """Step 2: Education Details"""
        st.subheader("🎓 Education Details")
        
        # Add education form
        with st.form("education_form"):
            st.write("Add Educational Qualification")
            
            col1, col2 = st.columns(2)
            with col1:
                degree = st.text_input("Degree/Certification*", 
                                      placeholder="e.g., B.Tech Computer Science")
                institution = st.text_input("Institution*", 
                                          placeholder="e.g., IIT Bombay")
            with col2:
                year = st.text_input("Year of Completion*", 
                                    placeholder="e.g., 2023")
                percentage = st.number_input("Percentage/CGPA", 0.0, 100.0, 0.0, 0.1)
            
            description = st.text_area("Description", 
                                      placeholder="Brief description of your studies...")
            
            if st.form_submit_button("➕ Add Education"):
                if not all([degree, institution, year]):
                    st.error("Please fill in all required fields (*)")
                else:
                    self.student_data["education"].append({
                        "degree": degree,
                        "institution": institution,
                        "year": year,
                        "percentage": percentage,
                        "description": description
                    })
                    
                    # Save to database if available
                    if not self.demo_mode and self.db_manager:
                        try:
                            student_id = self.get_student_id_from_db()
                            if student_id:
                                edu_data = {
                                    "student_id": student_id,
                                    "degree": degree,
                                    "institution": institution,
                                    "year": year,
                                    "percentage": percentage,
                                    "description": description
                                }
                                if hasattr(self.db_manager, 'save_student_education'):
                                    self.db_manager.save_student_education(edu_data)
                        except Exception as e:
                            st.warning(f"Could not save to database: {e}")
                    
                    st.success("✅ Education added successfully!")
                    st.rerun()
        
        # Display education history
        if self.student_data["education"]:
            st.subheader("📚 Education History")
            
            for i, edu in enumerate(self.student_data["education"]):
                with st.expander(f"{edu['degree']} - {edu['institution']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Year:** {edu['year']}")
                        st.write(f"**Institution:** {edu['institution']}")
                    with col2:
                        st.write(f"**Score:** {edu['percentage']}%")
                    
                    if edu['description']:
                        st.write(f"**Description:** {edu['description']}")
                    
                    # Delete button
                    if st.button(f"Delete", key=f"delete_edu_{i}"):
                        self.student_data["education"].pop(i)
                        
                        # Delete from database if available
                        if not self.demo_mode and self.db_manager:
                            try:
                                if hasattr(self.db_manager, 'delete_student_education'):
                                    # You would need the education record ID here
                                    pass
                            except:
                                pass
                        
                        st.rerun()
        else:
            st.info("No education details added yet.")
    
    # Continue with other steps (3, 4, 5)...
    # (Your existing code for steps 3, 4, 5 remains the same)
    
    def display_progress_bar(self):
        """Display progress bar for current step"""
        progress = self.current_step / self.total_steps
        st.progress(progress)
        st.caption(f"Step {self.current_step} of {self.total_steps}")
    
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
            
            with col2:
                st.write(f"**Department:** {profile['department']}")
                st.write(f"**Year:** {profile['year']}")
                st.write(f"**CGPA:** {profile['cgpa']}")
                st.write(f"**Backlogs:** {profile['backlogs']}")
            
            if profile['skills']:
                st.write(f"**Skills:** {', '.join(profile['skills'])}")
