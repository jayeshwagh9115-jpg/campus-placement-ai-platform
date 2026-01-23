import streamlit as st
from supabase import create_client
import requests
import json
from typing import Optional, List, Dict, Any

class SupabaseManager:
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.url = None
        self.key = None
        
        # Your credentials
        self.url = "https://ptnozudvgcqhnmidjoqj.supabase.co"
        self.key = "sb_publishable_WRZY__f0rKmSL0r5KCmZqA_yWf64uW0"
        
        print(f"🔗 Connecting to: {self.url}")
        
        if not self.url or not self.key:
            print("❌ Missing Supabase credentials")
            return
        
        try:
            # Create client
            self.client = create_client(self.url, self.key)
            
            # Test connection with a simple query
            try:
                response = self.client.table('students').select('id').limit(1).execute()
                print(f"✅ Connected! Found {len(response.data) if response.data else 0} students")
                self.is_connected = True
            except Exception as e:
                print(f"❌ Connection test failed: {e}")
                # Try direct API as fallback
                if self._test_direct_api():
                    self.is_connected = True
                else:
                    self.is_connected = False
                
        except Exception as e:
            print(f"❌ Failed to create Supabase client: {e}")
            self.is_connected = False
    
    def _test_direct_api(self):
        """Test connection using direct REST API"""
        try:
            headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.url}/rest/v1/students",
                headers=headers,
                params={"select": "*", "limit": "1"}
            )
            
            if response.status_code in [200, 201, 204]:
                print(f"✅ Direct API test successful")
                return True
            else:
                print(f"❌ API returned {response.status_code}: {response.text[:100]}")
                return False
                
        except Exception as e:
            print(f"❌ Direct API test failed: {e}")
            return False
    
    # ---------- CRUD OPERATIONS ----------
    def insert(self, table: str, data: Dict) -> Optional[Dict]:
        """Insert data into table"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Insert error in {table}: {e}")
            return None
    
    def select(self, table: str, filters: Dict = None) -> List[Dict]:
        """Select data from table"""
        if not self.is_connected or not self.client:
            return []
        
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Select error from {table}: {e}")
            return []
    
    def select_all(self, table: str) -> List[Dict]:
        """Select all data from table (simple version)"""
        return self.select(table)
    
    def update(self, table: str, id_value: str, updates: Dict) -> Optional[Dict]:
        """Update data in table"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            response = self.client.table(table).update(updates).eq('id', id_value).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Update error in {table}: {e}")
            return None
    
    # ---------- APP-SPECIFIC METHODS (FIXED SIGNATURES) ----------
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        """Create a new student - FIXED"""
        return self.insert('students', student_data)
    
    def get_students(self, college_id: str = None) -> List[Dict]:
        """Get students - FIXED (removed 'limit' parameter)"""
        if college_id:
            return self.select('students', {'college_id': college_id})
        return self.select('students')
    
    def get_all_students(self) -> List[Dict]:
        """Get all students - simple version"""
        return self.select_all('students')
    
    def get_student_count(self) -> int:
        """Get student count"""
        try:
            students = self.get_students()
            return len(students)
        except:
            return 0
    
    def create_job(self, job_data: Dict) -> Optional[Dict]:
        """Create a new job posting"""
        return self.insert('job_postings', job_data)
    
    def get_jobs(self, company_id: str = None) -> List[Dict]:
        """Get jobs - FIXED"""
        if company_id:
            return self.select('job_postings', {'company_id': company_id})
        return self.select('job_postings')
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs"""
        return self.select_all('job_postings')
    
    def create_application(self, app_data: Dict) -> Optional[Dict]:
        """Create a new application"""
        return self.insert('applications', app_data)
    
    def get_applications(self, student_id: str = None, job_id: str = None) -> List[Dict]:
        """Get applications - FIXED"""
        filters = {}
        if student_id:
            filters['student_id'] = student_id
        if job_id:
            filters['job_id'] = job_id
        return self.select('applications', filters if filters else None)
    
    def get_all_applications(self) -> List[Dict]:
        """Get all applications"""
        return self.select_all('applications')
    
    def get_companies(self) -> List[Dict]:
        """Get all companies"""
        return self.select_all('companies')
    
    def get_colleges(self) -> List[Dict]:
        """Get all colleges"""
        return self.select_all('colleges')
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        stats = {
            'total_students': 0,
            'active_jobs': 0,
            'total_companies': 0,
            'total_applications': 0
        }
        
        if not self.is_connected:
            return stats
        
        try:
            # Get counts
            stats['total_students'] = self.get_student_count()
            stats['total_companies'] = len(self.get_companies())
            stats['active_jobs'] = len(self.select('job_postings', {'status': 'open'}))
            stats['total_applications'] = len(self.get_all_applications())
        except Exception as e:
            print(f"Error getting stats: {e}")
        
        return stats
    
    def test_connection(self) -> Dict:
        """Test all connections and return status"""
        status = {
            'connected': self.is_connected,
            'tables': {},
            'sample_data': {}
        }
        
        if not self.is_connected:
            return status
        
        # Test each table
        tables = ['students', 'companies', 'job_postings', 'applications', 'colleges']
        
        for table in tables:
            try:
                data = self.select(table, {})
                status['tables'][table] = {
                    'accessible': True,
                    'count': len(data)
                }
                if data and len(data) > 0:
                    status['sample_data'][table] = data[0]
            except Exception as e:
                status['tables'][table] = {
                    'accessible': False,
                    'error': str(e)
                }
        
        return status
