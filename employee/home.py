import streamlit as st
import pymongo
import datetime
import time


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

def main():
    
    st.subheader("End of Day Report")
    icon_dict = {
                    "Jacob":"🐯",
                    "RISHIKA RICHA":"🐱",
                    "Aman ":"🧞‍♂️",
                    "Priya Kumari":"🦋",
                    "Nitin Yadav":"🦹‍♂️",
                    
                    "Shubham":"🧑‍💻"}
    
    name = st.session_state.name
    icon = icon_dict.get(name)
    email = st.session_state.user
    tab1, tab2= st.columns(2)
    with tab1:
        st.info(f"Hello, {name}!", icon=icon)
    with tab2:
        st.info(email)

    
    if st.session_state.user and st.session_state.access == 'team':
        with st.form("EOD Form",clear_on_submit=True):
            
            st.subheader("EOD Form")
            date = st.date_input("Date :") 
            date_as_datetime = datetime.datetime.combine(date, datetime.datetime.min.time())
            eod = st.text_area("EOD Report* :",placeholder='provide your eod report here')
            meeting = st.checkbox("Meetings(*if any) ")
            comment = st.text_area("Comments(*if any)")
            login_button = st.form_submit_button(label = "Submit")

            if login_button:
                if eod:
                    try:
                        collection.insert_one({"name":name, "date":date_as_datetime, "eod": eod, "meeting":meeting, "comment":comment})
                        st.success("eod submission successful!")
                        time.sleep(5)
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.warning("no eod to submit!")
                    st.rerun()

