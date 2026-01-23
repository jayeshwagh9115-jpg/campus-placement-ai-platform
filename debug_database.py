import streamlit as st
import pandas as pd
import json
import traceback
from datetime import datetime
import random

st.set_page_config(
    page_title="Database Debugger",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Database Debugger")
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
        
        # Test 1: Check tables
        st.subheader("📊 Table Check")
        
        tables_to_check = ['students', 'companies', 'job_postings', 'applications', 'colleges']
        
        table_status = []
        for table in tables_to_check:
            try:
                # Try to select from table
                data = db.select(table, limit=1)
                table_status.append({
                    'Table': table,
                    'Status': '✅ Accessible',
                    'Records': len(data),
                    'Sample': data[0] if data else None
                })
            except Exception as e:
                table_status.append({
                    'Table': table,
                    'Status': f'❌ Error: {str(e)[:100]}',
                    'Records': 0,
                    'Sample': None
                })
        
        # Display table status
        df_status = pd.DataFrame(table_status)
        st.dataframe(df_status[['Table', 'Status', 'Records']], use_container_width=True)
        
        # Show sample data for accessible tables
        for status in table_status:
            if status['Sample']:
                with st.expander(f"Sample from {status['Table']}"):
                    st.json(status['Sample'])
        
        # Test 2: Try to save a test student
        st.subheader("💾 Test Student Save")
        
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
        
        st.write("**Test Data to Save:**")
        st.json(test_student)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Test save_student_profile method", type="primary"):
                with st.spinner("Testing save_student_profile..."):
                    try:
                        result = db.save_student_profile(test_student)
                        if result:
                            st.success("✅ save_student_profile SUCCESS!")
                            
                            # Verify it was saved
                            saved = db.get_student_profile(test_email)
                            if saved:
                                st.success(f"✅ Verified! Student ID: {saved.get('id', 'N/A')}")
                                st.json(saved)
                            else:
                                st.warning("⚠️ Saved but cannot retrieve")
                        else:
                            st.error("❌ save_student_profile FAILED")
                    except Exception as e:
                        st.error(f"❌ Exception: {str(e)}")
                        st.code(traceback.format_exc())
        
        with col2:
            if st.button("🔍 Test insert method"):
                with st.spinner("Testing direct insert..."):
                    try:
                        result = db.insert('students', test_student)
                        if result:
                            st.success(f"✅ Direct insert SUCCESS! ID: {result.get('id', 'N/A')}")
                            st.json(result)
                        else:
                            st.error("❌ Direct insert FAILED - No result returned")
                    except Exception as e:
                        st.error(f"❌ Exception: {str(e)}")
        
        with col3:
            if st.button("🔍 Test upsert method"):
                with st.spinner("Testing upsert..."):
                    try:
                        result = db.upsert('students', test_student, on_conflict='email')
                        if result:
                            st.success(f"✅ Upsert SUCCESS! ID: {result.get('id', 'N/A')}")
                            st.json(result)
                        else:
                            st.error("❌ Upsert FAILED - No result returned")
                    except Exception as e:
                        st.error(f"❌ Exception: {str(e)}")
        
        # Test 3: Raw SQL check
        st.subheader("⚙️ Database Schema Check")
        
        if st.button("Check students table schema"):
            try:
                # Try to get column information
                test_student = {
                    "full_name": "Schema Test",
                    "email": f"schema{random.randint(1000, 9999)}@test.com",
                    "roll_number": "SCHEMA001"
                }
                
                result = db.insert('students', test_student)
                if result:
                    st.success("✅ Can insert minimal data")
                    st.json(result)
                    
                    # Clean up
                    if 'id' in result:
                        db.delete('students', result['id'])
                        st.info("✅ Test data cleaned up")
                else:
                    st.error("❌ Cannot insert even minimal data")
                    
            except Exception as e:
                st.error(f"❌ Schema error: {str(e)}")
        
        # Test 4: Network request test
        st.subheader("🌐 Network Test")
        
        if st.button("Test direct API call"):
            import requests
            
            url = f"{db.url}/rest/v1/students"
            headers = {
                "apikey": db.key,
                "Authorization": f"Bearer {db.key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            test_data = {
                "full_name": "API Test Student",
                "email": f"api{random.randint(1000, 9999)}@test.com",
                "roll_number": f"API{random.randint(1000, 9999)}"
            }
            
            st.write(f"**URL:** `{url}`")
            st.write(f"**Headers:** `{json.dumps(headers, indent=2)}`")
            st.write(f"**Data:** `{json.dumps(test_data, indent=2)}`")
            
            try:
                response = requests.post(url, json=test_data, headers=headers)
                st.write(f"**Status Code:** {response.status_code}")
                st.write(f"**Response:** {response.text[:500]}")
                
                if response.status_code in [200, 201]:
                    st.success("✅ Direct API call successful!")
                    result = response.json()
                    if result and len(result) > 0:
                        st.json(result[0])
                else:
                    st.error(f"❌ API call failed: {response.status_code}")
            except Exception as e:
                st.error(f"❌ API call exception: {str(e)}")
        
        # Test 5: Clean up all test data
        st.subheader("🧹 Cleanup")
        
        if st.button("Clean up all test data"):
            try:
                # Get all test students
                test_students = db.select('students', {'email': {'like': '%@debug.com%'}})
                test_students.extend(db.select('students', {'email': {'like': '%@test.com%'}}))
                test_students.extend(db.select('students', {'roll_number': {'like': '%DEBUG%'}}))
                test_students.extend(db.select('students', {'roll_number': {'like': '%TEST%'}}))
                test_students.extend(db.select('students', {'roll_number': {'like': '%API%'}}))
                test_students.extend(db.select('students', {'roll_number': {'like': '%SCHEMA%'}}))
                
                deleted_count = 0
                for student in test_students:
                    if 'id' in student:
                        db.delete('students', student['id'])
                        deleted_count += 1
                
                st.success(f"✅ Cleaned up {deleted_count} test records")
            except Exception as e:
                st.error(f"❌ Cleanup error: {str(e)}")
    
    else:
        st.error("❌ Cannot connect to database")
        
        # Show troubleshooting tips
        st.subheader("🔧 Troubleshooting Tips")
        
        st.markdown("""
        1. **Check your Supabase credentials** in `supabase_manager.py`
        2. **Verify your Supabase project is active** at [Supabase Dashboard](https://app.supabase.com)
        3. **Check internet connection**
        4. **Try visiting your Supabase URL directly**: 
           - https://ptnozudvgcqhnmidjoqj.supabase.co
        5. **Check if you need to create tables**:
           ```sql
           -- Run this in Supabase SQL Editor
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
           ```
        6. **Disable RLS (Row Level Security) temporarily**:
           ```sql
           -- In Supabase SQL Editor
           ALTER TABLE students DISABLE ROW LEVEL SECURITY;
           
           -- Or create permissive policies
           CREATE POLICY "Allow all operations" ON students
               FOR ALL USING (true);
           ```
        """)
        
except ImportError as e:
    st.error(f"❌ Cannot import SupabaseManager: {str(e)}")
    st.code(traceback.format_exc())
except Exception as e:
    st.error(f"❌ Unexpected error: {str(e)}")
    st.code(traceback.format_exc())

# Footer
st.divider()
st.markdown("**Run this debugger to identify the exact database issue.**")
