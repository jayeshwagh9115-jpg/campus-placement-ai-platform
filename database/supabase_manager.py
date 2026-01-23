import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

load_dotenv()

class SupabaseManager:
    def __init__(self):
        self.is_connected = False
        self.client = None
        
        # Get Supabase credentials - only URL and KEY are needed
        self.url = st.secrets.get("SUPABASE_URL", os.environ.get("https://ptnozudvgcqhnmidjoqj.supabase.co"))
        self.key = st.secrets.get("SUPABASE_KEY", os.environ.get("sb_publishable_WRZY__f0rKmSL0r5KCmZqA_yWf64uW0"))
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
                # Test connection with a safer query
                self.client.from_('students').select('id').limit(1).execute()
                self.is_connected = True
                print("✅ Connected to Supabase")
            except Exception as e:
                print(f"❌ Supabase connection error: {e}")
                self.is_connected = False
        else:
            print("⚠️ Supabase credentials not found")
            self.is_connected = False
    
    # ---------- STUDENT OPERATIONS ----------
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        """Create a new student record"""
        try:
            response = self.client.table('students').insert(student_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating student: {e}")
            return None
    
    def get_students(self, college_id: Optional[str] = None) -> List[Dict]:
        """Get all students or students from specific college"""
        try:
            query = self.client.table('students').select("*")
            if college_id:
                query = query.eq('college_id', college_id)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching students: {e}")
            return []
    
    def get_student_by_email(self, email: str) -> Optional[Dict]:
        """Get student by email"""
        try:
            response = self.client.table('students').select("*").eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error fetching student by email: {e}")
            return None
    
    def update_student(self, student_id: str, updates: Dict) -> Optional[Dict]:
        """Update student record"""
        try:
            response = self.client.table('students').update(updates).eq('id', student_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating student: {e}")
            return None
    
    # ---------- COLLEGE OPERATIONS ----------
    def create_college(self, college_data: Dict) -> Optional[Dict]:
        """Create a new college record"""
        try:
            response = self.client.table('colleges').insert(college_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating college: {e}")
            return None
    
    def get_colleges(self) -> List[Dict]:
        """Get all colleges"""
        try:
            response = self.client.table('colleges').select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching colleges: {e}")
            return []
    
    def get_college_by_email(self, email: str) -> Optional[Dict]:
        """Get college by email"""
        try:
            response = self.client.table('colleges').select("*").eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error fetching college by email: {e}")
            return None
    
    # ---------- COMPANY OPERATIONS ----------
    def create_company(self, company_data: Dict) -> Optional[Dict]:
        """Create a new company record"""
        try:
            response = self.client.table('companies').insert(company_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating company: {e}")
            return None
    
    def get_companies(self) -> List[Dict]:
        """Get all companies"""
        try:
            response = self.client.table('companies').select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching companies: {e}")
            return []
    
    def get_company_by_email(self, email: str) -> Optional[Dict]:
        """Get company by email"""
        try:
            response = self.client.table('companies').select("*").eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error fetching company by email: {e}")
            return None
    
    # ---------- JOB OPERATIONS ----------
    def create_job_posting(self, job_data: Dict) -> Optional[Dict]:
        """Create a new job posting"""
        try:
            response = self.client.table('job_postings').insert(job_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating job posting: {e}")
            return None
    
    def get_jobs(self, company_id: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Get all jobs or filter by company/status"""
        try:
            query = self.client.table('job_postings').select("*, companies(*)")
            if company_id:
                query = query.eq('company_id', company_id)
            if status:
                query = query.eq('status', status)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching jobs: {e}")
            return []
    
    def update_job_status(self, job_id: str, status: str) -> Optional[Dict]:
        """Update job status"""
        try:
            response = self.client.table('job_postings').update({'status': status}).eq('id', job_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating job status: {e}")
            return None
    
    # ---------- APPLICATION OPERATIONS ----------
    def create_application(self, application_data: Dict) -> Optional[Dict]:
        """Create a new application"""
        try:
            response = self.client.table('applications').insert(application_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating application: {e}")
            return None
    
    def get_applications(self, student_id: Optional[str] = None, 
                         job_id: Optional[str] = None,
                         company_id: Optional[str] = None) -> List[Dict]:
        """Get applications with optional filters"""
        try:
            query = self.client.table('applications').select("""
                *,
                students (*),
                job_postings (*, companies (*))
            """)
            
            if student_id:
                query = query.eq('student_id', student_id)
            if job_id:
                query = query.eq('job_id', job_id)
            if company_id:
                query = query.eq('job_postings.company_id', company_id)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Error fetching applications: {e}")
            return []
    
    def update_application_status(self, application_id: str, status: str, notes: str = None) -> Optional[Dict]:
        """Update application status"""
        try:
            updates = {'status': status}
            if notes:
                updates['notes'] = notes
            response = self.client.table('applications').update(updates).eq('id', application_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error updating application: {e}")
            return None
    
    # ---------- STATISTICS OPERATIONS ----------
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        try:
            stats = {}
            
            # Get counts
            students_count = self.client.table('students').select('count', count='exact').execute()
            companies_count = self.client.table('companies').select('count', count='exact').execute()
            jobs_count = self.client.table('job_postings').select('count', count='exact').eq('status', 'open').execute()
            applications_count = self.client.table('applications').select('count', count='exact').execute()
            
            stats['total_students'] = students_count.count if students_count.count else 0
            stats['total_companies'] = companies_count.count if companies_count.count else 0
            stats['active_jobs'] = jobs_count.count if jobs_count.count else 0
            stats['total_applications'] = applications_count.count if applications_count.count else 0
            
            # Get recent activities
            recent_jobs = self.client.table('job_postings').select("*, companies(name)").order('created_at', desc=True).limit(5).execute()
            recent_apps = self.client.table('applications').select("*, students(full_name), job_postings(title)").order('applied_at', desc=True).limit(5).execute()
            
            stats['recent_jobs'] = recent_jobs.data if recent_jobs.data else []
            stats['recent_applications'] = recent_apps.data if recent_apps.data else []
            
            return stats
        except Exception as e:
            st.error(f"Error fetching dashboard stats: {e}")
            return {}
