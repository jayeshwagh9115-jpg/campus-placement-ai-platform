import streamlit as st
from supabase import create_client
import requests
import json
from typing import Optional, List, Dict, Any
from datetime import datetime

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
    
    # ---------- GENERIC CRUD OPERATIONS ----------
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
    
    def upsert(self, table: str, data: Dict, on_conflict: str = 'id') -> Optional[Dict]:
        """Upsert data into table"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            response = self.client.table(table).upsert(data, on_conflict=on_conflict).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Upsert error in {table}: {e}")
            return None
    
    def select(self, table: str, filters: Dict = None, limit: int = None) -> List[Dict]:
        """Select data from table"""
        if not self.is_connected or not self.client:
            return []
        
        try:
            query = self.client.table(table).select("*")
            
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Select error from {table}: {e}")
            return []
    
    def select_all(self, table: str) -> List[Dict]:
        """Select all data from table"""
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
    
    def delete(self, table: str, id_value: str) -> bool:
        """Delete data from table"""
        if not self.is_connected or not self.client:
            return False
        
        try:
            response = self.client.table(table).delete().eq('id', id_value).execute()
            return True
        except Exception as e:
            print(f"Delete error in {table}: {e}")
            return False
    
    # ---------- STUDENT METHODS ----------
    def save_student_profile(self, student_data):
        """Save student profile to database"""
        print(f"🔍 DEBUG save_student_profile called with data keys: {list(student_data.keys())}")
    
        if not self.is_connected:
            print("❌ Not connected to database")
            return False
    
        try:
            # Ensure required fields
            required_fields = ['full_name', 'email', 'roll_number']
            for field in required_fields:
                if field not in student_data:
                    print(f"❌ Missing required field: {field}")
                    return False
        
            # Try multiple approaches
            print("💾 Attempt 1: Using upsert...")
            try:
                result = self.upsert('students', student_data, on_conflict='email')
                if result:
                    print(f"✅ Upsert successful: {result.get('id')}")
                    return True
            except Exception as e1:
                print(f"❌ Upsert failed: {e1}")
        
            print("💾 Attempt 2: Using insert...")
            try:
                result = self.insert('students', student_data)
                if result:
                    print(f"✅ Insert successful: {result.get('id')}")
                    return True
            except Exception as e2:
                print(f"❌ Insert failed: {e2}")
        
            print("💾 Attempt 3: Using client directly...")
            try:
                response = self.client.table('students').insert(student_data).execute()
                if response.data and len(response.data) > 0:
                    print(f"✅ Direct client insert successful: {response.data[0].get('id')}")
                    return True
            except Exception as e3:
                print(f"❌ Direct client insert failed: {e3}")
        
            print("❌ All save attempts failed")
            return False
        
        except Exception as e:
            print(f"❌ Exception in save_student_profile: {e}")
            import traceback
            print(f"❌ Traceback: {traceback.format_exc()}")
            return False
    
    def get_student_profile(self, email: str) -> Optional[Dict]:
        """Get student profile by email"""
        try:
            students = self.select('students', {'email': email}, limit=1)
            return students[0] if students else None
        except Exception as e:
            print(f"Error getting student profile: {e}")
            return None
    
    def get_student_by_email(self, email: str) -> Optional[Dict]:
        """Get student by email (alias for get_student_profile)"""
        return self.get_student_profile(email)
    
    def create_student(self, student_data: Dict) -> Optional[Dict]:
        """Create a new student"""
        return self.insert('students', student_data)
    
    def get_students(self, college_id: str = None) -> List[Dict]:
        """Get students"""
        if college_id:
            return self.select('students', {'college_id': college_id})
        return self.select_all('students')
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        return self.select_all('students')
    
    def get_student_count(self) -> int:
        """Get student count"""
        try:
            students = self.get_students()
            return len(students)
        except:
            return 0
    
    # ---------- STUDENT EDUCATION METHODS ----------
    def save_student_education(self, education_data: Dict) -> bool:
        """Save student education record"""
        try:
            result = self.insert('student_education', education_data)
            return result is not None
        except Exception as e:
            print(f"Error saving student education: {e}")
            return False
    
    def get_student_education(self, student_id: str) -> List[Dict]:
        """Get education records for a student"""
        return self.select('student_education', {'student_id': student_id})
    
    # ---------- STUDENT PROJECT METHODS ----------
    def save_student_project(self, project_data: Dict) -> bool:
        """Save student project"""
        try:
            result = self.insert('student_projects', project_data)
            return result is not None
        except Exception as e:
            print(f"Error saving student project: {e}")
            return False
    
    def get_student_projects(self, student_id: str) -> List[Dict]:
        """Get projects for a student"""
        return self.select('student_projects', {'student_id': student_id})
    
    # ---------- STUDENT INTERNSHIP METHODS ----------
    def save_student_internship(self, internship_data: Dict) -> bool:
        """Save student internship"""
        try:
            result = self.insert('student_internships', internship_data)
            return result is not None
        except Exception as e:
            print(f"Error saving student internship: {e}")
            return False
    
    def get_student_internships(self, student_id: str) -> List[Dict]:
        """Get internships for a student"""
        return self.select('student_internships', {'student_id': student_id})
    
    # ---------- STUDENT CERTIFICATION METHODS ----------
    def save_student_certification(self, certification_data: Dict) -> bool:
        """Save student certification"""
        try:
            result = self.insert('student_certifications', certification_data)
            return result is not None
        except Exception as e:
            print(f"Error saving student certification: {e}")
            return False
    
    def get_student_certifications(self, student_id: str) -> List[Dict]:
        """Get certifications for a student"""
        return self.select('student_certifications', {'student_id': student_id})
    
    # ---------- STUDENT APPLICATION METHODS ----------
    def get_student_applications(self, student_id: str) -> List[Dict]:
        """Get applications for a student"""
        return self.select('applications', {'student_id': student_id})
    
    # ---------- COLLEGE METHODS ----------
    def save_college_profile(self, college_data: Dict) -> bool:
        """Save college profile to database"""
        try:
            # Add timestamp if not present
            if 'created_at' not in college_data:
                college_data['created_at'] = datetime.now().isoformat()
            
            result = self.upsert('colleges', college_data)
            return result is not None
        except Exception as e:
            print(f"Error saving college profile: {e}")
            return False
    
    def get_college_profile(self, college_id: str) -> Optional[Dict]:
        """Get college profile by ID"""
        try:
            colleges = self.select('colleges', {'id': college_id}, limit=1)
            return colleges[0] if colleges else None
        except Exception as e:
            print(f"Error getting college profile: {e}")
            return None
    
    def get_colleges(self) -> List[Dict]:
        """Get all colleges"""
        return self.select_all('colleges')
    
    def get_college_students(self, college_id: str) -> List[Dict]:
        """Get students for a college"""
        return self.select('students', {'college_id': college_id})
    
    def bulk_save_students(self, college_id: str, students_data: List[Dict]) -> int:
        """Bulk save students for a college"""
        success_count = 0
        for student in students_data:
            student['college_id'] = college_id
            if self.insert('students', student):
                success_count += 1
        return success_count
    
    def save_student(self, student_data: Dict) -> bool:
        """Save individual student"""
        try:
            result = self.upsert('students', student_data)
            return result is not None
        except Exception as e:
            print(f"Error saving student: {e}")
            return False
    
    # ---------- JOB METHODS ----------
    def create_job(self, job_data: Dict) -> Optional[Dict]:
        """Create a new job posting"""
        return self.insert('job_postings', job_data)
    
    def get_jobs(self, company_id: str = None) -> List[Dict]:
        """Get jobs"""
        if company_id:
            return self.select('job_postings', {'company_id': company_id})
        return self.select_all('job_postings')
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all jobs"""
        return self.select_all('job_postings')
    
    # ---------- APPLICATION METHODS ----------
    def create_application(self, app_data: Dict) -> Optional[Dict]:
        """Create a new application"""
        return self.insert('applications', app_data)
    
    def get_applications(self, student_id: str = None, job_id: str = None) -> List[Dict]:
        """Get applications"""
        filters = {}
        if student_id:
            filters['student_id'] = student_id
        if job_id:
            filters['job_id'] = job_id
        return self.select('applications', filters if filters else None)
    
    def get_all_applications(self) -> List[Dict]:
        """Get all applications"""
        return self.select_all('applications')
    
    # ---------- COMPANY METHODS ----------
    def get_companies(self) -> List[Dict]:
        """Get all companies"""
        return self.select_all('companies')
    
    def save_company_profile(self, company_data: Dict) -> bool:
        """Save company profile to database"""
        try:
            result = self.upsert('companies', company_data)
            return result is not None
        except Exception as e:
            print(f"Error saving company profile: {e}")
            return False
    
    # ---------- DASHBOARD & STATISTICS ----------
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
    
    def get_placement_stats(self, college_id: str = None) -> Dict:
        """Get placement statistics"""
        stats = {
            'total_students': 0,
            'placed_students': 0,
            'placement_rate': 0,
            'avg_package': 0
        }
        
        try:
            students = self.get_students(college_id) if college_id else self.get_all_students()
            if students:
                stats['total_students'] = len(students)
                placed = [s for s in students if s.get('placement_status') == 'placed']
                stats['placed_students'] = len(placed)
                stats['placement_rate'] = (len(placed) / len(students)) * 100 if students else 0
                
                # Calculate average package
                packages = [float(s.get('package', 0)) for s in placed if s.get('package')]
                stats['avg_package'] = sum(packages) / len(packages) if packages else 0
        except Exception as e:
            print(f"Error getting placement stats: {e}")
        
        return stats
    
    # ---------- TEST & DEBUG METHODS ----------
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
    
    def get_table_schema(self, table_name: str) -> List[Dict]:
        """Get table schema information"""
        try:
            # This is a simplified approach - in production, you might need to query information_schema
            # For now, return sample data to infer schema
            sample = self.select(table_name, limit=1)
            if sample:
                return [{'column': key, 'type': type(value).__name__} for key, value in sample[0].items()]
            return []
        except Exception as e:
            print(f"Error getting schema for {table_name}: {e}")
            return []
    
    # ---------- DATA VALIDATION ----------
    def validate_student_data(self, student_data: Dict) -> Dict:
        """Validate student data before saving"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['full_name', 'email', 'roll_number', 'department']
        for field in required_fields:
            if not student_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Email validation
        email = student_data.get('email', '')
        if email and '@' not in email:
            warnings.append("Email format may be invalid")
        
        # CGPA validation
        cgpa = student_data.get('cgpa', 0)
        if cgpa < 0 or cgpa > 10:
            warnings.append("CGPA should be between 0 and 10")
        
        # Backlogs validation
        backlogs = student_data.get('backlogs', 0)
        if backlogs < 0:
            warnings.append("Backlogs cannot be negative")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
