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
                suggestions.append("**Action Verbs:** Replace 'did' with stronger verbs like 'developed', 'implemented', 'optimized'")
            if "Add Metrics and Quantifiable Results" in resume_data['ai_enhancements']:
                suggestions.append("**Quantify Results:** Add metrics like 'improved performance by 30%', 'reduced costs by 20%'")
            
            for suggestion in suggestions:
                st.info(suggestion)
        
        # Download options
        st.subheader("📥 Download Options")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📝 Download as PDF"):
                st.info("PDF generation would be implemented with external library")
        with col2:
            if st.button("📄 Download as DOCX"):
                st.info("DOCX generation would be implemented with python-docx")
        with col3:
            if st.button("📋 Copy HTML to Clipboard"):
                st.info("Would copy HTML to clipboard")
    
    def create_html_resume(self, resume_data):
        """Create HTML representation of resume"""
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #2c3e50; margin-bottom: 5px;">{resume_data['personal_info']['name']}</h1>
                <div style="color: #7f8c8d;">
                    {resume_data['personal_info']['email']} | {resume_data['personal_info']['phone']}
                    {f"| LinkedIn: {resume_data['personal_info']['linkedin']}" if resume_data['personal_info']['linkedin'] else ""}
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">Education</h2>
                <p><strong>{resume_data['education']['degree']} in {resume_data['education']['major']}</strong></p>
                <p>{resume_data['education']['university']} | CGPA: {resume_data['education']['cgpa']} | Graduation: {resume_data['education']['year']}</p>
            </div>
        """
        
        # Add sections based on available data
        if resume_data.get('experience'):
            html += """
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">Experience</h2>
            """
            for exp in resume_data['experience']:
                html += f"""
                <div style="margin-bottom: 15px;">
                    <p><strong>{exp['position']}</strong> at {exp['company']}</p>
                    <p><em>{exp['duration']} | {exp['location']}</em></p>
                    <p style="white-space: pre-line;">{exp['description']}</p>
                </div>
                """
            html += "</div>"
        
        if resume_data.get('skills'):
            html += """
            <div style="margin-bottom: 20px;">
                <h2 style="color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 5px;">Skills</h2>
            """
            for category, skills in resume_data['skills'].items():
                if skills:
                    html += f"""
                    <p><strong>{category}:</strong> {', '.join(skills)}</p>
                    """
            html += "</div>"
        
        html += "</div>"
        return html
    
    def optimize_resume(self):
        """Optimize existing resume"""
        st.subheader("Optimize Existing Resume")
        
        st.info("Upload your resume for AI optimization and ATS compatibility check")
        
        uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT)", 
                                       type=['pdf', 'docx', 'txt'])
        
        if uploaded_file is not None:
            st.success(f"File uploaded: {uploaded_file.name}")
            
            # Show optimization options
            st.subheader("Optimization Options")
            
            col1, col2 = st.columns(2)
            with col1:
                target_role = st.text_input("Target Role for Optimization", 
                                          "Software Development Engineer")
                target_company = st.text_input("Target Company (Optional)")
            
            with col2:
                optimization_level = st.select_slider(
                    "Optimization Level",
                    options=["Light", "Moderate", "Aggressive"],
                    value="Moderate"
                )
            
            # Additional options
            optimization_features = st.multiselect(
                "Specific Optimizations:",
                ["Keyword Optimization", "ATS Compatibility", "Action Verb Enhancement",
                 "Quantifiable Metrics", "Length Optimization", "Formatting Check",
                 "Skill Gap Analysis", "Industry-specific Jargon"]
            )
            
            if st.button("🔍 Analyze and Optimize Resume"):
                with st.spinner("AI is analyzing your resume..."):
                    # Simulate AI processing
                    import time
                    time.sleep(2)
                    
                    # Show results
                    st.success("Analysis Complete!")
                    
                    # Display optimization report
                    st.subheader("📊 Optimization Report")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("ATS Score", "78/100", "+15")
                    with col2:
                        st.metric("Keyword Match", "65%", "+25%")
                    with col3:
                        st.metric("Readability", "Good", "Improved")
                    
                    # Recommendations
                    st.subheader("🤖 AI Recommendations")
                    
                    recommendations = [
                        "**1. Add more action verbs:** Replace passive language with strong action verbs",
                        "**2. Include quantifiable metrics:** Add numbers to show impact (e.g., 'Improved performance by 30%')",
                        "**3. Optimize for keywords:** Add relevant keywords: 'agile methodology', 'SDLC', 'cross-functional teams'",
                        "**4. Improve formatting:** Use consistent bullet points and spacing",
                        "**5. Add missing sections:** Consider adding a 'Projects' section if applicable"
                    ]
                    
                    for rec in recommendations:
                        st.info(rec)
    
    def ats_checker(self):
        """ATS (Applicant Tracking System) checker"""
        st.subheader("ATS Compatibility Checker")
        
        st.warning("""
        ⚠️ **Important:** Many companies use ATS to filter resumes before human review.
        This tool checks if your resume will pass through common ATS systems.
        """)
        
        # ATS check options
        ats_systems = st.multiselect(
            "Select ATS systems to check against:",
            ["Workday", "Greenhouse", "Lever", "Taleo", "ICIMS", "BambooHR", "SuccessFactors"],
            default=["Workday", "Greenhouse"]
        )
        
        # Resume text input
        resume_text = st.text_area(
            "Paste your resume text here for ATS analysis:",
            height=200,
            value="""John Doe
