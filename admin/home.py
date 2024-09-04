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
        week_start = current_date - datetime.timedelta(days=current_date.weekday())  # recent Monday
        week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
        current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

        #dataframe to include the week range
        filtered_df = df[(df['name'].isin(name_filter)) & (df['date'].between(week_start, current_date_normalized))]
        #reset the index
        filtered_df.reset_index(drop=True, inplace=True)
    elif report_type == 'Monthly':
        #first day of the current month
        month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
        current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

        #dataframe to include the month range
        filtered_df = df[(df['name'].isin(name_filter)) & (df['date'].between(month_start, current_date_normalized))]

        #reset the index.
        filtered_df.reset_index(drop=True, inplace=True) 
        
        
        
    st.dataframe(filtered_df)
    filename = f"eod_{current_date.date()}.csv"
    st.download_button(
                    label="download eod!",
                    data=filtered_df.to_csv().encode(),
                    file_name= filename,
                    mime="text/csv" )
    
    
    
