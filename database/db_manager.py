import sqlite3
import json
import pandas as pd
from datetime import datetime
from contextlib import contextmanager
import hashlib
from typing import Optional, List, Dict, Any
import os
import streamlit as st

class DatabaseManager:
    def __init__(self, db_path='campus_placement.db'):
        self.db_path = db_path
        try:
            self.init_database()
        except Exception as e:
            st.error(f"Database initialization failed: {str(e)}")
    
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
            st.error(f"Database error: {str(e)}")
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with schema"""
        with self.get_connection() as conn:
            # Create all tables
            self.create_tables(conn)
            # Insert default data
            self.insert_default_data(conn)
    
    def create_tables(self, conn):
        """Create all tables programmatically"""
        # Essential tables first
        essential_tables = [
            # Users table
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
            """,
            # Students table
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                roll_number VARCHAR(20) UNIQUE NOT NULL,
                department VARCHAR(50) NOT NULL,
                semester INTEGER,
                cgpa DECIMAL(3,2),
                backlogs INTEGER DEFAULT 0,
                graduation_year INTEGER,
                resume_file_path TEXT,
                github_profile TEXT,
                linkedin_profile TEXT,
                portfolio_website TEXT,
                placement_status VARCHAR(20) DEFAULT 'Not Placed',
                placement_company_id INTEGER,
                placement_package DECIMAL(10,2),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
            """,
            # Companies table
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name VARCHAR(100) UNIQUE NOT NULL,
                industry VARCHAR(50),
                website TEXT,
                description TEXT,
                logo_url TEXT,
                founded_year INTEGER,
                employee_count VARCHAR(50),
                headquarters VARCHAR(100),
                contact_person VARCHAR(100),
                contact_email VARCHAR(100),
                contact_phone VARCHAR(15),
                hr_email VARCHAR(100),
                is_verified BOOLEAN DEFAULT 0,
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            # Job postings table
            """
            CREATE TABLE IF NOT EXISTS job_postings (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                job_title VARCHAR(100) NOT NULL,
                job_description TEXT NOT NULL,
                job_type VARCHAR(20),
                location VARCHAR(100),
                salary_min DECIMAL(10,2),
                salary_max DECIMAL(10,2),
                salary_currency VARCHAR(3) DEFAULT 'INR',
                vacancies INTEGER DEFAULT 1,
                min_cgpa DECIMAL(3,2),
                max_backlogs INTEGER DEFAULT 0,
                required_skills TEXT,
                benefits TEXT,
                application_deadline DATE,
                posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (company_id) REFERENCES companies(company_id)
            )
            """,
            # Student applications table
            """
            CREATE TABLE IF NOT EXISTS student_applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                application_status VARCHAR(20) DEFAULT 'Applied',
                resume_version TEXT,
                cover_letter TEXT,
                applied_via VARCHAR(20) DEFAULT 'Portal',
                notes TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
                UNIQUE(student_id, job_id)
            )
            """
        ]
        
        # Create essential tables
        for sql in essential_tables:
            try:
                conn.execute(sql)
            except Exception as e:
                st.warning(f"Could not create table: {str(e)}")
        
        # Additional tables (optional)
        additional_tables = [
            # Student skills table
            """
            CREATE TABLE IF NOT EXISTS student_skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                skill_name VARCHAR(100) NOT NULL,
                skill_level VARCHAR(20) DEFAULT 'Intermediate',
                skill_category VARCHAR(50) DEFAULT 'Technical',
                years_of_experience DECIMAL(3,1) DEFAULT 0,
                last_used_year INTEGER,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """,
            # Student resumes table
            """
            CREATE TABLE IF NOT EXISTS student_resumes (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                template_id INTEGER,
                resume_title VARCHAR(100) DEFAULT 'My Resume',
                resume_data TEXT,
                resume_html TEXT,
                ats_score DECIMAL(5,2),
                is_primary BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """,
            # Resume templates table
            """
            CREATE TABLE IF NOT EXISTS resume_templates (
                template_id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name VARCHAR(100) NOT NULL,
                template_type VARCHAR(50) DEFAULT 'Modern',
                preview_url TEXT,
                is_free BOOLEAN DEFAULT 1,
                html_template TEXT,
                css_styles TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            # Placement predictions table
            """
            CREATE TABLE IF NOT EXISTS placement_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                prediction_date DATE NOT NULL,
                placement_probability DECIMAL(5,2),
                predicted_companies TEXT,
                predicted_package DECIMAL(10,2),
                key_factors TEXT,
                accuracy_score DECIMAL(5,2),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """,
            # NEP course plans table
            """
            CREATE TABLE IF NOT EXISTS nep_course_plans (
                plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                major_subject VARCHAR(100) NOT NULL,
                minor_subject VARCHAR(100),
                total_credits INTEGER DEFAULT 160,
                planned_courses TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
            """,
            # Interview schedule table
            """
            CREATE TABLE IF NOT EXISTS interviews (
                interview_id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                interview_date DATE NOT NULL,
                interview_time TIME NOT NULL,
                interview_type VARCHAR(50) DEFAULT 'Technical',
                interviewer_name VARCHAR(100),
                interview_link TEXT,
                duration_minutes INTEGER DEFAULT 60,
                status VARCHAR(20) DEFAULT 'Scheduled',
                feedback TEXT,
                rating INTEGER,
                FOREIGN KEY (application_id) REFERENCES student_applications(application_id)
            )
            """
        ]
        
        # Create additional tables (if they don't exist)
        for sql in additional_tables:
            try:
                conn.execute(sql)
            except:
                pass  # Skip if table creation fails
    
    def insert_default_data(self, conn):
        """Insert default/seed data"""
        try:
            # Check if users table is empty
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert default users
                default_users = [
                    ('admin', 'admin@college.edu', self.hash_password('admin123'), 'college_admin', 'Admin User', '9876543210'),
                    ('student1', 'student1@college.edu', self.hash_password('student123'), 'student', 'Rahul Sharma', '9876543211'),
                    ('recruiter1', 'hr@techcorp.com', self.hash_password('recruiter123'), 'recruiter', 'HR Manager', '9876543212')
                ]
                
                conn.executemany(
                    "INSERT INTO users (username, email, password_hash, role, full_name, phone) VALUES (?, ?, ?, ?, ?, ?)",
                    default_users
                )
                
                # Insert default companies
                default_companies = [
                    ('Google', 'IT', 'https://google.com', 'Technology company', None, '100,000+', 'California', 'John Doe', 'john@google.com', '1234567890', 'hr@google.com'),
                    ('Microsoft', 'IT', 'https://microsoft.com', 'Software company', None, '200,000+', 'Washington', 'Jane Smith', 'jane@microsoft.com', '1234567891', 'hr@microsoft.com'),
                    ('Amazon', 'E-commerce', 'https://amazon.com', 'E-commerce giant', None, '1,500,000+', 'Seattle', 'Bob Johnson', 'bob@amazon.com', '1234567892', 'hr@amazon.com')
                ]
                
                conn.executemany(
                    """INSERT INTO companies 
                       (company_name, industry, website, description, logo_url, employee_count, headquarters,
                        contact_person, contact_email, contact_phone, hr_email) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    default_companies
                )
                
                # Insert default job postings
                cursor = conn.execute("SELECT company_id FROM companies WHERE company_name = 'Google'")
                google_row = cursor.fetchone()
                if google_row:
                    google_id = google_row[0]
                    
                    default_jobs = [
                        (google_id, 'Software Development Engineer', 'Develop and maintain software applications', 
                         'Full-time', 'Bangalore', 15.0, 30.0, 10, 7.5, 2, 'Python,Java,SQL', 'Health insurance, stock options', '2024-12-31'),
                        (google_id, 'Product Manager Intern', 'Assist in product development', 'Internship', 
                         'Hyderabad', 0.7, 1.0, 5, 8.0, 0, 'Product Management,Analytics', 'Mentorship, housing allowance', '2024-12-31')
                    ]
                    
                    conn.executemany(
                        """INSERT INTO job_postings 
                           (company_id, job_title, job_description, job_type, location, 
                            salary_min, salary_max, vacancies, min_cgpa, max_backlogs, 
                            required_skills, benefits, application_deadline) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        default_jobs
                    )
        except Exception as e:
            st.warning(f"Could not insert default data: {str(e)}")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # === USER MANAGEMENT METHODS ===
    
    def create_user(self, username: str, email: str, password: str, role: str, 
                   full_name: str, phone: str = None) -> Optional[int]:
        """Create a new user"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO users (username, email, password_hash, role, full_name, phone) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (username, email, self.hash_password(password), role, full_name, phone)
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        try:
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
        except Exception as e:
            st.error(f"Error authenticating user: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                return dict(user) if user else None
        except Exception as e:
            st.error(f"Error getting user: {str(e)}")
            return None
    
    # === STUDENT MANAGEMENT METHODS ===
    
    def create_student(self, user_id: int, roll_number: str, department: str, 
                      semester: int, cgpa: float = None, graduation_year: int = None) -> Optional[int]:
        """Create a new student record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO students (user_id, roll_number, department, semester, cgpa, graduation_year) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (user_id, roll_number, department, semester, cgpa, graduation_year)
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error creating student: {str(e)}")
            return None
    
    def get_student_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get student by user ID"""
        try:
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
        except Exception as e:
            st.error(f"Error getting student: {str(e)}")
            return None
    
    def update_student_profile(self, student_id: int, **kwargs):
        """Update student profile"""
        valid_fields = ['cgpa', 'semester', 'backlogs', 'graduation_year', 
                       'github_profile', 'linkedin_profile', 'portfolio_website',
                       'resume_file_path', 'placement_status', 'placement_company_id', 'placement_package']
        
        updates = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
        
        if updates:
            set_clause = ', '.join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values())
            values.append(student_id)
            
            try:
                with self.get_connection() as conn:
                    conn.execute(
                        f"UPDATE students SET {set_clause} WHERE student_id = ?",
                        values
                    )
            except Exception as e:
                st.error(f"Error updating student: {str(e)}")
    
    def get_student_by_id(self, student_id: int) -> Optional[Dict]:
        """Get student by student ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT s.*, u.username, u.email, u.full_name, u.phone 
                       FROM students s 
                       JOIN users u ON s.user_id = u.user_id 
                       WHERE s.student_id = ?""",
                    (student_id,)
                )
                student = cursor.fetchone()
                return dict(student) if student else None
        except Exception as e:
            st.error(f"Error getting student: {str(e)}")
            return None
    
    def get_all_students(self) -> List[Dict]:
        """Get all students"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT s.*, u.username, u.email, u.full_name, u.phone 
                       FROM students s 
                       JOIN users u ON s.user_id = u.user_id 
                       ORDER BY s.student_id"""
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Error getting students: {str(e)}")
            return []
    
    def add_student_skill(self, student_id: int, skill_name: str, 
                         skill_level: str = 'Intermediate', skill_category: str = 'Technical'):
        """Add a skill to student profile"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO student_skills (student_id, skill_name, skill_level, skill_category) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, skill_name, skill_level, skill_category)
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error adding skill: {str(e)}")
            return None
    
    def get_student_skills(self, student_id: int) -> List[Dict]:
        """Get all skills for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM student_skills WHERE student_id = ?",
                    (student_id,)
                )
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []
    
    # === COMPANY & JOB MANAGEMENT METHODS ===
    
    def create_company(self, company_name: str, industry: str = None, website: str = None,
                      description: str = None, **kwargs) -> Optional[int]:
        """Create a new company record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO companies (company_name, industry, website, description, 
                       contact_person, contact_email, contact_phone, hr_email) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (company_name, industry, website, description,
                     kwargs.get('contact_person'), kwargs.get('contact_email'),
                     kwargs.get('contact_phone'), kwargs.get('hr_email'))
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error creating company: {str(e)}")
            return None
    
    def get_company_by_id(self, company_id: int) -> Optional[Dict]:
        """Get company by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM companies WHERE company_id = ?",
                    (company_id,)
                )
                company = cursor.fetchone()
                return dict(company) if company else None
        except Exception as e:
            st.error(f"Error getting company: {str(e)}")
            return None
    
    def get_all_companies(self) -> List[Dict]:
        """Get all companies"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT * FROM companies ORDER BY company_name"
                )
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Error getting companies: {str(e)}")
            return []
    
    def create_job_posting(self, company_id: int, job_title: str, job_description: str,
                          job_type: str, location: str, salary_min: float, salary_max: float,
                          vacancies: int = 1, min_cgpa: float = 7.0, max_backlogs: int = 2,
                          required_skills: List[str] = None, **kwargs) -> Optional[int]:
        """Create a new job posting"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO job_postings 
                       (company_id, job_title, job_description, job_type, location, 
                        salary_min, salary_max, vacancies, min_cgpa, max_backlogs, 
                        required_skills, benefits, application_deadline) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (company_id, job_title, job_description, job_type, location,
                     salary_min, salary_max, vacancies, min_cgpa, max_backlogs,
                     ','.join(required_skills) if required_skills else None,
                     kwargs.get('benefits'), kwargs.get('application_deadline'))
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error creating job posting: {str(e)}")
            return None
    
    def get_active_jobs(self, filters: Dict = None) -> List[Dict]:
        """Get active job postings with optional filters"""
        query = """
            SELECT j.*, c.company_name, c.industry, c.logo_url 
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
        
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Error getting jobs: {str(e)}")
            return []
    
    def get_job_by_id(self, job_id: int) -> Optional[Dict]:
        """Get job posting by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT j.*, c.company_name, c.industry, c.website 
                       FROM job_postings j 
                       JOIN companies c ON j.company_id = c.company_id 
                       WHERE j.job_id = ?""",
                    (job_id,)
                )
                job = cursor.fetchone()
                return dict(job) if job else None
        except Exception as e:
            st.error(f"Error getting job: {str(e)}")
            return None
    
    # === APPLICATION MANAGEMENT METHODS ===
    
    def apply_for_job(self, student_id: int, job_id: int, resume_version: str = None,
                     cover_letter: str = None) -> Optional[int]:
        """Apply for a job"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO student_applications 
                       (student_id, job_id, resume_version, cover_letter) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, job_id, resume_version, cover_letter)
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Already applied
            return -1
        except Exception as e:
            st.error(f"Error applying for job: {str(e)}")
            return None
    
    def get_student_applications(self, student_id: int) -> List[Dict]:
        """Get all applications for a student"""
        try:
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
        except Exception as e:
            st.error(f"Error getting applications: {str(e)}")
            return []
    
    def update_application_status(self, application_id: int, status: str, notes: str = None):
        """Update application status"""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "UPDATE student_applications SET application_status = ?, notes = ? WHERE application_id = ?",
                    (status, notes, application_id)
                )
        except Exception as e:
            st.error(f"Error updating application: {str(e)}")
    
    def get_application_by_id(self, application_id: int) -> Optional[Dict]:
        """Get application by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT a.*, s.roll_number, u.full_name as student_name,
                              j.job_title, c.company_name
                       FROM student_applications a
                       JOIN students s ON a.student_id = s.student_id
                       JOIN users u ON s.user_id = u.user_id
                       JOIN job_postings j ON a.job_id = j.job_id
                       JOIN companies c ON j.company_id = c.company_id
                       WHERE a.application_id = ?""",
                    (application_id,)
                )
                app = cursor.fetchone()
                return dict(app) if app else None
        except Exception as e:
            st.error(f"Error getting application: {str(e)}")
            return None
    
    # === ANALYTICS & REPORTING METHODS ===
    
    def get_placement_statistics(self, department: str = None) -> Dict:
        """Get placement statistics"""
        try:
            with self.get_connection() as conn:
                query = """
                    SELECT 
                        COUNT(*) as total_students,
                        SUM(CASE WHEN placement_status = 'Placed' THEN 1 ELSE 0 END) as placed_count,
                        SUM(CASE WHEN placement_status = 'Intern' THEN 1 ELSE 0 END) as intern_count,
                        AVG(CASE WHEN placement_status = 'Placed' THEN placement_package ELSE NULL END) as avg_package,
                        AVG(cgpa) as avg_cgpa
                    FROM students
                    WHERE 1=1
                """
                
                params = []
                if department:
                    query += " AND department = ?"
                    params.append(department)
                
                cursor = conn.execute(query, params)
                stats = dict(cursor.fetchone())
                
                # Calculate percentages
                if stats['total_students'] and stats['total_students'] > 0:
                    stats['placement_rate'] = (stats['placed_count'] / stats['total_students']) * 100
                    stats['intern_rate'] = (stats['intern_count'] / stats['total_students']) * 100
                else:
                    stats['placement_rate'] = 0
                    stats['intern_rate'] = 0
                
                return stats
        except Exception as e:
            st.error(f"Error getting statistics: {str(e)}")
            return {'total_students': 0, 'placed_count': 0, 'intern_count': 0, 
                   'avg_package': 0, 'avg_cgpa': 0, 'placement_rate': 0, 'intern_rate': 0}
    
    def get_student_analytics(self, student_id: int) -> Dict:
        """Get comprehensive analytics for a student"""
        try:
            with self.get_connection() as conn:
                # Get basic student info
                cursor = conn.execute(
                    "SELECT * FROM students WHERE student_id = ?",
                    (student_id,)
                )
                student = dict(cursor.fetchone()) if cursor.fetchone() else {}
                
                # Get applications
                cursor = conn.execute(
                    """SELECT COUNT(*) as total_applications,
                              SUM(CASE WHEN application_status = 'Selected' THEN 1 ELSE 0 END) as selected_count,
                              SUM(CASE WHEN application_status = 'Rejected' THEN 1 ELSE 0 END) as rejected_count
                       FROM student_applications 
                       WHERE student_id = ?""",
                    (student_id,)
                )
                apps_row = cursor.fetchone()
                apps = dict(apps_row) if apps_row else {'total_applications': 0, 'selected_count': 0, 'rejected_count': 0}
                
                # Get skills count
                cursor = conn.execute(
                    "SELECT COUNT(*) as total_skills FROM student_skills WHERE student_id = ?",
                    (student_id,)
                )
                skills_row = cursor.fetchone()
                skills = dict(skills_row) if skills_row else {'total_skills': 0}
                
                # Calculate success rate
                if apps['total_applications'] > 0:
                    success_rate = (apps['selected_count'] / apps['total_applications'] * 100)
                else:
                    success_rate = 0
                
                return {
                    **student,
                    **apps,
                    **skills,
                    'application_success_rate': success_rate
                }
        except Exception as e:
            st.error(f"Error getting analytics: {str(e)}")
            return {}
    
    # === RESUME MANAGEMENT METHODS ===
    
    def save_resume(self, student_id: int, resume_data: Dict, template_id: int = None,
                   resume_title: str = "My Resume") -> Optional[int]:
        """Save student resume"""
        try:
            with self.get_connection() as conn:
                # If setting as primary, unset other primary resumes
                if resume_data.get('is_primary'):
                    conn.execute(
                        "UPDATE student_resumes SET is_primary = 0 WHERE student_id = ?",
                        (student_id,)
                    )
                
                cursor = conn.execute(
                    """INSERT INTO student_resumes 
                       (student_id, template_id, resume_title, resume_data, resume_html, ats_score, is_primary) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (student_id, template_id, resume_title, 
                     json.dumps(resume_data), resume_data.get('html', ''),
                     resume_data.get('ats_score', 0), resume_data.get('is_primary', 0))
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error saving resume: {str(e)}")
            return None
    
    def get_student_resumes(self, student_id: int) -> List[Dict]:
        """Get all resumes for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT r.*, t.template_name 
                       FROM student_resumes r 
                       LEFT JOIN resume_templates t ON r.template_id = t.template_id 
                       WHERE r.student_id = ? 
                       ORDER BY r.is_primary DESC, r.created_at DESC""",
                    (student_id,)
                )
                resumes = []
                for row in cursor.fetchall():
                    resume = dict(row)
                    if resume['resume_data']:
                        try:
                            resume['resume_data'] = json.loads(resume['resume_data'])
                        except:
                            resume['resume_data'] = {}
                    resumes.append(resume)
                return resumes
        except:
            return []
    
    # === PLACEMENT PREDICTION METHODS ===
    
    def save_placement_prediction(self, student_id: int, placement_probability: float,
                                 predicted_companies: List[str] = None, 
                                 predicted_package: float = None, key_factors: Dict = None):
        """Save placement prediction for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO placement_predictions 
                       (student_id, prediction_date, placement_probability, 
                        predicted_companies, predicted_package, key_factors) 
                       VALUES (?, DATE('now'), ?, ?, ?, ?)""",
                    (student_id, placement_probability,
                     json.dumps(predicted_companies) if predicted_companies else None,
                     predicted_package, json.dumps(key_factors) if key_factors else None)
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error saving prediction: {str(e)}")
            return None
    
    def get_student_predictions(self, student_id: int) -> List[Dict]:
        """Get placement predictions for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """SELECT * FROM placement_predictions 
                       WHERE student_id = ? 
                       ORDER BY prediction_date DESC""",
                    (student_id,)
                )
                predictions = []
                for row in cursor.fetchall():
                    pred = dict(row)
                    if pred.get('predicted_companies'):
                        try:
                            pred['predicted_companies'] = json.loads(pred['predicted_companies'])
                        except:
                            pred['predicted_companies'] = []
                    if pred.get('key_factors'):
                        try:
                            pred['key_factors'] = json.loads(pred['key_factors'])
                        except:
                            pred['key_factors'] = {}
                    predictions.append(pred)
                return predictions
        except:
            return []
    
    # === NEP COURSE PLANNING METHODS ===
    
    def save_nep_plan(self, student_id: int, major_subject: str, minor_subject: str = None,
                     total_credits: int = 160, planned_courses: List[Dict] = None) -> Optional[int]:
        """Save NEP course plan for a student"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    """INSERT INTO nep_course_plans 
                       (student_id, major_subject, minor_subject, total_credits, planned_courses) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (student_id, major_subject, minor_subject, total_credits,
                     json.dumps(planned_courses) if planned_courses else None)
                )
                return cursor.lastrowid
        except Exception as e:
            st.error(f"Error saving NEP plan: {str(e)}")
            return None
    
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
        
        try:
            with self.get_connection() as conn:
                return pd.read_sql_query(query, conn, params=params if params else None)
        except Exception as e:
            st.error(f"Error exporting data: {str(e)}")
            return pd.DataFrame()
    
    def backup_database(self, backup_path: str):
        """Create a backup of the database"""
        import shutil
        try:
            shutil.copy2(self.db_path, backup_path)
        except Exception as e:
            st.error(f"Error backing up database: {str(e)}")
    
    # === UTILITY METHODS ===
    
    def execute_query(self, query: str, params: tuple = None, fetch_all: bool = True):
        """Execute a custom SQL query"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(query, params or ())
                if fetch_all:
                    return [dict(row) for row in cursor.fetchall()]
                else:
                    result = cursor.fetchone()
                    return dict(result) if result else None
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
            return [] if fetch_all else None
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,)
                )
                return cursor.fetchone() is not None
        except:
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict]:
        """Get information about table columns"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                return [dict(row) for row in cursor.fetchall()]
        except:
            return []
    
    def check_database_status(self):
        """Check if database tables are properly created"""
        status = {}
        tables_to_check = ['users', 'students', 'companies', 'job_postings', 'student_applications']
        
        try:
            with self.get_connection() as conn:
                for table in tables_to_check:
                    try:
                        cursor = conn.execute(f"SELECT COUNT(*) as count FROM {table}")
                        count = cursor.fetchone()[0]
                        status[table] = f"✓ Exists ({count} rows)"
                    except:
                        status[table] = "✗ Missing or Error"
        except Exception as e:
            status['connection'] = f"✗ Error: {str(e)}"
        
        return status

# Singleton instance - with error handling
try:
    db_manager = DatabaseManager()
    if db_manager:
        # Check database status
        status = db_manager.check_database_status()
        st.sidebar.success("✅ Database Connected")
        # Uncomment to see detailed status
        # for table, stat in status.items():
        #     st.sidebar.write(f"  {table}: {stat}")
except Exception as e:
    st.error(f"Failed to initialize database: {str(e)}")
    db_manager = None
