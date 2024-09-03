import streamlit as st
import pymongo
import time


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

# def main():

with st.form("register",clear_on_submit=True):
        
        st.subheader("Member Registration")
        name = st.text_input("Name : ")
        useremail = st.text_input("User Email :")
        password = st.text_input("Password :", type="password")
        confirm_password = st.text_input("Confirm Password :", type="password")
        login_button = st.form_submit_button(label = "Register")

        if login_button:
            if password == confirm_password:
                try:
                    collection.insert_one({"name":name,"email":useremail,"password":password})
                    st.success("registration successful, please login to continue..")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                    st.warning("password mismatch")
                
            