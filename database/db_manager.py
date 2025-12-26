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
        self.init_database()
    
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
    
    def init_database(self):
        """Initialize database with schema - with robust error handling"""
        try:
            with self.get_connection() as conn:
                # Read and execute schema SQL
                schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
                
                if os.path.exists(schema_path):
                    print(f"Found schema.sql at {schema_path}")
                    with open(schema_path, 'r') as f:
                        schema_sql = f.read()
                    
                    try:
                        # Execute schema creation safely
                        self.execute_schema_safely(conn, schema_sql)
                        
                        # Insert default data
                        self.insert_default_data(conn)
                        print("Database initialized successfully from schema.sql")
                        
                    except Exception as schema_error:
                        print(f"Error executing schema.sql: {schema_error}")
                        print("Attempting programmatic table creation...")
                        
                        # Try programmatic creation as fallback
                        try:
                            self.create_tables(conn)
                            self.insert_default_data(conn)
                            print("Database initialized successfully via programmatic creation")
                        except Exception as fallback_error:
                            print(f"Fallback also failed: {fallback_error}")
                            # Try minimal tables
                            self.create_minimal_tables(conn)
                else:
                    print("schema.sql not found, creating tables programmatically...")
                    # Create tables programmatically if schema file doesn't exist
                    self.create_tables(conn)
                    self.insert_default_data(conn)
                    print("Database initialized successfully via programmatic creation")
                    
        except Exception as e:
            print(f"Critical error initializing database: {e}")
            # Try to create minimal tables as last resort
            self.create_minimal_tables_as_last_resort()
    
    def execute_schema_safely(self, conn, schema_sql):
        """Execute schema SQL statement by statement with error handling"""
        # Split by semicolons and execute each statement separately
        statements = schema_sql.split(';')
        
        for statement in statements:
            # Clean up the statement
            statement = statement.strip()
            if not statement:
                continue
                
            # Skip comments
            if statement.startswith('--'):
                continue
                
            try:
                # Execute the statement
                conn.execute(statement)
            except sqlite3.OperationalError as e:
                # Check if it's an "already exists" error
                error_msg = str(e).lower()
                if any(keyword in error_msg for keyword in ['already exists', 'duplicate', 'index']):
                    print(f"Note: Skipping statement (already exists): {statement[:50]}...")
                else:
                    # Re-raise for other operational errors
                    raise e
    
    def create_minimal_tables(self, conn):
        """Create only the essential tables needed for the app to run"""
        minimal_tables = [
            # Users table
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'college_admin', 'recruiter', 'tpo')),
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
                semester INTEGER CHECK (semester BETWEEN 1 AND 10),
                cgpa DECIMAL(3,2) CHECK (cgpa BETWEEN 0.00 AND 10.00),
                backlogs INTEGER DEFAULT 0,
                graduation_year INTEGER,
                resume_file_path TEXT,
                github_profile TEXT,
                linkedin_profile TEXT,
                portfolio_website TEXT,
                placement_status VARCHAR(20) DEFAULT 'Not Placed' CHECK (placement_status IN ('Not Placed', 'Placed', 'Intern', 'Higher Studies')),
                placement_company_id INTEGER,
                placement_package DECIMAL(10,2),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
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
                job_type VARCHAR(20) CHECK (job_type IN ('Full-time', 'Internship', 'Contract', 'Part-time')),
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
                FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
            )
            """
        ]
        
        for sql in minimal_tables:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError as e:
                print(f"Note: Could not create table: {e}")
        
        # Insert absolutely essential default data
        self.insert_minimal_default_data(conn)
    
    def create_minimal_tables_as_last_resort(self):
        """Absolute last resort - try to create tables without any dependencies"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL
                )
            """)
            conn.commit()
            conn.close()
            print("Created minimal users table as last resort")
        except Exception as e:
            print(f"Even last resort failed: {e}")
    
    def insert_minimal_default_data(self, conn):
        """Insert absolutely essential default data"""
        try:
            # Check if we have any users
            cursor = conn.execute("SELECT COUNT(*) as count FROM users")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert only the admin user
                conn.execute(
                    "INSERT INTO users (username, email, password_hash, role, full_name) VALUES (?, ?, ?, ?, ?)",
                    ('admin', 'admin@college.edu', self.hash_password('admin123'), 'college_admin', 'Admin User')
                )
                print("Inserted minimal default data")
        except Exception as e:
            print(f"Could not insert minimal default data: {e}")
    
    def create_tables(self, conn):
        """Create tables programmatically"""
        # This is a fallback if schema.sql doesn't exist or fails
        tables_sql = [
            # Users table
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL CHECK (role IN ('student', 'college_admin', 'recruiter', 'tpo')),
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
            """,
            # Companies table (moved up to avoid circular references)
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
            # Students table
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                roll_number VARCHAR(20) UNIQUE NOT NULL,
                department VARCHAR(50) NOT NULL,
                semester INTEGER CHECK (semester BETWEEN 1 AND 10),
                cgpa DECIMAL(3,2) CHECK (cgpa BETWEEN 0.00 AND 10.00),
                backlogs INTEGER DEFAULT 0,
                graduation_year INTEGER,
                resume_file_path TEXT,
                github_profile TEXT,
                linkedin_profile TEXT,
                portfolio_website TEXT,
                placement_status VARCHAR(20) DEFAULT 'Not Placed' CHECK (placement_status IN ('Not Placed', 'Placed', 'Intern', 'Higher Studies')),
                placement_company_id INTEGER,
                placement_package DECIMAL(10,2),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (placement_company_id) REFERENCES companies(company_id) ON DELETE SET NULL
            )
            """,
            # Job postings table
            """
            CREATE TABLE IF NOT EXISTS job_postings (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                job_title VARCHAR(100) NOT NULL,
                job_description TEXT NOT NULL,
                job_type VARCHAR(20) CHECK (job_type IN ('Full-time', 'Internship', 'Contract', 'Part-time')),
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
                FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
            )
            """,
            # Student applications table
            """
            CREATE TABLE IF NOT EXISTS student_applications (
                application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                application_status VARCHAR(20) DEFAULT 'Applied' CHECK (application_status IN ('Applied', 'Shortlisted', 'Rejected', 'Interview', 'Selected', 'Offer Accepted', 'Offer Declined')),
                resume_version TEXT,
                cover_letter TEXT,
                applied_via VARCHAR(20) DEFAULT 'Portal',
                notes TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                FOREIGN KEY (job_id) REFERENCES job_postings(job_id) ON DELETE CASCADE,
                UNIQUE(student_id, job_id)
            )
            """,
            # Student skills table
            """
            CREATE TABLE IF NOT EXISTS student_skills (
                skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                skill_name VARCHAR(50) NOT NULL,
                skill_level VARCHAR(20) CHECK (skill_level IN ('Beginner', 'Intermediate', 'Advanced')),
                skill_category VARCHAR(20) DEFAULT 'Technical',
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                UNIQUE(student_id, skill_name)
            )
            """,
            # Student resumes table
            """
            CREATE TABLE IF NOT EXISTS student_resumes (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                template_id INTEGER,
                resume_title VARCHAR(100) NOT NULL,
                resume_data TEXT NOT NULL,
                resume_html TEXT,
                resume_pdf_path TEXT,
                ats_score INTEGER,
                is_primary BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
            """,
            # Resume templates table
            """
            CREATE TABLE IF NOT EXISTS resume_templates (
                template_id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_name VARCHAR(50) NOT NULL,
                template_description TEXT,
                template_html TEXT NOT NULL,
                template_css TEXT,
                category VARCHAR(20) DEFAULT 'Professional',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            # Placement predictions table
            """
            CREATE TABLE IF NOT EXISTS placement_predictions (
                prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                prediction_date DATE NOT NULL,
                placement_probability DECIMAL(5,2) CHECK (placement_probability BETWEEN 0 AND 100),
                predicted_companies TEXT,
                predicted_package DECIMAL(10,2),
                key_factors TEXT,
                model_version VARCHAR(20),
                confidence_score DECIMAL(5,2),
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
            """,
            # NEP course plans table
            """
            CREATE TABLE IF NOT EXISTS nep_course_plans (
                plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                major_subject VARCHAR(50) NOT NULL,
                minor_subject VARCHAR(50),
                specialization VARCHAR(50),
                total_credits INTEGER DEFAULT 160,
                planned_courses TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
            )
            """
        ]
        
        for sql in tables_sql:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError as e:
                print(f"Note: Could not create table: {e}")
                # Try to continue with other tables
        
        # Create indexes with IF NOT EXISTS
        indexes_sql = [
            "CREATE INDEX IF NOT EXISTS idx_students_user_id ON students(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_students_department ON students(department)",
            "CREATE INDEX IF NOT EXISTS idx_students_placement ON students(placement_status)",
            "CREATE INDEX IF NOT EXISTS idx_jobs_company ON job_postings(company_id)",
            "CREATE INDEX IF NOT EXISTS idx_jobs_active ON job_postings(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_applications_student ON student_applications(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_applications_job ON student_applications(job_id)",
            "CREATE INDEX IF NOT EXISTS idx_applications_status ON student_applications(application_status)",
            "CREATE INDEX IF NOT EXISTS idx_users_role ON users(role)",
            "CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active)",
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"
        ]
        
        for sql in indexes_sql:
            try:
                conn.execute(sql)
            except sqlite3.OperationalError as e:
                print(f"Note: Could not create index: {e}")
    
    def insert_default_data(self, conn):
        """Insert default/seed data"""
        try:
            # Check if default data already exists
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
                    "INSERT OR IGNORE INTO users (username, email, password_hash, role, full_name, phone) VALUES (?, ?, ?, ?, ?, ?)",
                    default_users
                )
                
                # Insert default companies
                default_companies = [
                    ('Google', 'IT', 'https://google.com', 'Technology company', 1998, '100,000+', 'California'),
                    ('Microsoft', 'IT', 'https://microsoft.com', 'Software company', 1975, '200,000+', 'Washington'),
                    ('Amazon', 'E-commerce', 'https://amazon.com', 'E-commerce giant', 1994, '1,500,000+', 'Seattle')
                ]
                
                conn.executemany(
                    """INSERT OR IGNORE INTO companies (company_name, industry, website, description, founded_year, employee_count, headquarters) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    default_companies
                )
                
                # Insert default resume templates
                default_templates = [
                    ('Professional', 'Clean and professional resume template for corporate jobs', '<div class="resume">Professional Template</div>', 'Professional'),
                    ('Modern', 'Modern design with accent colors', '<div class="resume">Modern Template</div>', 'Modern'),
                    ('ATS-Friendly', 'Simple format for Applicant Tracking Systems', '<div class="resume">ATS Template</div>', 'ATS')
                ]
                
                conn.executemany(
                    """INSERT OR IGNORE INTO resume_templates (template_name, template_description, template_html, category) 
                       VALUES (?, ?, ?, ?)""",
                    default_templates
                )
                
                # Try to insert default job postings if we have companies
                try:
                    cursor = conn.execute("SELECT company_id FROM companies WHERE company_name = 'Google'")
                    google_row = cursor.fetchone()
                    if google_row:
                        google_id = google_row[0]
                        
                        default_jobs = [
                            (google_id, 'Software Development Engineer', 'Develop and maintain software applications', 
                             'Full-time', 'Bangalore', 15.0, 30.0, 10, 7.5, 2, 'Python,Java,SQL', 'Health insurance, stock options', '2024-06-30'),
                            (google_id, 'Product Manager Intern', 'Assist in product development', 'Internship', 
                             'Hyderabad', 0.7, 1.0, 5, 8.0, 0, 'Product Management,Analytics', 'Mentorship, housing allowance', '2024-05-15')
                        ]
                        
                        conn.executemany(
                            """INSERT OR IGNORE INTO job_postings (company_id, job_title, job_description, job_type, location, 
                               salary_min, salary_max, vacancies, min_cgpa, max_backlogs, required_skills, benefits, application_deadline) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            default_jobs
                        )
                except Exception as e:
                    print(f"Could not insert default jobs: {e}")
                    
                print("Default data inserted successfully")
        except Exception as e:
            print(f"Error inserting default data: {e}")
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ... rest of your methods remain the same (user management, student management, etc.)
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
    
    # ... (keep all other methods as they were in your original file)
    # I'll continue with the rest of your methods but truncated for brevity
    # Please copy the rest of your original methods here
    
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
        valid_fields = ['cgpa', 'semester', 'backlogs', 'graduation_year', 
                       'github_profile', 'linkedin_profile', 'portfolio_website',
                       'resume_file_path', 'placement_status', 'placement_package']
        
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
        with self.get_connection() as conn:
            try:
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
    
    def get_student_skills(self, student_id: int) -> List[Dict]:
        """Get all skills for a student"""
        with self.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM student_skills WHERE student_id = ?",
                (student_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    
    # === COMPANY & JOB MANAGEMENT METHODS ===
    
    def create_company(self, company_name: str, industry: str = None, website: str = None,
                      description: str = None, **kwargs) -> int:
        """Create a new company record"""
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
    
    def create_job_posting(self, company_id: int, job_title: str, job_description: str,
                          job_type: str, location: str, salary_min: float, salary_max: float,
                          vacancies: int = 1, min_cgpa: float = 7.0, max_backlogs: int = 2,
                          required_skills: List[str] = None, **kwargs) -> int:
        """Create a new job posting"""
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
                       (student_id, job_id, resume_version, cover_letter) 
                       VALUES (?, ?, ?, ?)""",
                    (student_id, job_id, resume_version, cover_letter)
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
                "UPDATE student_applications SET application_status = ?, notes = ? WHERE application_id = ?",
                (status, notes, application_id)
            )
    
    # === ANALYTICS & REPORTING METHODS ===
    
    def get_placement_statistics(self, college_id: int = None, department: str = None) -> Dict:
        """Get placement statistics"""
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
        
        if college_id:
            # Assuming students are linked to college through some relation
            # You might need to adjust this based on your schema
            pass
        
        if department:
            query += " AND department = ?"
            params.append(department)
        
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            stats = dict(cursor.fetchone())
            
            # Calculate percentages
            if stats['total_students'] > 0:
                stats['placement_rate'] = (stats['placed_count'] / stats['total_students']) * 100
                stats['intern_rate'] = (stats['intern_count'] / stats['total_students']) * 100
            else:
                stats['placement_rate'] = 0
                stats['intern_rate'] = 0
            
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
                          SUM(CASE WHEN application_status = 'Selected' THEN 1 ELSE 0 END) as selected_count,
                          SUM(CASE WHEN application_status = 'Rejected' THEN 1 ELSE 0 END) as rejected_count
                   FROM student_applications 
                   WHERE student_id = ?""",
                (student_id,)
            )
            apps = dict(cursor.fetchone())
            
            # Get skills
            cursor = conn.execute(
                "SELECT COUNT(*) as total_skills FROM student_skills WHERE student_id = ?",
                (student_id,)
            )
            skills = dict(cursor.fetchone())
            
            return {
                **student,
                **apps,
                **skills,
                'application_success_rate': (apps['selected_count'] / apps['total_applications'] * 100) 
                                            if apps['total_applications'] > 0 else 0
            }
    
    # === RESUME MANAGEMENT METHODS ===
    
    def save_resume(self, student_id: int, resume_data: Dict, template_id: int = None,
                   resume_title: str = "My Resume") -> int:
        """Save student resume"""
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
    
    def get_student_resumes(self, student_id: int) -> List[Dict]:
        """Get all resumes for a student"""
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
                    resume['resume_data'] = json.loads(resume['resume_data'])
                resumes.append(resume)
            return resumes
    
    # === PLACEMENT PREDICTION METHODS ===
    
    def save_placement_prediction(self, student_id: int, placement_probability: float,
                                 predicted_companies: List[str] = None, 
                                 predicted_package: float = None, key_factors: Dict = None):
        """Save placement prediction for a student"""
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
    
    def get_student_predictions(self, student_id: int) -> List[Dict]:
        """Get placement predictions for a student"""
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
                if pred['predicted_companies']:
                    pred['predicted_companies'] = json.loads(pred['predicted_companies'])
                if pred['key_factors']:
                    pred['key_factors'] = json.loads(pred['key_factors'])
                predictions.append(pred)
            return predictions
    
    # === NEP COURSE PLANNING METHODS ===
    
    def save_nep_plan(self, student_id: int, major_subject: str, minor_subject: str = None,
                     total_credits: int = 160, planned_courses: List[Dict] = None) -> int:
        """Save NEP course plan for a student"""
        with self.get_connection() as conn:
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

# Singleton instance - with error handling
try:
    db_manager = DatabaseManager()
    print("Database manager initialized successfully")
except Exception as e:
    print(f"Error initializing database manager: {e}")
    # Create a minimal db_manager that at least won't crash
    db_manager = None
