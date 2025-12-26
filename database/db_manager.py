import sqlite3
import json
import pandas as pd
from datetime import datetime
from contextlib import contextmanager
import hashlib
from typing import Optional, List, Dict, Any
import os

class DatabaseManager:
    def __init__(self, db_path='campus_placement.db'):
        self.db_path = db_path
        # Use a simpler initialization approach
        self._init_simple()
    
    def _init_simple(self):
        """Simple initialization that always works"""
        try:
            # First, delete the problematic database file if it exists
            if os.path.exists(self.db_path):
                try:
                    os.remove(self.db_path)
                    print(f"Removed existing database file: {self.db_path}")
                except:
                    print(f"Could not remove {self.db_path}, will try to overwrite")
            
            # Create a new simple database
            conn = sqlite3.connect(self.db_path)
            
            # Create only the most essential tables
            conn.execute("""
                CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active INTEGER DEFAULT 1
                )
            """)
            
            conn.execute("""
                CREATE TABLE students (
                    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER UNIQUE,
                    roll_number TEXT,
                    department TEXT,
                    semester INTEGER,
                    cgpa REAL,
                    graduation_year INTEGER,
                    placement_status TEXT DEFAULT 'Not Placed',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE companies (
                    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT,
                    industry TEXT,
                    website TEXT,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE job_postings (
                    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_id INTEGER,
                    job_title TEXT NOT NULL,
                    job_description TEXT,
                    job_type TEXT,
                    location TEXT,
                    salary_min REAL,
                    salary_max REAL,
                    min_cgpa REAL,
                    is_active INTEGER DEFAULT 1,
                    posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE student_applications (
                    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    application_status TEXT DEFAULT 'Applied',
                    UNIQUE(student_id, job_id)
                )
            """)
            
            # Insert default admin user
            conn.execute(
                "INSERT INTO users (username, email, password_hash, role, full_name) VALUES (?, ?, ?, ?, ?)",
                ('admin', 'admin@college.edu', self.hash_password('admin123'), 'college_admin', 'Admin User')
            )
            
            conn.execute(
                "INSERT INTO users (username, email, password_hash, role, full_name) VALUES (?, ?, ?, ?, ?)",
                ('student1', 'student1@college.edu', self.hash_password('student123'), 'student', 'Rahul Sharma')
            )
            
            # Insert sample companies
            companies = [
                ('Google', 'Technology', 'https://google.com', 'Search engine company'),
                ('Microsoft', 'Software', 'https://microsoft.com', 'Software company'),
                ('Amazon', 'E-commerce', 'https://amazon.com', 'Online retailer')
            ]
            
            for company in companies:
                conn.execute(
                    "INSERT INTO companies (company_name, industry, website, description) VALUES (?, ?, ?, ?)",
                    company
                )
            
            # Insert sample job
            conn.execute("""
                INSERT INTO job_postings (company_id, job_title, job_description, job_type, location, salary_min, salary_max, min_cgpa)
                VALUES (1, 'Software Engineer', 'Develop software applications', 'Full-time', 'Bangalore', 1500000, 2500000, 7.5)
            """)
            
            conn.commit()
            conn.close()
            
            print("Database initialized successfully with simple schema")
            
        except Exception as e:
            print(f"Error in simple initialization: {e}")
            # Create absolute minimum
            try:
                conn = sqlite3.connect(self.db_path)
                conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
                conn.execute("INSERT OR IGNORE INTO users (username, password) VALUES ('admin', 'admin123')")
                conn.commit()
                conn.close()
                print("Created absolute minimum database")
            except:
                print("Could not create any database")
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # === USER MANAGEMENT METHODS ===
    
    def create_user(self, username: str, email: str, password: str, role: str, 
                   full_name: str, phone: str = None) -> int:
        """Create a new user"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO users (username, email, password_hash, role, full_name, phone) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (username, email, self.hash_password(password), role, full_name, phone)
            )
            return cursor.lastrowid
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password_hash = ? AND is_active = 1",
                (username, self.hash_password(password))
            )
            user = cursor.fetchone()
            
            if user:
                # Update last login
                conn.execute(
                    "UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?",
                    (user['user_id'],)
                )
                return dict(user)
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    def update_user_profile(self, user_id: int, **kwargs):
        """Update user profile"""
        valid_fields = ['full_name', 'phone', 'email']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
        
        if updates:
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values())
            values.append(user_id)
            
            with self.get_connection() as conn:
                conn.execute(
                    f"UPDATE users SET {set_clause} WHERE user_id = ?",
                    values
                )
    
    # === STUDENT MANAGEMENT METHODS ===
    
    def create_student(self, user_id: int, roll_number: str, department: str, 
                      semester: int, cgpa: float = None, graduation_year: int = None) -> int:
        """Create a new student record"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO students (user_id, roll_number, department, semester, cgpa, graduation_year) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (user_id, roll_number, department, semester, cgpa, graduation_year)
            )
            return cursor.lastrowid
    
    def get_student_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get student by user ID"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT s.*, u.username, u.email, u.full_name, u.phone 
                   FROM students s 
                   JOIN users u ON s.user_id = u.user_id 
                   WHERE s.user_id = ?""",
                (user_id,)
            )
            student = cursor.fetchone()
            return dict(student) if student else None
    
    def update_student_profile(self, student_id: int, **kwargs):
        """Update student profile"""
        valid_fields = ['cgpa', 'semester', 'graduation_year', 'placement_status', 'department']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
        
        if updates:
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values())
            values.append(student_id)
            
            with self.get_connection() as conn:
                conn.execute(
                    f"UPDATE students SET {set_clause} WHERE student_id = ?",
                    values
                )
    
    def add_student_skill(self, student_id: int, skill_name: str, 
                         skill_level: str = 'Intermediate', skill_category: str = 'Technical'):
        """Add a skill to student profile"""
        # Create skills table if it doesn't exist
        with self.get_connection() as conn:
            try:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS student_skills (
                        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        skill_name TEXT NOT NULL,
                        skill_level TEXT,
                        skill_category TEXT DEFAULT 'Technical'
                    )
                """)
                
                cursor = conn.execute(
                    """INSERT INTO student_skills (student_id, skill_name, skill_level, skill_category) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, skill_name, skill_level, skill_category)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Skill already exists, update it
                conn.execute(
                    """UPDATE student_skills SET skill_level = ?, skill_category = ? 
                       WHERE student_id = ? AND skill_name = ?""",
                    (skill_level, skill_category, student_id, skill_name)
                )
                return -1
    
    def get_student_skills(self, student_id: int) -> List[Dict]:
        """Get all skills for a student"""
        with self.get_connection() as conn:
            try:
                cursor = conn.execute(
                    "SELECT * FROM student_skills WHERE student_id = ?",
                    (student_id,)
                )
                return [dict(row) for row in cursor.fetchall()]
            except:
                return []
    
    # === COMPANY & JOB MANAGEMENT METHODS ===
    
    def create_company(self, company_name: str, industry: str = None, website: str = None,
                      description: str = None, **kwargs) -> int:
        """Create a new company record"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO companies (company_name, industry, website, description) 
                   VALUES (?, ?, ?, ?)""",
                (company_name, industry, website, description)
            )
            return cursor.lastrowid
    
    def create_job_posting(self, company_id: int, job_title: str, job_description: str,
                          job_type: str, location: str, salary_min: float, salary_max: float,
                          vacancies: int = 1, min_cgpa: float = 7.0, max_backlogs: int = 2,
                          required_skills: List[str] = None, **kwargs) -> int:
        """Create a new job posting"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO job_postings 
                   (company_id, job_title, job_description, job_type, location, 
                    salary_min, salary_max, min_cgpa) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (company_id, job_title, job_description, job_type, location,
                 salary_min, salary_max, min_cgpa)
            )
            return cursor.lastrowid
    
    def get_active_jobs(self, filters: Dict = None) -> List[Dict]:
        """Get active job postings with optional filters"""
        query = """
            SELECT j.*, c.company_name, c.industry 
            FROM job_postings j 
            JOIN companies c ON j.company_id = c.company_id 
            WHERE j.is_active = 1
        """
        
        params = []
        
        if filters:
            conditions = []
            if filters.get('company_id'):
                conditions.append("j.company_id = ?")
                params.append(filters['company_id'])
            if filters.get('job_type'):
                conditions.append("j.job_type = ?")
                params.append(filters['job_type'])
            if filters.get('location'):
                conditions.append("j.location LIKE ?")
                params.append(f'%{filters["location"]}%')
            if filters.get('min_salary'):
                conditions.append("j.salary_min >= ?")
                params.append(filters['min_salary'])
            
            if conditions:
                query += " AND " + " AND ".join(conditions)
        
        query += " ORDER BY j.posted_date DESC"
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # === APPLICATION MANAGEMENT METHODS ===
    
    def apply_for_job(self, student_id: int, job_id: int, resume_version: str = None,
                     cover_letter: str = None) -> int:
        """Apply for a job"""
        with self.get_connection() as conn:
            try:
                cursor = conn.execute(
                    """INSERT INTO student_applications 
                       (student_id, job_id) 
                       VALUES (?, ?)""",
                    (student_id, job_id)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Already applied
                return -1
    
    def get_student_applications(self, student_id: int) -> List[Dict]:
        """Get all applications for a student"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                """SELECT a.*, j.job_title, j.job_type, j.location, 
                          c.company_name, c.industry 
                   FROM student_applications a 
                   JOIN job_postings j ON a.job_id = j.job_id 
                   JOIN companies c ON j.company_id = c.company_id 
                   WHERE a.student_id = ? 
                   ORDER BY a.application_date DESC""",
                (student_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def update_application_status(self, application_id: int, status: str, notes: str = None):
        """Update application status"""
        with self.get_connection() as conn:
            conn.execute(
                "UPDATE student_applications SET application_status = ? WHERE application_id = ?",
                (status, application_id)
            )
    
    # === ANALYTICS & REPORTING METHODS ===
    
    def get_placement_statistics(self, college_id: int = None, department: str = None) -> Dict:
        """Get placement statistics"""
        query = """
            SELECT 
                COUNT(*) as total_students,
                SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) as placed_count,
                AVG(cgpa) as avg_cgpa
            FROM students
            WHERE 1=1
        """
        
        params = []
        
        if department:
            query += " AND department = ?"
            params.append(department)
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            stats = dict(cursor.fetchone())
            
            # Calculate percentages
            if stats['total_students'] > 0:
                stats['placement_rate'] = (stats['placed_count'] / stats['total_students']) * 100
            else:
                stats['placement_rate'] = 0
            
            return stats
    
    def get_student_analytics(self, student_id: int) -> Dict:
        """Get comprehensive analytics for a student"""
        with self.get_connection() as conn:
            # Get basic student info
            cursor = conn.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (student_id,)
            )
            student = dict(cursor.fetchone())
            
            # Get applications
            cursor = conn.execute(
                """SELECT COUNT(*) as total_applications,
                          SUM(CASE WHEN application_status = 'Selected' THEN 1 ELSE 0 END) as selected_count
                   FROM student_applications 
                   WHERE student_id = ?""",
                (student_id,)
            )
            apps = dict(cursor.fetchone())
            
            return {
                **student,
                **apps,
                'application_success_rate': (apps['selected_count'] / apps['total_applications'] * 100) 
                                            if apps['total_applications'] > 0 else 0
            }
    
    # === RESUME MANAGEMENT METHODS ===
    
    def save_resume(self, student_id: int, resume_data: Dict, template_id: int = None,
                   resume_title: str = "My Resume") -> int:
        """Save student resume"""
        with self.get_connection() as conn:
            # Create resumes table if it doesn't exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS student_resumes (
                    resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    template_id INTEGER,
                    resume_title TEXT NOT NULL,
                    resume_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor = conn.execute(
                """INSERT INTO student_resumes 
                   (student_id, template_id, resume_title, resume_data) 
                   VALUES (?, ?, ?, ?)""",
                (student_id, template_id, resume_title, json.dumps(resume_data))
            )
            return cursor.lastrowid
    
    def get_student_resumes(self, student_id: int) -> List[Dict]:
        """Get all resumes for a student"""
        with self.get_connection() as conn:
            try:
                cursor = conn.execute(
                    """SELECT r.* 
                       FROM student_resumes r 
                       WHERE r.student_id = ? 
                       ORDER BY r.created_at DESC""",
                    (student_id,)
                )
                resumes = []
                for row in cursor.fetchall():
                    resume = dict(row)
                    if resume['resume_data']:
                        resume['resume_data'] = json.loads(resume['resume_data'])
                    resumes.append(resume)
                return resumes
            except:
                return []
    
    # === PLACEMENT PREDICTION METHODS ===
    
    def save_placement_prediction(self, student_id: int, placement_probability: float,
                                 predicted_companies: List[str] = None, 
                                 predicted_package: float = None, key_factors: Dict = None):
        """Save placement prediction for a student"""
        with self.get_connection() as conn:
            # Create predictions table if it doesn't exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS placement_predictions (
                    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    prediction_date DATE DEFAULT CURRENT_DATE,
                    placement_probability REAL,
                    predicted_companies TEXT,
                    predicted_package REAL
                )
            """)
            
            cursor = conn.execute(
                """INSERT INTO placement_predictions 
                   (student_id, placement_probability, predicted_companies, predicted_package) 
                   VALUES (?, ?, ?, ?)""",
                (student_id, placement_probability,
                 json.dumps(predicted_companies) if predicted_companies else None,
                 predicted_package)
            )
            return cursor.lastrowid
    
    def get_student_predictions(self, student_id: int) -> List[Dict]:
        """Get placement predictions for a student"""
        with self.get_connection() as conn:
            try:
                cursor = conn.execute(
                    """SELECT * FROM placement_predictions 
                       WHERE student_id = ? 
                       ORDER BY prediction_date DESC""",
                    (student_id,)
                )
                predictions = []
                for row in cursor.fetchall():
                    pred = dict(row)
                    if pred['predicted_companies']:
                        pred['predicted_companies'] = json.loads(pred['predicted_companies'])
                    predictions.append(pred)
                return predictions
            except:
                return []
    
    # === NEP COURSE PLANNING METHODS ===
    
    def save_nep_plan(self, student_id: int, major_subject: str, minor_subject: str = None,
                     total_credits: int = 160, planned_courses: List[Dict] = None) -> int:
        """Save NEP course plan for a student"""
        with self.get_connection() as conn:
            # Create NEP plans table if it doesn't exist
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nep_course_plans (
                    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    major_subject TEXT NOT NULL,
                    minor_subject TEXT,
                    total_credits INTEGER,
                    planned_courses TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor = conn.execute(
                """INSERT INTO nep_course_plans 
                   (student_id, major_subject, minor_subject, total_credits, planned_courses) 
                   VALUES (?, ?, ?, ?, ?)""",
                (student_id, major_subject, minor_subject, total_credits,
                 json.dumps(planned_courses) if planned_courses else None)
            )
            return cursor.lastrowid
    
    # === DATA EXPORT METHODS ===
    
    def export_to_dataframe(self, table_name: str, filters: Dict = None) -> pd.DataFrame:
        """Export table data to pandas DataFrame"""
        query = f"SELECT * FROM {table_name}"
        params = []
        
        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                params.append(value)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params if params else None)
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    # === UTILITY METHODS ===
    
    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = True):
        """Execute a custom SQL query"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params or ())
            if fetch_all:
                return [dict(row) for row in cursor.fetchall()]
            else:
                result = cursor.fetchone()
                return dict(result) if result else None
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (table_name,)
            )
            return cursor.fetchone() is not None
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """Get information about table columns"""
        with self.get_connection() as conn:
            cursor = conn.execute(f"PRAGMA table_info({table_name})")
            return [dict(row) for row in cursor.fetchall()]

# Singleton instance
db_manager = DatabaseManager()
