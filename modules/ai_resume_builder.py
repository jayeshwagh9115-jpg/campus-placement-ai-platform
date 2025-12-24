import streamlit as st
import pandas as pd
import json
import base64
from datetime import datetime

class AIResumeBuilder:
    def __init__(self):
        self.template_options = {
            "Professional": "Clean and formal design suitable for corporate jobs",
            "Creative": "Modern design with color accents for creative roles",
            "Academic": "Traditional format suitable for research and academic positions",
            "Minimalist": "Simple and elegant design focusing on content"
        }
    
    def display(self):
        """Display AI Resume Builder interface"""
        st.header("🤖 AI-Powered Resume Builder")
        
        # Check if user is in demo mode
        if 'demo_mode' in st.session_state and st.session_state.demo_mode:
            st.info("🎮 Demo Mode Active - Using sample student data")
            self.demo_mode()
            return
        
        # Main interface
        tab1, tab2, tab3 = st.tabs(["📝 Build Resume", "🔄 Optimize Resume", "📊 ATS Checker"])
        
        with tab1:
            self.build_resume()
        
        with tab2:
            self.optimize_resume()
        
        with tab3:
            self.ats_checker()
    
    def build_resume(self):
        """Build resume from scratch"""
        st.subheader("Create Your Resume")
        
        with st.form("resume_builder_form"):
            # Personal Information
            st.markdown("### Personal Information")
            col1, col2 = st.columns(2)
            
            with col1:
                full_name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone Number")
            
            with col2:
                linkedin = st.text_input("LinkedIn Profile URL")
                github = st.text_input("GitHub Profile URL")
                portfolio = st.text_input("Portfolio Website")
            
            # Education
            st.markdown("### Education")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                degree = st.text_input("Degree*", "Bachelor of Technology")
                university = st.text_input("University*", "ABC University")
            
            with col2:
                major = st.text_input("Major*", "Computer Science")
                cgpa = st.number_input("CGPA/Percentage*", 0.0, 10.0, 8.5, 0.1)
            
            with col3:
                grad_year = st.number_input("Graduation Year*", 2000, 2030, 2024)
                location = st.text_input("Location", "City, Country")
            
            # Work Experience
            st.markdown("### Work Experience")
            experience_count = st.number_input("Number of Experiences", 0, 5, 1)
            
            experiences = []
            for i in range(experience_count):
                st.markdown(f"**Experience {i+1}**")
                exp_col1, exp_col2 = st.columns(2)
                
                with exp_col1:
                    company = st.text_input(f"Company {i+1}", key=f"company_{i}")
                    position = st.text_input(f"Position {i+1}", key=f"position_{i}")
                
                with exp_col2:
                    duration = st.text_input(f"Duration {i+1} (e.g., Jan 2023 - Present)", key=f"duration_{i}")
                    location_exp = st.text_input(f"Location {i+1}", key=f"location_exp_{i}")
                
                description = st.text_area(f"Description {i+1}", 
                    key=f"desc_{i}", 
                    height=100,
                    value="• Developed and maintained web applications\n• Collaborated with cross-functional teams\n• Implemented new features and fixed bugs")
                
                experiences.append({
                    'company': company,
                    'position': position,
                    'duration': duration,
                    'location': location_exp,
                    'description': description
                })
            
            # Skills
            st.markdown("### Skills")
            skill_categories = {
                "Technical Skills": ["Python", "Java", "JavaScript", "React", "Node.js", 
                                   "SQL", "AWS", "Docker", "Git", "Machine Learning"],
                "Soft Skills": ["Communication", "Leadership", "Teamwork", "Problem Solving", 
                              "Time Management", "Adaptability"],
                "Tools": ["VS Code", "JIRA", "Figma", "Postman", "Tableau", "Power BI"]
            }
            
            selected_skills = {}
            for category, skills in skill_categories.items():
                selected_skills[category] = st.multiselect(
                    category,
                    skills,
                    default=skills[:2] if category == "Technical Skills" else []
                )
            
            # Projects
            st.markdown("### Projects")
            project_count = st.number_input("Number of Projects", 0, 5, 1)
            
            projects = []
            for i in range(project_count):
                st.markdown(f"**Project {i+1}**")
                proj_col1, proj_col2 = st.columns(2)
                
                with proj_col1:
                    proj_title = st.text_input(f"Project Title {i+1}", key=f"proj_title_{i}")
                    proj_tech = st.text_input(f"Technologies Used {i+1}", key=f"proj_tech_{i}")
                
                with proj_col2:
                    proj_duration = st.text_input(f"Duration {i+1}", key=f"proj_duration_{i}")
                    proj_link = st.text_input(f"Project Link {i+1}", key=f"proj_link_{i}")
                
                proj_desc = st.text_area(f"Description {i+1}", 
                    key=f"proj_desc_{i}", 
                    height=80,
                    value="• Developed a web application for [purpose]\n• Implemented [key features]\n• Achieved [results/impact]")
                
                projects.append({
                    'title': proj_title,
                    'technologies': proj_tech,
                    'duration': proj_duration,
                    'link': proj_link,
                    'description': proj_desc
                })
            
            # Template Selection
            st.markdown("### Resume Template")
            template = st.selectbox("Choose a Template", list(self.template_options.keys()),
                                  format_func=lambda x: f"{x} - {self.template_options[x]}")
            
            # AI Enhancement Options
            st.markdown("### AI Enhancement")
            ai_options = st.multiselect(
                "Select AI enhancements for your resume:",
                ["Optimize Keywords for ATS", "Improve Action Verbs", 
                 "Add Metrics and Quantifiable Results", "Suggest Missing Sections",
                 "Check Grammar and Style"]
            )
            
            # Submit button
            if st.form_submit_button("🚀 Generate AI-Optimized Resume"):
                # Collect all data
                resume_data = {
                    'personal_info': {
                        'name': full_name,
                        'email': email,
                        'phone': phone,
                        'linkedin': linkedin,
                        'github': github,
                        'portfolio': portfolio
                    },
                    'education': {
                        'degree': degree,
                        'university': university,
                        'major': major,
                        'cgpa': cgpa,
                        'year': grad_year,
                        'location': location
                    },
                    'experience': experiences,
                    'skills': selected_skills,
                    'projects': projects,
                    'template': template,
                    'ai_enhancements': ai_options,
                    'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Generate resume
                self.generate_resume(resume_data)
    
    def generate_resume(self, resume_data):
        """Generate and display resume"""
        st.success("✅ Resume generated successfully!")
        
        # Display resume preview
        st.subheader("📄 Resume Preview")
        
        # Create resume HTML preview
        html_resume = self.create_html_resume(resume_data)
        
        # Display in expandable preview
        with st.expander("Preview Resume", expanded=True):
            st.markdown(html_resume, unsafe_allow_html=True)
        
        # AI Suggestions
        if resume_data.get('ai_enhancements'):
            st.subheader("🤖 AI Suggestions")
            
            suggestions = []
            if "Optimize Keywords for ATS" in resume_data['ai_enhancements']:
                suggestions.append("**ATS Optimization:** Add keywords like 'agile methodology', 'cross-functional collaboration', 'SDLC'")
            if "Improve Action Verbs" in resume_data['ai_enhancements']:
                suggestions.append("**Action Verbs:** Replace 'did' with stronger verbs like '
