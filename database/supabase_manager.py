import streamlit as st
from supabase import create_client, Client
import pandas as pd
from typing import Optional, Dict, List, Any
import json
from datetime import datetime

class SupabaseManager:
    """Manage database operations with Supabase"""
    
    def __init__(self):
        self.supabase: Optional[Client] = None
        self.is_connected = False
        
        # Get credentials from Streamlit secrets or environment variables
        try:
            supabase_url = st.secrets["supabase"]["url"]
            supabase_key = st.secrets["supabase"]["key"]
            self.supabase = create_client(supabase_url, supabase_key)
            self.is_connected = True
            st.success("✅ Connected to Supabase successfully!")
        except Exception as e:
            st.error(f"❌ Failed to connect to Supabase: {str(e)}")
            self.is_connected = False
    
    def check_connection(self):
        """Check if Supabase connection is active"""
        if not self.is_connected or not self.supabase:
            return False
        try:
            # Simple query to check connection
            self.supabase.table('students').select('id').limit(1).execute()
            return True
        except:
            return False
    
    # ============= STUDENT OPERATIONS =============
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        """Create a new student record"""
        try:
            response = self.supabase.table('students').insert(student_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating student: {str(e)}")
            return None
    
    def get_student(self, student_id: str) -> Optional[Dict]:
        """Get student by ID"""
        try:
            response = self.supabase.table('students').select('*').eq('id', student_id).execute()
            return response.data[0] if response.data else None
        except:
            return None
    
    def update_student(self, student_id: str, updates: Dict) -> bool:
        """Update student record"""
        try:
            response = self.supabase.table('students').update(updates).eq('id', student_id).execute()
            return True
        except Exception as e:
            st.error(f"Error updating student: {str(e)}")
            return False
    
    # ============= COMPANY/RECRUITER OPERATIONS =============
    def create_company(self, company_data: Dict) -> Optional[Dict]:
        """Create a new company record"""
        try:
            response = self.supabase.table('companies').insert(company_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating company: {str(e)}")
            return None
    
    def get_all_companies(self) -> List[Dict]:
        """Get all companies"""
        try:
            response = self.supabase.table('companies').select('*').execute()
            return response.data
        except:
            return []
    
    # ============= JOB OPERATIONS =============
    def create_job_posting(self, job_data: Dict) -> Optional[Dict]:
        """Create a new job posting"""
        try:
            response = self.supabase.table('job_postings').insert(job_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating job: {str(e)}")
            return None
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all job postings"""
        try:
            response = self.supabase.table('job_postings').select('*, companies(*)').execute()
            return response.data
        except:
            return []
    
    # ============= APPLICATION OPERATIONS =============
    def create_application(self, application_data: Dict) -> Optional[Dict]:
        """Create a new job application"""
        try:
            response = self.supabase.table('applications').insert(application_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating application: {str(e)}")
            return None
    
    def get_student_applications(self, student_id: str) -> List[Dict]:
        """Get all applications for a student"""
        try:
            response = self.supabase.table('applications').select('*, job_postings(*, companies(*))').eq('student_id', student_id).execute()
            return response.data
        except:
            return []
    
    # ============= COLLEGE OPERATIONS =============
    def create_college(self, college_data: Dict) -> Optional[Dict]:
        """Create a new college record"""
        try:
            response = self.supabase.table('colleges').insert(college_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Error creating college: {str(e)}")
            return None
    
    def get_all_colleges(self) -> List[Dict]:
        """Get all colleges"""
        try:
            response = self.supabase.table('colleges').select('*').execute()
            return response.data
        except:
            return []
    
    # ============= ANALYTICS/REPORTS =============
    def get_placement_stats(self) -> Dict:
        """Get placement statistics"""
        try:
            # Get total applications
            apps_response = self.supabase.table('applications').select('*').execute()
            total_applications = len(apps_response.data) if apps_response.data else 0
            
            # Get accepted applications
            accepted_response = self.supabase.table('applications').select('*').eq('status', 'accepted').execute()
            accepted_applications = len(accepted_response.data) if accepted_response.data else 0
            
            return {
                'total_applications': total_applications,
                'accepted_applications': accepted_applications,
                'success_rate': (accepted_applications / total_applications * 100) if total_applications > 0 else 0
            }
        except:
            return {'total_applications': 0, 'accepted_applications': 0, 'success_rate': 0}
