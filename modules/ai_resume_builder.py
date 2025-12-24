import streamlit as st
import pandas as pd
from openai import OpenAI
import PyPDF2
import docx
import json

class AIResumeBuilder:
    def __init__(self):
        self.client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        self.sample_resumes = self.load_sample_resumes()
    
    def display(self):
        st.header("🤖 AI-Powered Resume Builder")
        
        # Resume input options
        input_method = st.radio(
            "Choose input method:",
            ["📝 Manual Entry", "📁 Upload Resume", "🔗 Import from LinkedIn", "🎮 Demo Mode"]
        )
        
        if input_method == "🎮 Demo Mode":
            self.demo_mode()
        elif input_method == "📁 Upload Resume":
            self.upload_resume()
        elif input_method == "🔗 Import from LinkedIn":
            self.linkedin_import()
        else:
            self.manual_entry()
    
    def manual_entry(self):
        """Manual resume entry form"""
        with st.form("resume_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name*")
                email = st.text_input("Email*")
                phone = st.text_input("Phone")
                linkedin = st.text_input("LinkedIn Profile")
            with col2:
                target_role = st.text_input("Target Role*")
                experience = st.number_input("Years of Experience", min_value=0, max_value=50)
                education = st.selectbox("Highest Education", 
                    ["High School", "Bachelor's", "Master's", "PhD"])
            
            # Skills input with autocomplete suggestions [citation:4]
            skills = st.multiselect(
                "Skills*",
                options=["Python", "Java", "JavaScript", "React", "Node.js", 
                        "AWS", "Docker", "Kubernetes", "SQL", "Machine Learning",
                        "Data Analysis", "Project Management", "Agile", "Communication"],
                default=["Python", "SQL"]
            )
            
            # Experience details
            st.subheader("Work Experience")
            exp_company = st.text_input("Company Name")
            exp_role = st.text_input("Job Title")
            exp_duration = st.text_input("Duration (e.g., 2020-2023)")
            exp_description = st.text_area("Responsibilities and Achievements")
            
            # Projects
            st.subheader("Projects")
            project_title = st.text_input("Project Title")
            project_desc = st.text_area("Project Description")
            
            if st.form_submit_button("🚀 Generate AI-Optimized Resume"):
                self.generate_resume({
                    "name": name,
                    "contact": {"email": email, "phone": phone, "linkedin": linkedin},
                    "target_role": target_role,
                    "skills": skills,
                    "experience": [{
                        "company": exp_company,
                        "role": exp_role,
                        "duration": exp_duration,
                        "description": exp_description
                    }],
                    "projects": [{
                        "title": project_title,
                        "description": project_desc
                    }],
                    "education": education
                })
    
    def generate_resume(self, resume_data):
        """Generate AI-optimized resume"""
        with st.spinner("AI is optimizing your resume..."):
            # Create prompt for AI optimization
            prompt = f"""
            Optimize this resume for a {resume_data['target_role']} position:
            
            Name: {resume_data['name']}
            Skills: {', '.join(resume_data['skills'])}
            Experience: {resume_data['experience'][0]['description'] if resume_data['experience'] else 'None'}
            Education: {resume_data['education']}
            
            Provide:
            1. Professional summary
            2. Skills categorized by relevance
            3. Experience rewritten with action verbs and metrics
            4. ATS optimization tips
            5. Keywords to include
            """
            
            try:
                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional resume writer and ATS optimization expert."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                ai_suggestions = response.choices[0].message.content
                
                # Display results
                st.success("✅ Resume optimized successfully!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📄 Original Information")
                    st.json(resume_data, expanded=False)
                
                with col2:
                    st.subheader("🤖 AI Suggestions")
                    st.markdown(ai_suggestions)
                
                # Download options
                st.subheader("📥 Download Options")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📝 Download as PDF"):
                        st.info("PDF generation would be implemented with ReportLab or similar")
                with col2:
                    if st.button("📄 Download as DOCX"):
                        st.info("DOCX generation would be implemented with python-docx")
                with col3:
                    if st.button("📋 Copy to Clipboard"):
                        st.info("Would copy formatted resume to clipboard")
            
            except Exception as e:
                st.error(f"Error generating resume: {str(e)}")
    
    def demo_mode(self):
        """Demo mode with sample data [citation:3]"""
        st.info("Demo Mode: Using sample student data")
        
        sample_data = {
            "name": "Rahul Sharma",
            "contact": {"email": "rahul.sharma@example.com", "phone": "+91 9876543210"},
            "target_role": "Software Development Engineer",
            "skills": ["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"],
            "experience": [{
                "company": "Tech Innovations Pvt Ltd",
                "role": "Software Developer Intern",
                "duration": "June 2023 - Present",
                "description": "Developed and maintained web applications using React and Node.js"
            }],
            "education": "Bachelor's in Computer Science"
        }
        
        # Display sample data and generate
        st.json(sample_data, expanded=False)
        
        if st.button("🚀 Generate Sample Resume"):
            self.generate_resume(sample_data)
