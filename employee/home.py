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
    
    st.subheader("reporting system", divider=True)
    icon_dict = {"Madhan":"👀",
                    "Jacob":"🐯",
                    "RISHIKA RICHA":"🐱",
                    "Aman ":"🧞‍♂️",
                    "Priya Kumari":"🦋",
                    "Nitin Yadav":"🦹‍♂️",
                    
                    "Shubham":"🧑‍💻"}
    
    name = st.session_state.name
    icon = icon_dict.get(name)
    email = st.session_state.user
    col1, col2 = st.columns(2)
    tab1, tab2, = st.tabs(["🧿 eod reporting","🔊 leave request",])
    with col1:
        st.info(f"Hello, {name}!", icon=icon)
    with col2:
        st.info(email)

    with tab1:
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
    with tab2:
        with st.form("leave", clear_on_submit=True):
            st.subheader("leave form", divider=True)
            # employee_selected = st.selectbox(label="select employee", options=employee_list, index=0)
            date_start = st.date_input(label= "starting date:", key="start_date")
            date_start_datetime = datetime.datetime.combine(date_start, datetime.datetime.min.time())
            type = st.radio(label="check leave:", options=("half-day","full-day", "mutli-day"))
            # if type == "mutli-day":
            date_end = st.date_input(label = "end date(*for multi-day leave):", key="end_date")
            
            reason = st.text_input(label= "stated reason for leave:")
            if st.form_submit_button(label = "Request"):
                # if employee_selected != "Select":
                    if type == "half-day":
                        total_leave = 0.5
                        date_end_datetime = date_start_datetime
                    elif type == "full-day":
                        total_leave = 1
                        date_end_datetime = date_start_datetime
                    else:
                        total_leave = (date_end - date_start).days + 1
                        date_end_datetime = datetime.datetime.combine(date_end, datetime.datetime.min.time())
                    try:
                    
                        
                        collection_leave.insert_one({
                            "name": st.session_state.name,
                            "start_date": date_start_datetime,
                            "end_date": date_end_datetime,
                            "type":type,
                            "total_leave": total_leave,
                            "reason": reason,
                            "status":"pending"
                        })
                        st.success("request sent")
                        
                    except Exception as e:
                        st.error(f"Failed to send request: {e}")
        

