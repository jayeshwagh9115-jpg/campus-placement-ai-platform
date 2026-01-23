import streamlit as st
import pandas as pd
import json
import traceback
from datetime import datetime
import random
import requests

st.set_page_config(
    page_title="Database Debugger",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Database Debugger - Detailed Diagnostics")
st.markdown("This tool helps identify why database saves are failing.")

# Try to import the database module
try:
    from database.supabase_manager import SupabaseManager
    st.success("✅ Successfully imported SupabaseManager")
    
    # Initialize database
    with st.spinner("Connecting to database..."):
        db = SupabaseManager()
    
    st.write(f"**Connection Status:** {'✅ Connected' if db.is_connected else '❌ Not Connected'}")
    st.write(f"**Database URL:** {db.url}")
    
    if db.is_connected:
        st.success("🎉 Database connection successful!")
        
        # Test the save_student_profile method with detailed logging
        st.subheader("🔍 Detailed save_student_profile Debug")
        
        # Create test data
        test_email = f"test_{random.randint(1000, 9999)}@debug.com"
        test_student = {
            "full_name": "Debug Test Student",
            "email": test_email,
            "roll_number": f"DEBUG{random.randint(1000, 9999)}",
            "department": "Computer Science",
            "cgpa": 8.5,
            "backlogs": 0,
            "college_id": "TEST001",
            "created_at": datetime.now().isoformat()
        }
        
        st.write("**Test Data:**")
        st.json(test_student)
        
        if st.button("🔬 Run Detailed Debug", type="primary"):
            with st.spinner("Running detailed diagnostics..."):
                
                # Create a detailed debug version
                def debug_save_student_profile_detailed(db, student_data):
                    """Detailed debug version of save_student_profile"""
                    st.write("### Step 1: Checking database connection")
                    st.write(f"- is_connected: {db.is_connected}")
                    st.write(f"- client exists: {db.client is not None}")
                    
                    if not db.is_connected or not db.client:
                        st.error("❌ Database not properly connected")
                        return False
                    
                    st.write("### Step 2: Checking if 'students' table exists")
                    try:
                        # Try to query the table
                        response = db.client.table('students').select('count').execute()
                        st.write(f"- Table query response: {response}")
                        st.success("✅ Students table exists and is accessible")
                    except Exception as e:
                        st.error(f"❌ Cannot access students table: {str(e)}")
                        
                        # Try to create the table via API
                        st.write("### Step 3: Attempting to create table via API")
                        try:
                            create_table_sql = """
                            CREATE TABLE IF NOT EXISTS students (
                                id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
                                full_name TEXT NOT NULL,
                                email TEXT UNIQUE NOT NULL,
                                phone TEXT,
                                college_id TEXT,
                                roll_number TEXT NOT NULL,
                                department TEXT,
                                year TEXT,
                                cgpa DECIMAL(3,2),
                                backlogs INTEGER DEFAULT 0,
                                skills TEXT[],
                                resume_url TEXT,
                                profile_picture_url TEXT,
                                portfolio_link TEXT,
                                linkedin_profile TEXT,
                                github_profile TEXT,
                                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                            );
                            """
                            
                            # Try to execute SQL
                            sql_url = f"{db.url}/rest/v1/rpc/exec_sql"
                            headers = {
                                "apikey": db.key,
                                "Authorization": f"Bearer {db.key}",
                                "Content-Type": "application/json"
                            }
                            
                            sql_response = requests.post(sql_url, 
                                                         json={"query": create_table_sql}, 
                                                         headers=headers)
                            st.write(f"- Create table response: {sql_response.status_code}")
                            st.write(f"- Response text: {sql_response.text[:200]}")
                            
                        except Exception as sql_error:
                            st.error(f"❌ Cannot create table: {sql_error}")
                        
                        return False
                    
                    st.write("### Step 4: Checking RLS (Row Level Security) policies")
                    try:
                        # Try a simple insert with minimal data
                        minimal_data = {
                            "full_name": "Minimal Test",
                            "email": f"minimal{random.randint(1000, 9999)}@test.com",
                            "roll_number": f"MIN{random.randint(1000, 9999)}"
                        }
                        
                        st.write(f"- Testing with minimal data: {minimal_data}")
                        test_result = db.client.table('students').insert(minimal_data).execute()
                        
                        if test_result.data:
                            st.success(f"✅ Minimal insert successful! ID: {test_result.data[0].get('id')}")
                            
                            # Clean up
                            if 'id' in test_result.data[0]:
                                db.client.table('students').delete().eq('id', test_result.data[0]['id']).execute()
                                st.info("✅ Test data cleaned up")
                            
                            # Now try with full data
                            st.write("### Step 5: Testing with full data")
                            try:
                                full_result = db.client.table('students').insert(student_data).execute()
                                if full_result.data:
                                    st.success(f"✅ Full insert successful! ID: {full_result.data[0].get('id')}")
                                    return True
                                else:
                                    st.error("❌ Full insert returned no data")
                                    return False
                            except Exception as full_error:
                                st.error(f"❌ Full insert error: {str(full_error)}")
                                
                                # Check for specific column errors
                                if "column" in str(full_error).lower():
                                    st.error("⚠️ Column error detected. Checking table schema...")
                                    
                                    # Get table info
                                    try:
                                        info_response = requests.get(
                                            f"{db.url}/rest/v1/students",
                                            headers={
                                                "apikey": db.key,
                                                "Authorization": f"Bearer {db.key}",
                                                "Accept": "application/vnd.pgrst.object+json"
                                            }
                                        )
                                        st.write(f"- Table info: {info_response.text[:500]}")
                                    except:
                                        pass
                                
                                return False
                        else:
                            st.error("❌ Minimal insert failed - no data returned")
                            return False
                            
                    except Exception as insert_error:
                        st.error(f"❌ Insert test error: {str(insert_error)}")
                        
                        # Check for permission errors
                        if "permission" in str(insert_error).lower() or "policy" in str(insert_error).lower():
                            st.error("⚠️ RLS (Row Level Security) policy issue detected!")
                            st.markdown("""
                            **RLS Fix Instructions:**
                            
                            1. Go to your Supabase dashboard
                            2. Select your project
                            3. Go to **Authentication → Policies**
                            4. For the `students` table:
                               - Click **New Policy**
                               - Name: `Allow all operations`
                               - Using expression: `true`
                               - For: `ALL`
                               - With check: `true`
                            5. Save the policy
                            
                            Or run this SQL in Supabase SQL Editor:
                            ```sql
                            -- Disable RLS temporarily
                            ALTER TABLE students DISABLE ROW LEVEL SECURITY;
                            
                            -- Or create permissive policy
                            CREATE POLICY "Allow all operations" ON students
                                FOR ALL USING (true);
                            ```
                            """)
                        
                        return False
                    
                    return False
                
                # Run the detailed debug
                success = debug_save_student_profile_detailed(db, test_student)
                
                if success:
                    st.success("🎉 SUCCESS! The database save should work now.")
                else:
                    st.error("❌ FAILED. Check the error details above.")
        
        # Direct API Test
        st.subheader("🌐 Direct API Test (Bypassing Python Client)")
        
        test_email2 = f"direct{random.randint(1000, 9999)}@api.com"
        test_data = {
            "full_name": "Direct API Test",
            "email": test_email2,
            "roll_number": f"API{random.randint(1000, 9999)}",
            "department": "Test"
        }
        
        st.write("**Test Data for Direct API:**")
        st.json(test_data)
        
        if st.button("Test Direct REST API"):
            url = f"{db.url}/rest/v1/students"
            headers = {
                "apikey": db.key,
                "Authorization": f"Bearer {db.key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation,resolution=merge-duplicates"
            }
            
            st.write(f"**Request URL:** `POST {url}`")
            st.write(f"**Headers:**")
            st.json(headers)
            st.write(f"**Body:**")
            st.json(test_data)
            
            try:
                response = requests.post(url, json=test_data, headers=headers)
                
                st.write(f"**Response Status:** `{response.status_code}`")
                st.write(f"**Response Headers:**")
                st.json(dict(response.headers))
                st.write(f"**Response Body (first 500 chars):**")
                st.text(response.text[:500])
                
                if response.status_code in [200, 201]:
                    st.success("✅ Direct API call successful!")
                    try:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            st.json(result[0])
                        else:
                            st.json(result)
                    except:
                        st.text(response.text)
                elif response.status_code == 409:
                    st.error("❌ 409 Conflict - Email might already exist")
                elif response.status_code == 401:
                    st.error("❌ 401 Unauthorized - Check your API key")
                elif response.status_code == 404:
                    st.error("❌ 404 Not Found - Table might not exist")
                elif response.status_code == 425:
                    st.error("❌ 425 RLS violation - Check Row Level Security policies")
                else:
                    st.error(f"❌ API call failed with status {response.status_code}")
                    
            except Exception as e:
                st.error(f"❌ API call exception: {str(e)}")
        
        # Check existing data
        st.subheader("📋 Check Existing Students")
        
        if st.button("List existing students"):
            try:
                students = db.get_students()
                st.write(f"**Found {len(students)} students:**")
                
                if students:
                    # Create dataframe
                    df = pd.DataFrame(students)
                    
                    # Show column info
                    st.write("**Columns in students table:**")
                    st.write(list(df.columns))
                    
                    # Show data
                    st.dataframe(df.head(10))
                    
                    # Show sample record
                    with st.expander("View first record in detail"):
                        st.json(students[0])
                else:
                    st.info("No students found in database")
                    
            except Exception as e:
                st.error(f"❌ Error fetching students: {str(e)}")
    
    else:
        st.error("❌ Cannot connect to database")
        
        # Show troubleshooting
        st.subheader("🔧 Connection Troubleshooting")
        
        # Try direct connection test
        if st.button("Test Direct Connection"):
            try:
                test_url = "https://ptnozudvgcqhnmidjoqj.supabase.co/rest/v1/"
                headers = {
                    "apikey": db.key,
                    "Authorization": f"Bearer {db.key}"
                }
                
                response = requests.get(test_url, headers=headers)
                st.write(f"Direct test status: {response.status_code}")
                st.write(f"Response: {response.text[:200]}")
            except Exception as e:
                st.error(f"Direct test failed: {e}")
        
except ImportError as e:
    st.error(f"❌ Cannot import SupabaseManager: {str(e)}")
    st.code(traceback.format_exc())
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
    st.code(traceback.format_exc())

# Quick fix instructions
st.divider()
st.subheader("🚀 Quick Fix Options")

st.markdown("""
### Option 1: Create Table via Supabase Dashboard
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to **Table Editor**
4. Click **Create a new table**
5. Name: `students`
6. Add columns:
   - `id` (uuid, primary key, default: `gen_random_uuid()`)
   - `full_name` (text, not null)
   - `email` (text, unique, not null)
   - `roll_number` (text, not null)
   - `department` (text)
   - `cgpa` (numeric)
   - `backlogs` (integer)
   - `created_at` (timestamp, default: `now()`)
7. Save table

### Option 2: Run SQL in Supabase SQL Editor
```sql
-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    college_id TEXT,
    roll_number TEXT NOT NULL,
    department TEXT,
    year TEXT,
    cgpa DECIMAL(3,2),
    backlogs INTEGER DEFAULT 0,
    skills TEXT[],
    resume_url TEXT,
    profile_picture_url TEXT,
    portfolio_link TEXT,
    linkedin_profile TEXT,
    github_profile TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Disable RLS for testing
ALTER TABLE students DISABLE ROW LEVEL SECURITY;

-- Or create permissive policy
CREATE POLICY "Enable all operations" ON students
    FOR ALL USING (true);
