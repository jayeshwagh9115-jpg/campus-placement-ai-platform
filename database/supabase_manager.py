import os
from supabase import create_client, Client
import streamlit as st
from typing import Optional, List, Dict, Any

class SupabaseManager:
    def __init__(self):
        # Try to get from environment variables or Streamlit secrets
        try:
            # For Streamlit Cloud
            self.url = st.secrets["SUPABASE_URL"]
            self.key = st.secrets["SUPABASE_KEY"]
        except:
            # For local development
            self.url = os.getenv("SUPABASE_URL", "")
            self.key = os.getenv("SUPABASE_KEY", "")
        
        self.client = None
        self.is_connected = False
        
        try:
            if self.url and self.key:
                self.client: Client = create_client(self.url, self.key)
                # Test connection with a simple query
                try:
                    self.client.table('students').select('count', count='exact').limit(1).execute()
                    self.is_connected = True
                    st.success("✅ Connected to Supabase Database")
                except Exception as e:
                    st.warning(f"⚠️ Database connection issue: {e}")
                    self.is_connected = False
            else:
                st.warning("⚠️ Supabase credentials not found - Running in demo mode")
                self.is_connected = False
        except Exception as e:
            st.error(f"❌ Supabase initialization error: {e}")
            self.is_connected = False
    
    def insert(self, table: str, data: dict) -> Optional[Dict]:
        """Insert data into a table"""
        if not self.is_connected:
            return None
        
        try:
            # Clean data - remove None values
            clean_data = {k: v for k, v in data.items() if v is not None}
            
            response = self.client.table(table).insert(clean_data).execute()
            if hasattr(response, 'data') and response.data:
                return response.data[0] if response.data else None
            return None
        except Exception as e:
            st.error(f"❌ Insert error for table '{table}': {e}")
            return None
    
    def select(self, table: str, where: str = None, limit: int = None) -> List[Dict]:
        """Select data from a table"""
        if not self.is_connected:
            return []
        
        try:
            query = self.client.table(table).select("*")
            
            if where:
                # Handle where clause like "email='test@test.com'"
                if '=' in where:
                    parts = where.split('=')
                    if len(parts) == 2:
                        column = parts[0].strip()
                        value = parts[1].strip().strip("'").strip('"')
                        query = query.eq(column, value)
            
            if limit:
                query = query.limit(limit)
            
            response = query.execute()
            return response.data if hasattr(response, 'data') else []
        except Exception as e:
            st.error(f"❌ Select error for table '{table}': {e}")
            return []
    
    def update(self, table: str, data: dict, where: str) -> Optional[Dict]:
        """Update data in a table"""
        if not self.is_connected:
            return None
        
        try:
            # Clean data - remove None values
            clean_data = {k: v for k, v in data.items() if v is not None}
            
            if '=' in where:
                parts = where.split('=')
                if len(parts) == 2:
                    column = parts[0].strip()
                    value = parts[1].strip().strip("'").strip('"')
                    response = self.client.table(table).update(clean_data).eq(column, value).execute()
                    return response.data[0] if response.data else None
            return None
        except Exception as e:
            st.error(f"❌ Update error for table '{table}': {e}")
            return None
    
    def delete(self, table: str, where: str) -> bool:
        """Delete data from a table"""
        if not self.is_connected:
            return False
        
        try:
            if '=' in where:
                parts = where.split('=')
                if len(parts) == 2:
                    column = parts[0].strip()
                    value = parts[1].strip().strip("'").strip('"')
                    self.client.table(table).delete().eq(column, value).execute()
                    return True
            return False
        except Exception as e:
            st.error(f"❌ Delete error for table '{table}': {e}")
            return False
    
    def get_student_by_email(self, email: str) -> Optional[Dict]:
        """Get student by email"""
        results = self.select('students', where=f"email='{email}'", limit=1)
        return results[0] if results else None
    
    def get_student_by_roll_number(self, roll_number: str) -> Optional[Dict]:
        """Get student by roll number"""
        results = self.select('students', where=f"roll_number='{roll_number}'", limit=1)
        return results[0] if results else None
    
    def save_student_profile(self, profile_data: dict) -> bool:
        """Save or update student profile - SIMPLIFIED VERSION"""
        if not self.is_connected:
            return False
        
        try:
            # Extract essential fields
            email = profile_data.get('email', '')
            roll_number = profile_data.get('roll_number', '')
            
            if not email or not roll_number:
                st.error("❌ Email and roll number are required")
                return False
            
            # Prepare simplified data for database
            db_data = {
                'full_name': profile_data.get('full_name'),
                'email': email,
                'phone': profile_data.get('phone'),
                'roll_number': roll_number,
                'college_id': profile_data.get('college_id'),
                'department': profile_data.get('department'),
                'year': profile_data.get('year'),
                'semester': profile_data.get('semester'),
                'cgpa': float(profile_data.get('cgpa', 0.0)) if profile_data.get('cgpa') else 0.0,
                'backlogs': int(profile_data.get('backlogs', 0)),
                'skills': profile_data.get('technical_skills', []),  # Map technical_skills to skills
                'linkedin_profile': profile_data.get('linkedin_profile'),
                'github_profile': profile_data.get('github_profile'),
                'portfolio_link': profile_data.get('portfolio_link'),
                'profile_picture_url': profile_data.get('profile_picture_url')
            }
            
            # Check if student already exists
            existing = self.get_student_by_email(email)
            if not existing:
                existing = self.get_student_by_roll_number(roll_number)
            
            if existing:
                # Update existing
                student_id = existing.get('id')
                if student_id:
                    result = self.update('students', db_data, where=f"id='{student_id}'")
                    if result:
                        st.success(f"✅ Updated profile for {db_data['full_name']}")
                        return True
            else:
                # Insert new
                result = self.insert('students', db_data)
                if result:
                    st.success(f"✅ Created profile for {db_data['full_name']}")
                    return True
            
            return False
                
        except Exception as e:
            st.error(f"❌ Error saving student profile: {e}")
            return False
    
    def get_student_profile(self, email: str) -> Optional[Dict]:
        """Get student profile by email"""
        return self.get_student_by_email(email)
    
    def validate_student_data(self, data: dict) -> Dict[str, Any]:
        """Validate student data before saving"""
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['full_name', 'email', 'roll_number', 'department']
        for field in required_fields:
            if not data.get(field):
                errors.append(f"{field} is required")
        
        # Email validation
        email = data.get('email', '')
        if email and '@' not in email:
            errors.append("Invalid email format")
        
        # CGPA validation
        cgpa = data.get('cgpa', 0)
        if cgpa < 0 or cgpa > 10:
            errors.append("CGPA must be between 0 and 10")
        
        # Semester validation
        semester = data.get('semester', 0)
        if semester < 1 or semester > 12:
            warnings.append("Semester should be between 1 and 12")
        
        # Warnings
        if not data.get('technical_skills'):
            warnings.append("No technical skills specified")
        
        if not data.get('career_interests'):
            warnings.append("No career interests specified")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def get_dashboard_stats(self) -> Dict[str, int]:
        """Get dashboard statistics"""
        if not self.is_connected:
            # Return demo stats
            return {
                "total_students": 1250,
                "total_companies": 32,
                "active_jobs": 45,
                "total_applications": 320
            }
        
        try:
            # Get counts from database
            students = self.select('students', limit=1000)
            companies = self.select('companies', limit=1000) if hasattr(self, 'select') else []
            jobs = self.select('job_postings', limit=1000) if hasattr(self, 'select') else []
            applications = self.select('applications', limit=1000) if hasattr(self, 'select') else []
            
            return {
                "total_students": len(students),
                "total_companies": len(companies),
                "active_jobs": len(jobs),
                "total_applications": len(applications)
            }
        except Exception as e:
            st.error(f"❌ Error getting stats: {e}")
            # Return demo stats on error
            return {
                "total_students": 1250,
                "total_companies": 32,
                "active_jobs": 45,
                "total_applications": 320
            }