Software Developer
Skills: Python, JavaScript, React
Experience: Developed web applications at Tech Company"""
        )
        
        if st.button("🔍 Check ATS Compatibility"):
            # Simulate ATS analysis
            with st.spinner("Analyzing resume for ATS compatibility..."):
                import time
                time.sleep(3)
                
                # Display results
                st.success("ATS Analysis Complete!")
                
                # ATS Score
                ats_score = 72
                st.subheader(f"ATS Score: {ats_score}/100")
                st.progress(ats_score / 100)
                
                # Detailed analysis
                st.subheader("Detailed Analysis")
                
                analysis_data = {
                    "Category": ["Formatting", "Keywords", "Readability", "Length", "File Type"],
                    "Score": [85, 65, 90, 78, 95],
                    "Status": ["✅ Good", "⚠️ Needs Work", "✅ Excellent", "✅ Good", "✅ Excellent"],
                    "Recommendation": [
                        "Proper use of headings and bullet points",
                        "Add more industry-specific keywords",
                        "Clear and concise language",
                        "Optimal 1-2 page length",
                        "PDF format recommended"
                    ]
                }
                
                st.dataframe(pd.DataFrame(analysis_data), use_container_width=True)
                
                # Critical issues
                st.subheader("⚠️ Critical Issues Found")
                issues = [
                    "**1. Missing Keywords:** Add more technical keywords relevant to software development roles",
                    "**2. No Quantifiable Results:** Add metrics and numbers to show impact",
                    "**3. Could use more action verbs:** Start bullet points with strong action verbs",
                    "**4. Consider adding a summary section:** Helps ATS understand your profile"
                ]
                
                for issue in issues:
                    st.error(issue)
    
    def demo_mode(self):
        """Demo mode with sample data"""
        st.info("🎮 **Demo Mode:** Using sample student data for demonstration")
        
        # Sample student data
        sample_data = {
            'personal_info': {
                'name': 'Rahul Sharma',
                'email': 'rahul.sharma@example.com',
                'phone': '+91 9876543210',
                'linkedin': 'linkedin.com/in/rahulsharma',
                'github': 'github.com/rahulsharma',
                'portfolio': 'rahulsharma.dev'
            },
            'education': {
                'degree': 'Bachelor of Technology',
                'university': 'Indian Institute of Technology',
                'major': 'Computer Science and Engineering',
                'cgpa': 8.7,
                'year': 2024,
                'location': 'Mumbai, India'
            },
            'experience': [
                {
                    'company': 'Tech Innovations Pvt Ltd',
                    'position': 'Software Developer Intern',
                    'duration': 'June 2023 - Present',
                    'location': 'Bangalore, India',
                    'description': '• Developed and maintained web applications using React and Node.js\n• Collaborated with cross-functional teams to implement new features\n• Reduced page load time by 30% through performance optimization'
                }
            ],
            'skills': {
                'Technical Skills': ['Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker'],
                'Soft Skills': ['Communication', 'Problem Solving', 'Teamwork'],
                'Tools': ['Git', 'VS Code', 'JIRA', 'Postman']
            },
            'projects': [
                {
                    'title': 'Campus Placement Portal',
                    'technologies': 'Python, Streamlit, Machine Learning',
                    'duration': 'Jan 2024 - Present',
                    'link': 'github.com/rahulsharma/placement-portal',
                    'description': '• Developed an AI-powered campus placement management system\n• Implemented resume optimization and placement prediction features\n• Used by 500+ students for career guidance'
                }
            ],
            'template': 'Professional',
            'ai_enhancements': ['Optimize Keywords for ATS', 'Add Metrics and Quantifiable Results'],
            'generated_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Show sample data
        with st.expander("📋 View Sample Data", expanded=False):
            st.json(sample_data, expanded=False)
        
        # Direct generate button for demo
        if st.button("🚀 Generate Sample Resume", type="primary"):
            self.generate_resume(sample_data)
