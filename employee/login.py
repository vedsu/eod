import streamlit as st
import pymongo
import time
import employee.home as home

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
collection = db["user"]
if st.session_state.user and st.session_state.access == 'team':
    home.main()
# def main():
else:  
    
        with st.container():
            
            st.subheader("Member Login")
            user = st.text_input("User Email :")
            password = st.text_input("Password :", type="password")
            login_button = st.button(label = "Login")

            if login_button:
                # home.main()
                try:
                    credentials = collection.find_one({"email":user, "password": password})
                    if credentials:
                        st.write(credentials)
                        st.session_state.name = credentials.get("name")
                        st.write(st.session_state.name)
                        st.session_state.user = user
                        st.session_state.access = 'team'
                        st.rerun()
                    else:
                        st.warning("inavlid credentials")
                except Exception as e:
                    st.error(f"Error: {str(e)}")