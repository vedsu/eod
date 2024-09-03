import streamlit as st
import pymongo
import pandas as pd
import datetime

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


client = init_connection()
db = client["vybe"]
collection = db["eod"]


def main():
    st.subheader("EOD Review")
    data = list(collection.find({},{"_id":0}))
    df = pd.DataFrame(data)
    
    # current date
    current_date = datetime.datetime.now()
    # filter by Name
    name_filter = st.sidebar.multiselect('Select Name', options=df['name'].unique(), default=df['name'].unique())
    
    report_type = st.sidebar.radio(
    "Select Report Type",
    ('Daily', 'Weekly', 'Monthly'), index=0  # default selection to "Daily"
    )
    
    # date input based on report type
    if report_type == 'Daily':
        # Filter by Date Range
        start_date = st.sidebar.date_input('eod date')
        # Apply filters to the dataset
        filtered_df = df[(df['name'].isin(name_filter)) & (df['date'] == (pd.to_datetime(start_date)))]
    elif report_type == 'Weekly':
        week_start = current_date - datetime.timedelta(days=current_date.weekday())  # most recent Monday
        # st.sidebar.write(week_start)
        filtered_df = df[(df['name'].isin(name_filter)) & (df['date'].between(week_start, current_date))]
    elif report_type == 'Monthly':
        month_start = current_date.replace(day=1)  #first day of the current month
        # st.sidebar.write(month_start)
        filtered_df = df[(df['name'].isin(name_filter)) & (df['date'].between(month_start, current_date))]   
        
        
        
    st.dataframe(filtered_df)
    
    
    
