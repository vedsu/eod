import streamlit as st
import pymongo
import time
import admin.home as home
import admin.hr as hr


if 'user' not in st.session_state:
    st.session_state.user = None

# Database Connections
@st.cache_resource

def init_connection():
    try:
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password
        
        mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)
        client = pymongo.MongoClient(mongo_uri)
        return client
    
    except Exception as e:
    
        st.error(f"Connection failure:{str(e)}")
# Database Collections

client = init_connection()
db = client["vybe"]
collection = db["eod"]

admin_username = st.secrets.admin_username
admin_passwords = st.secrets.admin_passwords
hr_username = st.secrets.hr_username
hr_passwords = st.secrets.hr_passwords

if st.session_state.user and st.session_state.access == 'admin':
    home.main()
elif st.session_state.user and st.session_state.access == "hr":
    hr.main()

else:
# def main():
    with st.form(key="auth_form",clear_on_submit=True):
            st.subheader("Admin/HR Login")
            user = st.text_input("Username :")
            password = st.text_input("Password :", type="password")
            login_button = st.form_submit_button(label = "Login")
            
            if login_button:
                
                if user == admin_username and password == admin_passwords:
                        st.session_state.user = user
                        st.session_state.access = 'admin'
                        st.rerun()
                elif user == hr_username and password == hr_passwords:
                     st.session_state.user = user
                     st.session_state.access = 'hr'
                     st.rerun()
                else:
                    st.error("Invalid credentials! user not authorized try again!")
