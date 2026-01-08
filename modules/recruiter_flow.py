import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

class RecruiterFlow:
    def __init__(self):
        self.recruiter_data = self.initialize_recruiter_data()
    
    def initialize_recruiter_data(self):
        """Initialize recruiter data with sample data for demonstration"""
        return {
            "company_profile": {
                "name": "TechCorp Solutions",
                "industry": "IT/Software",
                "website": "www.techcorp.com",
                "contact": {
                    "person": "John Doe",
                    "email": "john@techcorp.com",
                    "phone": "+91 9876543210",
                    "hr_email": "hr@techcorp.com"
                },
                "description": "Leading technology solutions provider"
            },
            "job_postings": [
                {
                    "id": "JOB001",
                    "title": "Software Development Engineer",
                    "type": "Full-time",
                    "location": "Bangalore",
                    "salary": 12.0,
                    "vacancies": 5,
                    "requirements": {
                        "cgpa_min": 7.0,
                        "backlogs_allowed": 2,
                        "skills": ["Python", "SQL", "Java"]
                    },
                    "description": "We are looking for a talented software engineer...",
                    "posted_date": "2024-01-15",
                    "status": "Active"
                }
            ],
            "candidates": [
                {
                    "id": "CAND001",
                    "name": "Alice Johnson",
                    "email": "alice@email.com",
                    "phone": "+91 9123456789",
                    "college": "IIT Bombay",
                    "cgpa": 8.5,
                    "backlogs": 0,
                    "skills": ["Python", "Java", "SQL", "React"],
                    "experience": "1 year",
                    "applied_jobs": ["JOB001"],
                    "status": "Screened",
                    "matching_score": 85
                },
                {
                    "id": "CAND002",
                    "name": "Bob Smith",
                    "email": "bob@email.com",
                    "phone": "+91 9876543210",
                    "college": "NIT Trichy",
                    "cgpa": 7.8,
                    "backlogs": 1,
                    "skills": ["Python", "JavaScript", "AWS"],
                    "experience": "Fresh Graduate",
                    "applied_jobs": ["JOB001"],
                    "status": "Pending",
                    "matching_score": 72
                }
            ],
            "interviews": [
                {
                    "id": "INT001",
                    "candidate_id": "CAND001",
                    "candidate_name": "Alice Johnson",
                    "job_id": "JOB001",
                    "job_title": "Software Development Engineer",
                    "interview_type": "Technical Round",
                    "scheduled_date": "2024-01-25",
                    "scheduled_time": "10:00 AM",
                    "interviewer": "Tech Lead",
                    "status": "Scheduled",
                    "feedback": ""
                }
            ],
            "offers": [],
            "analytics": {
                "total_applications": 150,
                "shortlisted": 45,
                "interviews": 25,
                "offers": 8,
                "hires": 5,
                "time_to_hire": 30  # days
            }
        }
    
    def display(self):
        """Display recruiter workflow"""
        st.header("💼 Recruiter Hiring Platform")
        
        # Create sidebar navigation for recruiter workflow
        with st.sidebar:
            st.subheader("📋 Recruiter Hiring Process")
            
            # Define all steps
            steps = [
                "🏢 Company Profile",
                "📋 Job Posting",
                "🔍 Candidate Search",
                "🤖 AI Screening",
                "📅 Interview Scheduling",
                "⭐ Candidate Evaluation",
                "📄 Offer Management",
                "📊 Hiring Analytics"
            ]
            
            # Get current step from URL or session state
            if 'recruiter_step' not in st.session_state:
                st.session_state.recruiter_step = 1
            
            # Create step selection
            selected_step = st.radio(
                "Select Step:",
                steps,
                index=st.session_state.recruiter_step - 1
            )
            
            # Update current step based on selection
            step_index = steps.index(selected_step) + 1
            st.session_state.recruiter_step = step_index
            
            # Display status
            st.divider()
            st.caption(f"**Current Step:** {step_index}/8")
            
            # Navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Previous", disabled=(step_index == 1)):
                    st.session_state.recruiter_step -= 1
                    st.rerun()
            with col2:
                if st.button("Next →", disabled=(step_index == 8)):
                    st.session_state.recruiter_step += 1
                    st.rerun()
        
        # Display step based on current step
        current_step = st.session_state.recruiter_step
        
        if current_step == 1:
            self.step1_company_profile()
        elif current_step == 2:
            self.step2_job_posting()
        elif current_step == 3:
            self.step3_candidate_search()
        elif current_step == 4:
            self.step4_ai_screening()
        elif current_step == 5:
            self.step5_interview_scheduling()
        elif current_step == 6:
            self.step6_candidate_evaluation()
        elif current_step == 7:
            self.step7_offer_management()
        elif current_step == 8:
            self.step8_hiring_analytics()
    
    def step1_company_profile(self):
        """Step 1: Company Profile"""
        st.subheader("🏢 Company Profile Setup")
        
        # Load existing data if available
        company_profile = self.recruiter_data["company_profile"]
        
        with st.form("company_profile_form"):
            company_name = st.text_input("Company Name*", 
                                         value=company_profile.get("name", ""))
            
            industry = st.selectbox("Industry*",
                ["IT/Software", "Finance/Banking", "Consulting", "Manufacturing",
                 "E-commerce", "Healthcare", "Education", "Automotive", "Retail", "Telecom"],
                index=["IT/Software", "Finance/Banking", "Consulting", "Manufacturing",
                      "E-commerce", "Healthcare", "Education", "Automotive", "Retail", "Telecom"]
                      .index(company_profile.get("industry", "IT/Software")) if company_profile.get("industry") else 0)
            
            website = st.text_input("Website", value=company_profile.get("website", ""))
            
            col1, col2 = st.columns(2)
            with col1:
                contact_person = st.text_input("Contact Person*", 
                                               value=company_profile.get("contact", {}).get("person", ""))
                email = st.text_input("Email*", 
                                      value=company_profile.get("contact", {}).get("email", ""))
            with col2:
                phone = st.text_input("Phone*", 
                                      value=company_profile.get("contact", {}).get("phone", ""))
                hr_email = st.text_input("HR Email for Applications", 
                                         value=company_profile.get("contact", {}).get("hr_email", ""))
            
            company_description = st.text_area("Company Description", 
                                               value=company_profile.get("description", ""),
                                               height=150,
                                               placeholder="Describe your company culture, mission, and values...")
            
            submitted = st.form_submit_button("💾 Save Company Profile")
            
            if submitted:
                if not all([company_name, industry, contact_person, email, phone]):
                    st.error("Please fill in all required fields (*)")
                else:
                    self.recruiter_data["company_profile"] = {
                        "name": company_name,
                        "industry": industry,
                        "website": website,
                        "contact": {
                            "person": contact_person,
                            "email": email,
                            "phone": phone,
                            "hr_email": hr_email
                        },
                        "description": company_description
                    }
                    st.success("✅ Company profile saved successfully!")
                    st.balloons()
    
    def step2_job_posting(self):
        """Step 2: Job Posting"""
        st.subheader("📋 Create Job Posting")
        
        if not self.recruiter_data["company_profile"]:
            st.warning("⚠️ Please complete company profile first!")
            return
        
        with st.form("job_posting_form"):
            job_title = st.text_input("Job Title*", "Software Development Engineer")
            
            col1, col2 = st.columns(2)
            with col1:
                job_type = st.selectbox("Job Type*", 
                    ["Full-time", "Internship", "Contract", "Part-time", "Remote"])
                location = st.text_input("Location*", "Bangalore")
            with col2:
                salary = st.number_input("Salary (LPA)", 0.0, 100.0, 12.0, 1.0)
                vacancies = st.number_input("Vacancies", 1, 100, 5)
            
            # Requirements section
            st.subheader("📋 Requirements")
            
            col3, col4 = st.columns(2)
            with col3:
                cgpa_min = st.number_input("Minimum CGPA", 0.0, 10.0, 7.0, 0.1)
            with col4:
                backlogs_allowed = st.number_input("Maximum Backlogs Allowed", 0, 10, 2)
            
            # Experience
            experience = st.selectbox("Experience Required",
                ["Fresher", "0-1 years", "1-3 years", "3-5 years", "5+ years"])
            
            # Skills
            st.write("**Required Skills:**")
            skill_categories = {
                "Programming": ["Python", "Java", "C++", "JavaScript", "Go", "Rust"],
                "Web Development": ["React", "Angular", "Vue.js", "Node.js", "Django", "Flask"],
                "Databases": ["SQL", "MongoDB", "PostgreSQL", "Redis", "Oracle"],
                "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD"],
                "Data Science": ["Machine Learning", "Data Analysis", "TensorFlow", "PyTorch"],
                "Soft Skills": ["Communication", "Problem Solving", "Teamwork", "Leadership"]
            }
            
            selected_skills = []
            for category, skills in skill_categories.items():
                with st.expander(f"📁 {category}"):
                    cat_skills = st.multiselect(f"Select {category} skills:", 
                                                skills, 
                                                key=f"skills_{category}")
                    selected_skills.extend(cat_skills)
            
            job_description = st.text_area("Job Description*", height=200,
                value="""We are looking for a talented software engineer to join our team.

Responsibilities:
- Design, develop and maintain software applications
- Collaborate with cross-functional teams
- Write clean, efficient, and well-documented code
- Participate in code reviews and team meetings

Requirements:
- Strong problem-solving skills
- Good understanding of software development principles
- Ability to work in a fast-paced environment""")
            
            col5, col6 = st.columns(2)
            with col5:
                application_deadline = st.date_input("Application Deadline", 
                                                    datetime.now() + timedelta(days=30))
            with col6:
                is_remote = st.checkbox("Remote Work Allowed")
            
            if st.form_submit_button("📢 Post Job"):
                job_id = f"JOB{len(self.recruiter_data['job_postings']) + 1:03d}"
                self.recruiter_data["job_postings"].append({
                    "id": job_id,
                    "title": job_title,
                    "type": job_type,
                    "location": location,
                    "salary": salary,
                    "vacancies": vacancies,
                    "requirements": {
                        "cgpa_min": cgpa_min,
                        "backlogs_allowed": backlogs_allowed,
                        "experience": experience,
                        "skills": selected_skills,
                        "remote_allowed": is_remote
                    },
                    "description": job_description,
                    "posted_date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "deadline": application_deadline.strftime("%Y-%m-%d"),
                    "status": "Active",
                    "applications": 0
                })
                st.success(f"✅ Job posted successfully! Job ID: {job_id}")
                st.balloons()
        
        # Display existing job postings
        if self.recruiter_data["job_postings"]:
            st.divider()
            st.subheader("📋 Active Job Postings")
            
            for job in self.recruiter_data["job_postings"]:
                with st.expander(f"{job['id']} - {job['title']} ({job['location']})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Salary", f"₹{job['salary']} LPA")
                    with col2:
                        st.metric("Vacancies", job['vacancies'])
                    with col3:
                        st.metric("Type", job['type'])
                    
                    st.write(f"**Requirements:** CGPA ≥ {job['requirements']['cgpa_min']}, "
                            f"Backlogs ≤ {job['requirements']['backlogs_allowed']}")
                    st.write(f"**Skills:** {', '.join(job['requirements']['skills'])}")
                    st.write(f"**Posted:** {job['posted_date']}")
                    
                    if st.button(f"View Applications", key=f"view_{job['id']}"):
                        st.session_state.recruiter_step = 3
                        st.rerun()
    
    def step3_candidate_search(self):
        """Step 3: Candidate Search"""
        st.subheader("🔍 Candidate Search & Filtering")
        
        if not self.recruiter_data["job_postings"]:
            st.warning("⚠️ Please create a job posting first!")
            return
        
        # Search and filter section
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Search by Name", "")
        with col2:
            search_skills = st.text_input("Search by Skills", "")
        with col3:
            job_filter = st.selectbox("Filter by Job", 
                                     ["All Jobs"] + [job["title"] for job in self.recruiter_data["job_postings"]])
        
        # Advanced filters
        with st.expander("🔧 Advanced Filters"):
            col4, col5, col6 = st.columns(3)
            with col4:
                min_cgpa = st.slider("Minimum CGPA", 0.0, 10.0, 7.0, 0.5)
            with col5:
                max_backlogs = st.slider("Maximum Backlogs", 0, 10, 2)
            with col6:
                experience_filter = st.selectbox("Experience Level",
                                                ["All", "Fresher", "0-1 years", "1-3 years", "3+ years"])
        
        # Display candidates
        st.subheader("👥 Candidate Pool")
        
        # Create dataframe for display
        candidates_df = pd.DataFrame(self.recruiter_data["candidates"])
        
        if not candidates_df.empty:
            # Apply filters
            filtered_df = candidates_df.copy()
            
            if search_name:
                filtered_df = filtered_df[filtered_df["name"].str.contains(search_name, case=False, na=False)]
            
            if search_skills:
                filtered_df = filtered_df[filtered_df["skills"].apply(
                    lambda x: any(skill.lower() in str(x).lower() for skill in search_skills.split(","))
                )]
            
            if min_cgpa > 0:
                filtered_df = filtered_df[filtered_df["cgpa"] >= min_cgpa]
            
            filtered_df = filtered_df[filtered_df["backlogs"] <= max_backlogs]
            
            if experience_filter != "All":
                filtered_df = filtered_df[filtered_df["experience"] == experience_filter]
            
            # Display candidates
            for idx, candidate in filtered_df.iterrows():
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        st.write(f"**{candidate['name']}**")
                        st.write(f"📧 {candidate['email']} | 📞 {candidate['phone']}")
                        st.write(f"🎓 {candidate['college']} | 📊 CGPA: {candidate['cgpa']}")
                        st.write(f"🛠️ Skills: {', '.join(candidate['skills'])}")
                    
                    with col2:
                        st.metric("Match Score", f"{candidate.get('matching_score', 0)}%")
                        st.write(f"📅 Experience: {candidate['experience']}")
                        st.write(f"📝 Backlogs: {candidate['backlogs']}")
                    
                    with col3:
                        status_color = {
                            "Pending": "gray",
                            "Screened": "blue",
                            "Shortlisted": "green",
                            "Rejected": "red"
                        }.get(candidate["status"], "gray")
                        
                        st.markdown(f"<p style='color:{status_color};'><b>{candidate['status']}</b></p>", 
                                  unsafe_allow_html=True)
                        
                        if st.button("View Profile", key=f"view_{candidate['id']}"):
                            # Store selected candidate in session state
                            st.session_state.selected_candidate = candidate.to_dict()
                            st.session_state.recruiter_step = 4
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("No candidates found. Candidates will appear here as they apply.")
    
    def step4_ai_screening(self):
        """Step 4: AI-powered Candidate Screening"""
        st.subheader("🤖 AI-powered Candidate Screening")
        
        # Get selected candidate from session state
        selected_candidate = st.session_state.get('selected_candidate')
        
        if not selected_candidate:
            st.warning("Please select a candidate first from Candidate Search")
            st.button("← Back to Candidate Search", on_click=lambda: setattr(st.session_state, 'recruiter_step', 3))
            return
        
        # Display candidate info
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Candidate:** {selected_candidate['name']}")
            st.write(f"**Email:** {selected_candidate['email']}")
            st.write(f"**College:** {selected_candidate['college']}")
            st.write(f"**CGPA:** {selected_candidate['cgpa']}")
            st.write(f"**Experience:** {selected_candidate['experience']}")
        with col2:
            # AI Matching Score
            score = selected_candidate.get('matching_score', random.randint(70, 95))
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "AI Match Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 80
                    }
                }
            ))
            fig.update_layout(height=200)
            st.plotly_chart(fig, use_container_width=True)
        
        # Skills Analysis
        st.subheader("🛠️ Skills Analysis")
        
        # Mock skills analysis
        required_skills = ["Python", "SQL", "Java", "Communication"]
        candidate_skills = selected_candidate['skills']
        
        skill_data = []
        for skill in required_skills:
            has_skill = skill in candidate_skills
            skill_data.append({
                "Skill": skill,
                "Status": "Present" if has_skill else "Missing",
                "Match": has_skill
            })
        
        skill_df = pd.DataFrame(skill_data)
        
        # Display skills analysis
        for skill in skill_data:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{skill['Skill']}**")
            with col2:
                if skill['Match']:
                    st.success("✓ Present")
                else:
                    st.error("✗ Missing")
        
        # Resume Parser (Mock)
        st.subheader("📄 Resume Insights")
        
        with st.expander("View AI-generated Insights"):
            insights = [
                "✅ Strong educational background from reputable institution",
                "✅ Relevant technical skills match job requirements",
                "✅ Good academic performance with CGPA above threshold",
                "⚠️ Limited internship experience in the field",
                "✅ Projects demonstrate practical application of skills",
                "⚠️ Could benefit from more leadership experience"
            ]
            
            for insight in insights:
                st.write(insight)
        
        # Screening Decision
        st.subheader("📋 Screening Decision")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Shortlist Candidate", type="primary", use_container_width=True):
                # Update candidate status
                for candidate in self.recruiter_data["candidates"]:
                    if candidate["id"] == selected_candidate["id"]:
                        candidate["status"] = "Shortlisted"
                        break
                st.success("Candidate shortlisted!")
                st.balloons()
                
        with col2:
            if st.button("⏸️ Keep for Review", use_container_width=True):
                st.info("Candidate marked for review")
                
        with col3:
            if st.button("❌ Reject", use_container_width=True):
                for candidate in self.recruiter_data["candidates"]:
                    if candidate["id"] == selected_candidate["id"]:
                        candidate["status"] = "Rejected"
                        break
                st.warning("Candidate rejected")
        
        # Navigation
        st.divider()
        if st.button("← Back to Candidate Search"):
            st.session_state.recruiter_step = 3
            st.rerun()
        
        if st.button("📅 Schedule Interview →"):
            st.session_state.recruiter_step = 5
            st.rerun()
    
    def step5_interview_scheduling(self):
        """Step 5: Interview Scheduling"""
        st.subheader("📅 Interview Scheduling")
        
        # Get shortlisted candidates
        shortlisted = [c for c in self.recruiter_data["candidates"] if c["status"] == "Shortlisted"]
        
        if not shortlisted:
            st.warning("No shortlisted candidates available. Please shortlist candidates first.")
            st.button("← Back to AI Screening", on_click=lambda: setattr(st.session_state, 'recruiter_step', 4))
            return
        
        # Schedule new interview
        with st.form("interview_schedule_form"):
            col1, col2 = st.columns(2)
            with col1:
                candidate = st.selectbox("Select Candidate*",
                                        [f"{c['id']} - {c['name']}" for c in shortlisted])
                interview_type = st.selectbox("Interview Type*",
                                            ["Technical Round", "HR Round", "Managerial Round",
                                             "Cultural Fit", "Final Round"])
            with col2:
                scheduled_date = st.date_input("Interview Date*", datetime.now() + timedelta(days=7))
                scheduled_time = st.time_input("Interview Time*", datetime.strptime("10:00", "%H:%M"))
                duration = st.selectbox("Duration", ["30 mins", "45 mins", "1 hour", "1.5 hours", "2 hours"])
            
            interviewer = st.text_input("Interviewer Name*", "Tech Lead")
            meeting_link = st.text_input("Meeting Link/Platform", "https://meet.google.com/xxx-xxxx-xxx")
            additional_notes = st.text_area("Additional Notes", height=100)
            
            if st.form_submit_button("📅 Schedule Interview"):
                candidate_id = candidate.split(" - ")[0]
                candidate_name = candidate.split(" - ")[1]
                
                # Find job candidate applied for
                applied_job = None
                for cand in self.recruiter_data["candidates"]:
                    if cand["id"] == candidate_id:
                        applied_job = cand["applied_jobs"][0] if cand["applied_jobs"] else "JOB001"
                        candidate_name = cand["name"]
                        break
                
                # Get job title
                job_title = "Software Development Engineer"
                for job in self.recruiter_data["job_postings"]:
                    if job["id"] == applied_job:
                        job_title = job["title"]
                        break
                
                interview_id = f"INT{len(self.recruiter_data['interviews']) + 1:03d}"
                self.recruiter_data["interviews"].append({
                    "id": interview_id,
                    "candidate_id": candidate_id,
                    "candidate_name": candidate_name,
                    "job_id": applied_job,
                    "job_title": job_title,
                    "interview_type": interview_type,
                    "scheduled_date": scheduled_date.strftime("%Y-%m-%d"),
                    "scheduled_time": scheduled_time.strftime("%I:%M %p"),
                    "duration": duration,
                    "interviewer": interviewer,
                    "meeting_link": meeting_link,
                    "notes": additional_notes,
                    "status": "Scheduled",
                    "feedback": ""
                })
                
                st.success(f"✅ Interview scheduled! Interview ID: {interview_id}")
        
        # Display scheduled interviews
        if self.recruiter_data["interviews"]:
            st.divider()
            st.subheader("🗓️ Upcoming Interviews")
            
            for interview in self.recruiter_data["interviews"]:
                if interview["status"] == "Scheduled":
                    with st.expander(f"{interview['id']} - {interview['candidate_name']} ({interview['interview_type']})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Date:** {interview['scheduled_date']}")
                            st.write(f"**Time:** {interview['scheduled_time']}")
                            st.write(f"**Duration:** {interview['duration']}")
                        with col2:
                            st.write(f"**Interviewer:** {interview['interviewer']}")
                            st.write(f"**Job:** {interview['job_title']}")
                            st.write(f"**Platform:** {interview['meeting_link']}")
                        
                        if st.button("Take Notes", key=f"notes_{interview['id']}"):
                            st.session_state.selected_interview = interview
                            st.session_state.recruiter_step = 6
                            st.rerun()
    
    def step6_candidate_evaluation(self):
        """Step 6: Candidate Evaluation"""
        st.subheader("⭐ Candidate Evaluation & Feedback")
        
        # Get interview from session state or select one
        selected_interview = st.session_state.get('selected_interview')
        
        if not selected_interview:
            # Let user select an interview
            scheduled_interviews = [i for i in self.recruiter_data["interviews"] if i["status"] == "Scheduled"]
            
            if not scheduled_interviews:
                st.warning("No interviews scheduled for evaluation.")
                st.button("← Back to Interview Scheduling", 
                         on_click=lambda: setattr(st.session_state, 'recruiter_step', 5))
                return
            
            interview_options = [f"{i['id']} - {i['candidate_name']} ({i['interview_type']})" 
                               for i in scheduled_interviews]
            selected_option = st.selectbox("Select Interview for Evaluation:", interview_options)
            
            if selected_option:
                interview_id = selected_option.split(" - ")[0]
                selected_interview = next(i for i in scheduled_interviews if i["id"] == interview_id)
        
        # Display interview details
        st.info(f"**Evaluating:** {selected_interview['candidate_name']} "
               f"for {selected_interview['job_title']} "
               f"({selected_interview['interview_type']})")
        
        # Evaluation form
        with st.form("evaluation_form"):
            st.subheader("Evaluation Criteria")
            
            # Technical Skills
            tech_score = st.slider("Technical Skills / Knowledge", 1, 10, 7)
            tech_feedback = st.text_area("Technical Feedback", height=100)
            
            # Problem Solving
            problem_score = st.slider("Problem Solving Ability", 1, 10, 7)
            problem_feedback = st.text_area("Problem Solving Feedback", height=100)
            
            # Communication
            comm_score = st.slider("Communication Skills", 1, 10, 7)
            comm_feedback = st.text_area("Communication Feedback", height=100)
            
            # Cultural Fit
            culture_score = st.slider("Cultural Fit", 1, 10, 7)
            culture_feedback = st.text_area("Cultural Fit Feedback", height=100)
            
            # Overall Feedback
            overall_feedback = st.text_area("Overall Feedback & Notes", height=150)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                recommendation = st.selectbox("Recommendation",
                                            ["Strong Hire", "Hire", "No Hire", "Strong No Hire"])
            with col2:
                next_steps = st.selectbox("Next Steps",
                                         ["Next Round", "Final Round", "Offer", "Reject", "On Hold"])
            with col3:
                overall_rating = st.selectbox("Overall Rating", 
                                            ["Excellent (9-10)", "Good (7-8)", "Average (5-6)", "Poor (1-4)"])
            
            if st.form_submit_button("📝 Submit Evaluation"):
                # Calculate average score
                avg_score = (tech_score + problem_score + comm_score + culture_score) / 4
                
                # Update interview with feedback
                for interview in self.recruiter_data["interviews"]:
                    if interview["id"] == selected_interview["id"]:
                        interview["status"] = "Completed"
                        interview["feedback"] = {
                            "technical": {"score": tech_score, "feedback": tech_feedback},
                            "problem_solving": {"score": problem_score, "feedback": problem_feedback},
                            "communication": {"score": comm_score, "feedback": comm_feedback},
                            "cultural_fit": {"score": culture_score, "feedback": culture_feedback},
                            "overall_feedback": overall_feedback,
                            "recommendation": recommendation,
                            "next_steps": next_steps,
                            "overall_rating": overall_rating,
                            "average_score": avg_score,
                            "evaluated_date": datetime.now().strftime("%Y-%m-%d")
                        }
                        break
                
                # Update candidate status
                for candidate in self.recruiter_data["candidates"]:
                    if candidate["id"] == selected_interview["candidate_id"]:
                        candidate["status"] = next_steps
                        candidate["interview_score"] = avg_score
                        break
                
                st.success("✅ Evaluation submitted successfully!")
                
                # Auto-create offer for strong candidates
                if recommendation in ["Strong Hire", "Hire"] and next_steps == "Offer":
                    st.info("Candidate recommended for hire. Proceeding to Offer Management...")
                    st.session_state.recruiter_step = 7
                    st.rerun()
        
        # Navigation
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Interviews"):
                st.session_state.recruiter_step = 5
                st.rerun()
        with col2:
            if st.button("Manage Offers →"):
                st.session_state.recruiter_step = 7
                st.rerun()
    
    def step7_offer_management(self):
        """Step 7: Offer Management"""
        st.subheader("📄 Offer Management")
        
        # Get candidates ready for offer
        offer_candidates = [c for c in self.recruiter_data["candidates"] 
                          if c.get("status") in ["Offer", "Final Round"]]
        
        if not offer_candidates:
            st.info("No candidates ready for offer yet. Complete evaluations first.")
            st.button("← Back to Evaluations", 
                     on_click=lambda: setattr(st.session_state, 'recruiter_step', 6))
            return
        
        # Create new offer
        with st.form("offer_form"):
            col1, col2 = st.columns(2)
            with col1:
                candidate = st.selectbox("Select Candidate*",
                                        [f"{c['id']} - {c['name']}" for c in offer_candidates])
                position = st.text_input("Position*", "Software Development Engineer")
            with col2:
                offered_salary = st.number_input("Offered Salary (LPA)*", 0.0, 100.0, 12.0, 1.0)
                joining_date = st.date_input("Joining Date*", datetime.now() + timedelta(days=30))
            
            # Benefits
            st.subheader("💰 Benefits & Perks")
            
            col3, col4 = st.columns(2)
            with col3:
                signing_bonus = st.number_input("Signing Bonus", 0, 500000, 100000, 50000)
                health_insurance = st.checkbox("Health Insurance", value=True)
                pf_contribution = st.checkbox("PF Contribution", value=True)
            with col4:
                stock_options = st.checkbox("Stock Options")
                relocation_assistance = st.checkbox("Relocation Assistance")
                annual_bonus = st.number_input("Annual Bonus (%)", 0, 50, 10, 5)
            
            # Offer letter content
            offer_letter = st.text_area("Offer Letter Content*", height=200,
                value=f"""Dear [Candidate],

We are pleased to offer you the position of {position} at TechCorp Solutions.

Position: {position}
Salary: ₹{offered_salary} LPA per annum
Joining Date: {joining_date.strftime('%B %d, %Y')}

Benefits:
- Health Insurance
- Provident Fund
- Annual Bonus: {annual_bonus}%
- Signing Bonus: ₹{signing_bonus:,}

Please sign and return this offer letter by [Date].

Sincerely,
HR Department
TechCorp Solutions""")
            
            if st.form_submit_button("📄 Generate Offer Letter"):
                candidate_id = candidate.split(" - ")[0]
                candidate_name = candidate.split(" - ")[1]
                
                offer_id = f"OFFER{len(self.recruiter_data.get('offers', [])) + 1:03d}"
                
                if "offers" not in self.recruiter_data:
                    self.recruiter_data["offers"] = []
                
                self.recruiter_data["offers"].append({
                    "id": offer_id,
                    "candidate_id": candidate_id,
                    "candidate_name": candidate_name,
                    "position": position,
                    "offered_salary": offered_salary,
                    "joining_date": joining_date.strftime("%Y-%m-%d"),
                    "benefits": {
                        "signing_bonus": signing_bonus,
                        "health_insurance": health_insurance,
                        "pf_contribution": pf_contribution,
                        "stock_options": stock_options,
                        "relocation_assistance": relocation_assistance,
                        "annual_bonus": annual_bonus
                    },
                    "offer_letter": offer_letter,
                    "status": "Pending",
                    "generated_date": datetime.now().strftime("%Y-%m-%d"),
                    "accepted_date": None,
                    "declined_date": None
                })
                
                st.success(f"✅ Offer letter generated! Offer ID: {offer_id}")
                
                # Download offer letter
                st.download_button(
                    label="📥 Download Offer Letter",
                    data=offer_letter,
                    file_name=f"Offer_Letter_{candidate_name.replace(' ', '_')}.txt",
                    mime="text/plain"
                )
        
        # Display existing offers
        if self.recruiter_data.get("offers"):
            st.divider()
            st.subheader("📋 Offer Status")
            
            offers_df = pd.DataFrame(self.recruiter_data["offers"])
            
            for idx, offer in offers_df.iterrows():
                status_color = {
                    "Pending": "orange",
                    "Accepted": "green",
                    "Declined": "red",
                    "Expired": "gray"
                }.get(offer["status"], "gray")
                
                with st.expander(f"{offer['id']} - {offer['candidate_name']} (Status: {offer['status']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Position:** {offer['position']}")
                        st.write(f"**Salary:** ₹{offer['offered_salary']} LPA")
                        st.write(f"**Joining Date:** {offer['joining_date']}")
                    with col2:
                        st.write(f"**Generated:** {offer['generated_date']}")
                        if offer['status'] == "Accepted":
                            st.write(f"**Accepted:** {offer.get('accepted_date', 'N/A')}")
                        
                        # Action buttons
                        if offer['status'] == "Pending":
                            col_accept, col_decline = st.columns(2)
                            with col_accept:
                                if st.button("Accept", key=f"accept_{offer['id']}"):
                                    # Update offer status
                                    for o in self.recruiter_data["offers"]:
                                        if o["id"] == offer["id"]:
                                            o["status"] = "Accepted"
                                            o["accepted_date"] = datetime.now().strftime("%Y-%m-%d")
                                            break
                                    st.rerun()
                            with col_decline:
                                if st.button("Decline", key=f"decline_{offer['id']}"):
                                    for o in self.recruiter_data["offers"]:
                                        if o["id"] == offer["id"]:
                                            o["status"] = "Declined"
                                            o["declined_date"] = datetime.now().strftime("%Y-%m-%d")
                                            break
                                    st.rerun()
        
        # Navigation
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Evaluations"):
                st.session_state.recruiter_step = 6
                st.rerun()
        with col2:
            if st.button("View Analytics →"):
                st.session_state.recruiter_step = 8
                st.rerun()
    
    def step8_hiring_analytics(self):
        """Step 8: Hiring Analytics Dashboard"""
        st.subheader("📊 Hiring Analytics Dashboard")
        
        # Key Metrics
        st.subheader("📈 Key Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Applications", self.recruiter_data["analytics"]["total_applications"])
        with col2:
            st.metric("Shortlisted", self.recruiter_data["analytics"]["shortlisted"])
        with col3:
            st.metric("Interviews", self.recruiter_data["analytics"]["interviews"])
        with col4:
            st.metric("Hires", self.recruiter_data["analytics"]["hires"])
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Application funnel
            st.subheader("📊 Application Funnel")
            
            funnel_data = pd.DataFrame({
                'Stage': ['Applications', 'Shortlisted', 'Interviews', 'Offers', 'Hires'],
                'Count': [
                    self.recruiter_data["analytics"]["total_applications"],
                    self.recruiter_data["analytics"]["shortlisted"],
                    self.recruiter_data["analytics"]["interviews"],
                    self.recruiter_data["analytics"]["offers"],
                    self.recruiter_data["analytics"]["hires"]
                ]
            })
            
            fig = px.funnel(funnel_data, x='Count', y='Stage', title='Hiring Funnel')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Time to hire distribution
            st.subheader("⏱️ Time to Hire")
            
            time_data = pd.DataFrame({
                'Stage': ['Screening', 'Interviews', 'Offer', 'Joining'],
                'Days': [5, 15, 5, 5]  # Mock data
            })
            
            fig = px.bar(time_data, x='Stage', y='Days', title='Average Time per Stage (Days)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Source of Hire
        st.subheader("📍 Source of Applications")
        
        source_data = pd.DataFrame({
            'Source': ['Campus', 'Job Portals', 'Referrals', 'Social Media', 'Direct'],
            'Applications': [45, 60, 25, 15, 5]
        })
        
        fig = px.pie(source_data, values='Applications', names='Source', title='Application Sources')
        st.plotly_chart(fig, use_container_width=True)
        
        # Skill Gap Analysis
        st.subheader("🛠️ Top Required Skills vs Available Skills")
        
        skill_data = pd.DataFrame({
            'Skill': ['Python', 'Java', 'SQL', 'Communication', 'Problem Solving'],
            'Required': [85, 70, 80, 90, 85],
            'Available': [75, 65, 70, 80, 75]
        })
        
        fig = go.Figure(data=[
            go.Bar(name='Required %', x=skill_data['Skill'], y=skill_data['Required']),
            go.Bar(name='Available %', x=skill_data['Skill'], y=skill_data['Available'])
        ])
        fig.update_layout(barmode='group', title='Skill Gap Analysis')
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost per Hire
        st.subheader("💰 Cost Analysis")
        
        cost_data = pd.DataFrame({
            'Component': ['Advertising', 'Agency Fees', 'Interview Costs', 'Relocation', 'Training'],
            'Cost (₹)': [50000, 100000, 25000, 75000, 50000]
        })
        
        fig = px.bar(cost_data, x='Component', y='Cost (₹)', title='Cost per Hire Breakdown')
        st.plotly_chart(fig, use_container_width=True)
        
        # Download Reports
        st.divider()
        st.subheader("📥 Reports")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📄 Generate Monthly Report", use_container_width=True):
                st.success("Monthly report generated!")
        with col2:
            if st.button("📊 Export Analytics", use_container_width=True):
                st.success("Analytics exported successfully!")
        with col3:
            if st.button("📈 Download Dashboard", use_container_width=True):
                st.success("Dashboard downloaded!")
        
        # Reset workflow
        st.divider()
        if st.button("🔄 Start New Hiring Cycle", type="primary"):
            # Reset recruiter data
            self.recruiter_data = self.initialize_recruiter_data()
            st.session_state.recruiter_step = 1
            st.success("New hiring cycle started!")
            st.rerun()

# For testing the module directly
if __name__ == "__main__":
    recruiter = RecruiterFlow()
    recruiter.display()
