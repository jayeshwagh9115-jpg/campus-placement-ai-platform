
import streamlit as st
from supabase import create_client
import requests
import json
from typing import Optional, List, Dict, Any
from datetime import datetime
import traceback

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
                print(f"⚠️ Connection test failed: {e}")
                print("🔧 Creating tables if they don't exist...")
                
                # Try to create tables automatically
                if self._create_tables_if_not_exist():
                    self.is_connected = True
                else:
                    # Try direct API as fallback
                    if self._test_direct_api():
                        self.is_connected = True
                    else:
                        self.is_connected = False
                
        except Exception as e:
            print(f"❌ Failed to create Supabase client: {e}")
            self.is_connected = False
    
    def _create_tables_if_not_exist(self):
        """Create tables if they don't exist"""
        try:
            # List of tables to check/create
            tables = ['students', 'colleges', 'companies', 'job_postings', 'applications']
            created_count = 0
            
            for table in tables:
                try:
                    # Try to select from table
                    response = self.client.table(table).select('id').limit(1).execute()
                    print(f"✅ Table '{table}' exists")
                except Exception as e:
                    if "not found" in str(e).lower() or "does not exist" in str(e).lower():
                        print(f"⚠️ Table '{table}' doesn't exist. Creating...")
                        # In Supabase, you typically create tables via SQL in the dashboard
                        # For now, just note which tables are missing
                        print(f"   Run SQL in Supabase dashboard to create '{table}' table")
                    else:
                        print(f"⚠️ Error checking table '{table}': {e}")
            
            return True
        except Exception as e:
            print(f"❌ Error in table creation check: {e}")
            return False
    
    def _test_direct_api(self):
        """Test connection using direct REST API"""
        try:
            headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            response = requests.get(
                f"{self.url}/rest/v1/",
                headers=headers
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
            print(f"❌ Cannot insert: Not connected to database")
            return None
        
        try:
            print(f"📝 Inserting into {table} with data keys: {list(data.keys())}")
            
            # Clean data - remove None values and convert to JSON serializable format
            clean_data = {}
            for key, value in data.items():
                if value is not None:
                    # Handle list types
                    if isinstance(value, list):
                        clean_data[key] = json.dumps(value) if value else []
                    else:
                        clean_data[key] = value
            
            response = self.client.table(table).insert(clean_data).execute()
            
            if response.data and len(response.data) > 0:
                print(f"✅ Successfully inserted into {table}, ID: {response.data[0].get('id')}")
                return response.data[0]
            else:
                print(f"⚠️ No data returned from insert into {table}")
                return None
                
        except Exception as e:
            print(f"❌ Insert error in {table}: {e}")
            print(f"📋 Data attempted: {json.dumps(data, default=str)}")
            
            # More detailed error information
            if hasattr(e, 'message'):
                print(f"🔧 Error details: {e.message}")
            
            return None
    
    def upsert(self, table: str, data: Dict, on_conflict: str = 'id') -> Optional[Dict]:
        """Upsert data into table"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            # Clean data
            clean_data = {}
            for key, value in data.items():
                if value is not None:
                    if isinstance(value, list):
                        clean_data[key] = json.dumps(value) if value else []
                    else:
                        clean_data[key] = value
            
            response = self.client.table(table).upsert(clean_data, on_conflict=on_conflict).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Upsert error in {table}: {e}")
            print(f"📋 Data attempted: {json.dumps(data, default=str)}")
            return None
    
    def select(self, table: str, filters: Dict = None, limit: int = None, columns: str = "*") -> List[Dict]:
        """Select data from table"""
        if not self.is_connected or not self.client:
            return []
        
        try:
            query = self.client.table(table).select(columns)
            
            if filters:
                for key, value in filters.items():
                    if value is not None:
                        query = query.eq(key, value)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            
            # Parse JSON strings back to lists if needed
            if response.data:
                parsed_data = []
                for item in response.data:
                    parsed_item = {}
                    for key, value in item.items():
                        if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                            try:
                                parsed_item[key] = json.loads(value)
                            except:
                                parsed_item[key] = value
                        else:
                            parsed_item[key] = value
                    parsed_data.append(parsed_item)
                
                return parsed_data
            return []
            
        except Exception as e:
            print(f"❌ Select error from {table}: {e}")
            return []
    
    def select_all(self, table: str) -> List[Dict]:
        """Select all data from table"""
        return self.select(table)
    
    def update(self, table: str, id_value: str, updates: Dict) -> Optional[Dict]:
        """Update data in table"""
        if not self.is_connected or not self.client:
            return None
        
        try:
            # Clean update data
            clean_updates = {}
            for key, value in updates.items():
                if value is not None:
                    if isinstance(value, list):
                        clean_updates[key] = json.dumps(value) if value else []
                    else:
                        clean_updates[key] = value
            
            response = self.client.table(table).update(clean_updates).eq('id', id_value).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Update error in {table}: {e}")
            return None
    
    def delete(self, table: str, id_value: str) -> bool:
        """Delete data from table"""
        if not self.is_connected or not self.client:
            return False
        
        try:
            response = self.client.table(table).delete().eq('id', id_value).execute()
            return True
        except Exception as e:
            print(f"❌ Delete error in {table}: {e}")
            return False
    
    # ---------- USER MANAGEMENT METHODS ----------
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user account in the database"""
        print(f"🔍 DEBUG create_user called with data keys: {list(user_data.keys())}")
        
        if not self.is_connected:
            print("❌ Not connected to database")
            return {"success": False, "error": "Not connected to database", "id": None}
        
        try:
            # First check if user already exists
            email = user_data.get('email')
            if email:
                existing_user = self.get_user_by_email(email)
                if existing_user:
                    print(f"⚠️ User with email '{email}' already exists")
                    return {
                        "success": False, 
                        "error": f"User with email '{email}' already exists", 
                        "id": existing_user.get('id')
                    }
            
            # Add timestamp
            if 'created_at' not in user_data:
                user_data['created_at'] = datetime.now().isoformat()
            
            # Check if we're inserting into 'users' or 'students' table
            # Determine table based on available data
            if 'role' in user_data and user_data['role'] == 'student':
                # Save to students table
                print("💾 Saving as student...")
                result = self.save_student_profile(user_data)
                return result
            else:
                # Try to insert into 'users' table
                print("💾 Attempting to insert into users table...")
                try:
                    result = self.insert('users', user_data)
                    if result:
                        user_id = result.get('id')
                        print(f"✅ User created successfully: {user_id}")
                        return {"success": True, "id": user_id, "data": result}
                except Exception as e:
                    print(f"⚠️ Failed to insert into users table: {e}")
                    
                    # Fallback: Try students table if 'users' table doesn't exist
                    print("💾 Falling back to students table...")
                    try:
                        result = self.save_student_profile(user_data)
                        return result
                    except Exception as e2:
                        print(f"⚠️ Failed to save to students table: {e2}")
            
            print("❌ All create user attempts failed")
            return {"success": False, "error": "Failed to create user account", "id": None}
        
        except Exception as e:
            error_msg = f"Exception in create_user: {e}"
            print(f"❌ {error_msg}")
            print(f"❌ Traceback: {traceback.format_exc()}")
            return {"success": False, "error": error_msg, "id": None}
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email from database"""
        try:
            # First try 'users' table
            try:
                users = self.select('users', {'email': email}, limit=1)
                if users:
                    return users[0]
            except:
                pass
            
            # If not found, try 'students' table
            students = self.select('students', {'email': email}, limit=1)
            if students:
                return students[0]
            
            # Try 'companies' table
            companies = self.select('companies', {'company_email': email}, limit=1)
            if companies:
                return companies[0]
            
            return None
        except Exception as e:
            print(f"Error getting user by email: {e}")
            return None
    
    # ---------- TABLE VALIDATION METHODS ----------
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get column names for a table"""
        try:
            # Get one record to infer columns
            sample = self.select(table_name, limit=1)
            if sample and len(sample) > 0:
                return list(sample[0].keys())
            else:
                # Try to get schema via information_schema (limited in Supabase)
                print(f"⚠️ No data in {table_name} to infer columns")
                return []
        except Exception as e:
            print(f"❌ Error getting columns for {table_name}: {e}")
            return []
    
    def validate_data_against_table(self, table_name: str, data: Dict) -> Dict:
        """Validate data against table structure"""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'extra_fields': [],
            'missing_fields': []
        }
        
        # Get actual columns from table
        actual_columns = self.get_table_columns(table_name)
        
        if not actual_columns:
            validation_result['warnings'].append(f"Cannot validate: Could not get columns for {table_name}")
            return validation_result
        
        # Check for extra fields in data that don't exist in table
        data_fields = list(data.keys())
        for field in data_fields:
            if field not in actual_columns:
                validation_result['extra_fields'].append(field)
                validation_result['warnings'].append(f"Field '{field}' not found in table '{table_name}'")
        
        # Check required fields (basic check)
        required_fields = self._get_required_fields(table_name)
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == '':
                validation_result['missing_fields'].append(field)
                validation_result['errors'].append(f"Required field '{field}' is missing")
        
        validation_result['valid'] = len(validation_result['errors']) == 0
        return validation_result
    
    def _get_required_fields(self, table_name: str) -> List[str]:
        """Get required fields for a table (simplified)"""
        required_fields_map = {
            'students': ['full_name', 'email', 'roll_number'],
            'colleges': ['college_name', 'college_code'],
            'companies': ['company_name', 'company_email'],
            'job_postings': ['job_title', 'company_id'],
            'applications': ['student_id', 'job_id'],
            'users': ['email', 'full_name']  # Added users table
        }
        return required_fields_map.get(table_name, [])
    
    # ---------- ENHANCED STUDENT METHODS ----------
    def save_student_profile(self, student_data):
        """Save student profile to database with better error handling"""
        print(f"🔍 DEBUG save_student_profile called with data keys: {list(student_data.keys())}")
    
        if not self.is_connected:
            print("❌ Not connected to database")
            return {"success": False, "error": "Not connected to database", "id": None}
    
        try:
            # Validate against table structure first
            validation = self.validate_data_against_table('students', student_data)
            if not validation['valid']:
                print(f"❌ Validation failed: {validation['errors']}")
                return {"success": False, "error": f"Validation failed: {validation['errors']}", "id": None}
            
            # Ensure required fields
            required_fields = ['full_name', 'email', 'roll_number']
            for field in required_fields:
                if field not in student_data:
                    print(f"❌ Missing required field: {field}")
                    return {"success": False, "error": f"Missing required field: {field}", "id": None}
            
            # Add timestamp if not present
            if 'created_at' not in student_data:
                student_data['created_at'] = datetime.now().isoformat()
            
            # Try upsert first (handles both insert and update)
            print("💾 Attempting upsert...")
            try:
                result = self.upsert('students', student_data, on_conflict='email,roll_number')
                if result:
                    student_id = result.get('id')
                    print(f"✅ Upsert successful: {student_id}")
                    return {"success": True, "id": student_id, "data": result}
            except Exception as e1:
                print(f"⚠️ Upsert failed: {e1}")
            
            # If upsert fails, try insert
            print("💾 Attempting insert...")
            try:
                result = self.insert('students', student_data)
                if result:
                    student_id = result.get('id')
                    print(f"✅ Insert successful: {student_id}")
                    return {"success": True, "id": student_id, "data": result}
            except Exception as e2:
                print(f"⚠️ Insert failed: {e2}")
            
            # Try with direct API as last resort
            print("💾 Attempting direct API...")
            try:
                headers = {
                    "apikey": self.key,
                    "Authorization": f"Bearer {self.key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                }
                
                response = requests.post(
                    f"{self.url}/rest/v1/students",
                    json=student_data,
                    headers=headers
                )
                
                if response.status_code in [200, 201]:
                    result = response.json()
                    if result and len(result) > 0:
                        student_id = result[0].get('id')
                        print(f"✅ Direct API successful: {student_id}")
                        return {"success": True, "id": student_id, "data": result[0]}
                else:
                    print(f"❌ Direct API failed: {response.status_code} - {response.text[:200]}")
                    
            except Exception as e3:
                print(f"❌ Direct API failed: {e3}")
            
            print("❌ All save attempts failed")
            return {"success": False, "error": "All save attempts failed", "id": None}
        
        except Exception as e:
            error_msg = f"Exception in save_student_profile: {e}"
            print(f"❌ {error_msg}")
            print(f"❌ Traceback: {traceback.format_exc()}")
            return {"success": False, "error": error_msg, "id": None}
    
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
    
    def create_student(self, student_data: Dict) -> Dict:
        """Create a new student (wrapper for save_student_profile)"""
        return self.save_student_profile(student_data)
    
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
            # Use count() for better performance
            response = self.client.table('students').select('id', count='exact').execute()
            return response.count if hasattr(response, 'count') else 0
        except:
            try:
                students = self.get_students()
                return len(students)
            except:
                return 0
    
    # ---------- ENHANCED COLLEGE METHODS ----------
    def save_college_profile(self, college_data: Dict) -> Dict:
        """Save college profile to database with better error handling"""
        try:
            # Validate against table structure
            validation = self.validate_data_against_table('colleges', college_data)
            if not validation['valid']:
                return {"success": False, "error": f"Validation failed: {validation['errors']}", "id": None}
            
            # Add timestamp if not present
            if 'created_at' not in college_data:
                college_data['created_at'] = datetime.now().isoformat()
            
            result = self.upsert('colleges', college_data, on_conflict='college_code')
            if result:
                return {"success": True, "id": result.get('id'), "data": result}
            else:
                # Try insert as fallback
                result = self.insert('colleges', college_data)
                if result:
                    return {"success": True, "id": result.get('id'), "data": result}
                else:
                    return {"success": False, "error": "Failed to save college profile", "id": None}
                    
        except Exception as e:
            print(f"Error saving college profile: {e}")
            return {"success": False, "error": str(e), "id": None}
    
    # ---------- ENHANCED COMPANY METHODS ----------
    def save_company_profile(self, company_data: Dict) -> Dict:
        """Save company profile to database with better error handling"""
        try:
            # Validate against table structure
            validation = self.validate_data_against_table('companies', company_data)
            if not validation['valid']:
                return {"success": False, "error": f"Validation failed: {validation['errors']}", "id": None}
            
            result = self.upsert('companies', company_data, on_conflict='company_email')
            if result:
                return {"success": True, "id": result.get('id'), "data": result}
            else:
                # Try insert as fallback
                result = self.insert('companies', company_data)
                if result:
                    return {"success": True, "id": result.get('id'), "data": result}
                else:
                    return {"success": False, "error": "Failed to save company profile", "id": None}
                    
        except Exception as e:
            print(f"Error saving company profile: {e}")
            return {"success": False, "error": str(e), "id": None}
    
    # ---------- ENHANCED JOB METHODS ----------
    def create_job(self, job_data: Dict) -> Dict:
        """Create a new job posting with validation"""
        try:
            # Validate against table structure
            validation = self.validate_data_against_table('job_postings', job_data)
            if not validation['valid']:
                return {"success": False, "error": f"Validation failed: {validation['errors']}", "id": None}
            
            result = self.insert('job_postings', job_data)
            if result:
                return {"success": True, "id": result.get('id'), "data": result}
            else:
                return {"success": False, "error": "Failed to create job posting", "id": None}
        except Exception as e:
            print(f"Error creating job: {e}")
            return {"success": False, "error": str(e), "id": None}
    
    # ---------- ENHANCED APPLICATION METHODS ----------
    def create_application(self, app_data: Dict) -> Dict:
        """Create a new application with validation"""
        try:
            # Validate against table structure
            validation = self.validate_data_against_table('applications', app_data)
            if not validation['valid']:
                return {"success": False, "error": f"Validation failed: {validation['errors']}", "id": None}
            
            # Add timestamp if not present
            if 'applied_date' not in app_data:
                app_data['applied_date'] = datetime.now().isoformat()
            
            result = self.insert('applications', app_data)
            if result:
                return {"success": True, "id": result.get('id'), "data": result}
            else:
                return {"success": False, "error": "Failed to create application", "id": None}
        except Exception as e:
            print(f"Error creating application: {e}")
            return {"success": False, "error": str(e), "id": None}
    
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
            # Get counts with error handling for each
            try:
                stats['total_students'] = self.get_student_count()
            except:
                pass
            
            try:
                stats['total_companies'] = len(self.get_companies())
            except:
                pass
            
            try:
                stats['active_jobs'] = len(self.select('job_postings', {'status': 'open'}))
            except:
                pass
            
            try:
                stats['total_applications'] = len(self.get_all_applications())
            except:
                pass
                
        except Exception as e:
            print(f"Error getting stats: {e}")
        
        return stats
    
    # ---------- HELPER METHODS ----------
    def get_companies(self) -> List[Dict]:
        """Get all companies"""
        return self.select_all('companies')
    
    def get_all_applications(self) -> List[Dict]:
        """Get all applications"""
        return self.select_all('applications')
    
    # ---------- TEST & DEBUG METHODS ----------
    def test_connection(self) -> Dict:
        """Test all connections and return status"""
        status = {
            'connected': self.is_connected,
            'tables': {},
            'sample_data': {},
            'table_columns': {}
        }
        
        if not self.is_connected:
            return status
        
        # Test each table
        tables = ['students', 'companies', 'job_postings', 'applications', 'colleges', 'users']
        
        for table in tables:
            try:
                # Get table columns
                columns = self.get_table_columns(table)
                status['table_columns'][table] = columns
                
                # Try to select data
                data = self.select(table, limit=1)
                status['tables'][table] = {
                    'accessible': True,
                    'count': len(self.select_all(table)),
                    'columns': columns
                }
                
                if data and len(data) > 0:
                    status['sample_data'][table] = data[0]
                    
            except Exception as e:
                status['tables'][table] = {
                    'accessible': False,
                    'error': str(e),
                    'columns': []
                }
        
        return status
    
    def get_table_info(self, table_name: str) -> Dict:
        """Get detailed information about a table"""
        info = {
            'exists': False,
            'columns': [],
            'row_count': 0,
            'sample_row': None
        }
        
        try:
            # Check if table exists by trying to select
            sample = self.select(table_name, limit=1)
            if sample is not None:
                info['exists'] = True
                info['columns'] = self.get_table_columns(table_name)
                info['row_count'] = len(self.select_all(table_name))
                if sample and len(sample) > 0:
                    info['sample_row'] = sample[0]
        except Exception as e:
            info['error'] = str(e)
        
        return info
    
    # ---------- BULK OPERATIONS ----------
    def bulk_insert(self, table: str, data_list: List[Dict]) -> Dict:
        """Insert multiple records at once"""
        result = {
            'success': False,
            'inserted_count': 0,
            'errors': []
        }
        
        if not self.is_connected:
            result['errors'].append("Not connected to database")
            return result
        
        try:
            # Clean each record
            clean_data_list = []
            for data in data_list:
                clean_data = {}
                for key, value in data.items():
                    if value is not None:
                        if isinstance(value, list):
                            clean_data[key] = json.dumps(value) if value else []
                        else:
                            clean_data[key] = value
                clean_data_list.append(clean_data)
            
            response = self.client.table(table).insert(clean_data_list).execute()
            
            if response.data:
                result['success'] = True
                result['inserted_count'] = len(response.data)
            else:
                result['errors'].append("No data returned from bulk insert")
                
        except Exception as e:
            result['errors'].append(f"Bulk insert error: {e}")
        
        return result
    
    # ---------- DATA VALIDATION ----------
    def validate_student_data(self, student_data: Dict) -> Dict:
        """Validate student data before saving"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['full_name', 'email', 'roll_number']
        for field in required_fields:
            if not student_data.get(field):
                errors.append(f"Missing required field: {field}")
        
        # Email validation
        email = student_data.get('email', '')
        if email and '@' not in email:
            warnings.append("Email format may be invalid")
        
        # Check if email already exists
        try:
            existing = self.get_student_by_email(email)
            if existing:
                warnings.append(f"Email '{email}' already registered")
        except:
            pass
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def get_database_status(self) -> str:
        """Get database connection status as a string"""
        if not self.is_connected:
            return "❌ Not Connected"
        
        try:
            # Try a simple query
            self.client.table('students').select('count', count='exact').execute()
            return "✅ Connected and Active"
        except Exception as e:
            return f"⚠️ Connected but error: {str(e)[:50]}"
[file content end]
