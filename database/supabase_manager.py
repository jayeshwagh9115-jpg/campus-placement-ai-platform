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
        
        # Try multiple ways to get credentials
        self.url = "https://ptnozudvgcqhnmidjoqj.supabase.co"
        self.key = "sb_publishable_WRZY__f0rKmSL0r5KCmZqA_yWf64uW0"
        
        # If empty, try other sources
        if not self.url or not self.key:
            try:
                self.url = st.secrets.get("SUPABASE_URL", "")
                self.key = st.secrets.get("SUPABASE_KEY", "")
            except:
                pass
        
        print(f"🔗 Using URL: {self.url}")
        print(f"🔑 Using Key: {self.key[:15]}...")
        
        if not self.url or not self.key:
            print("❌ Missing Supabase credentials")
            return
        
        try:
            # Create client
            self.client = create_client(self.url, self.key)
            
            # Test connection with a safer method
            try:
                # Method 1: Try to get server version
                test_response = self.client.from_('').select('*').limit(0).execute()
                print("✅ Connection test passed")
                self.is_connected = True
            except Exception as test_error:
                # Method 2: Try direct REST API
                print(f"Client test error: {test_error}")
                self._test_direct_api()
                
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
            
            # Try to access a table
            response = requests.get(
                f"{self.url}/rest/v1/students",
                headers=headers,
                params={"select": "count", "limit": "1"}
            )
            
            if response.status_code in [200, 201, 204]:
                self.is_connected = True
                print(f"✅ Direct API connection successful")
            else:
                print(f"❌ API returned status {response.status_code}: {response.text[:100]}")
                self.is_connected = False
                
        except Exception as e:
            print(f"❌ Direct API test failed: {e}")
            self.is_connected = False
    
    # ---------- SAFE OPERATIONS WITH FALLBACK ----------
    def safe_execute(self, operation, *args, **kwargs):
        """Safely execute a database operation with error handling"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            return operation(*args, **kwargs)
        except Exception as e:
            st.error(f"Database operation failed: {e}")
            return None
    
    # ---------- CRUD OPERATIONS ----------
    def insert(self, table: str, data: Dict) -> Optional[Dict]:
        """Insert data into table"""
        if not self.is_connected:
            return None
        
        try:
            response = self.client.table(table).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            # Try direct API as fallback
            try:
                headers = {
                    "apikey": self.key,
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
                
                response = requests.post(
                    f"{self.url}/rest/v1/{table}",
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 201:
                    return response.json()[0] if response.json() else None
            except:
                pass
            
            st.error(f"Insert to {table} failed: {e}")
            return None
    
    def select(self, table: str, filters: Dict = None, limit: int = 100) -> List[Dict]:
        """Select data from table"""
        if not self.is_connected:
            return []
        
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            query = query.limit(limit)
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Select from {table} failed: {e}")
            return []
    
    def update(self, table: str, id_value: str, updates: Dict) -> Optional[Dict]:
        """Update data in table"""
        if not self.is_connected:
            return None
        
        try:
            response = self.client.table(table).update(updates).eq('id', id_value).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            st.error(f"Update in {table} failed: {e}")
            return None
    
    # ---------- APP-SPECIFIC METHODS ----------
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        return self.insert('students', student_data)
    
    def get_students(self, college_id: str = None) -> List[Dict]:
        if college_id:
            return self.select('students', {'college_id': college_id})
        return self.select('students')
    
    def get_student_count(self) -> int:
        try:
            response = self.client.table('students').select('*', count='exact').execute()
            return response.count if hasattr(response, 'count') else 0
        except:
            return len(self.get_students())
    
    def create_job(self, job_data: Dict) -> Optional[Dict]:
        return self.insert('job_postings', job_data)
    
    def get_jobs(self) -> List[Dict]:
        return self.select('job_postings')
    
    def create_application(self, app_data: Dict) -> Optional[Dict]:
        return self.insert('applications', app_data)
    
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
            stats['total_companies'] = len(self.select('companies'))
            stats['active_jobs'] = len(self.select('job_postings', {'status': 'open'}))
            stats['total_applications'] = len(self.select('applications'))
        except Exception as e:
            st.error(f"Error getting stats: {e}")
        
        return stats
