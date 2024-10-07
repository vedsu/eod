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
collection_eod = db["eod"]
collection_leave = db["leave"]
collection_user = db['user']
st.subheader("Human Resource Management", divider=True)


def main():
    # current date
    current_date = datetime.datetime.now()
    # name_options = list(collection_user.distinct("name"))
    employee = list(collection_user.distinct("name"))

    # filter by Name
    name_filter = st.sidebar.multiselect('Select Name', options=employee, default=employee)
            
    report_type = st.sidebar.radio(
    "Select Report Type",
    ('Daily', 'Weekly', 'Monthly'), index=0, key="leave" # default selection to "Daily"
    )
    # Filter by Date Range
    start_date = st.sidebar.date_input('leave date')
    
    employee_list = ["Select"] + sorted(employee)
    tab1, tab2, tab3 = st.tabs(["🧿 eod tracker","📰 leave tracker","🔊 leave approval" ])
    # st.write(employee)
    with tab3:
        with st.container():
            # employee_selected = st.selectbox(label="select employee", options=employee_list, index=0)
            leaves  = list(collection_leave.find({"$and":[{"name": {"$in":name_filter}}, {"status":"pending"}]}).sort({"start_date":1}))
        
            if leaves:
                for leave in leaves:

                    with st.expander(f"{leave.get("name")} on {leave.get("start_date")}"):
                        st.write(f"type: {leave.get("type")}")
                        st.write(f"leave_days:{leave.get("total_leave")}")
                        status = st.selectbox("action:", options= ["approve", "reject"],key=f"{leave.get("_id")}")
                        action = st.button("submit", key=f"{leave.get("_id")}_button")
                        if action:
                            try:
                                collection_leave.update_one({"_id": leave.get("_id")}, {"$set": {"status":status}})
                                st.success(f"leave {status}!")
                            except :
                                st.error(f"failed to update!")

    with tab2:
        data = list(collection_leave.find({},{"_id":0}))
        df = pd.DataFrame(data)
        # filter by Name
        # name_filter = st.sidebar.multiselect('Select Name', options=df['name'].unique(), default=df['name'].unique())
        
        
        # date input based on report type
        if report_type == 'Daily':
            # Filter by Date Range
            # start_date = st.sidebar.date_input('leave date')
            # Apply filters to the dataset
            filtered_df = df[(df['name'].isin(name_filter)) & ((df['start_date'] == (pd.to_datetime(start_date))) | (df['end_date'] == (pd.to_datetime(start_date))))]
        elif report_type == 'Weekly':
            week_start = current_date - datetime.timedelta(days=current_date.weekday())  # Get the most recent Monday
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
            current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

            # Filter the dataframe to include the week range
            filtered_df = df[(df['name'].isin(name_filter)) & (df['start_date'].between(week_start, current_date_normalized))]
        elif report_type == 'Monthly':
           # Get the first day of the current month
            month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
            current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

            # Filter the dataframe to include the month range
            filtered_df = df[(df['name'].isin(name_filter)) & (df['start_date'].between(month_start, current_date_normalized))]

            # Reset the index to start from 0, 1, 2, etc.
            filtered_df.reset_index(drop=True, inplace=True)
            
            
            
        st.dataframe(filtered_df)
    with tab1:
        data_eod = list(collection_eod.find({},{"_id":0}))
        df_eod = pd.DataFrame(data_eod)
        
        # # current date
        # current_date = datetime.datetime.now()
        # # filter by Name
        # name_filter = st.sidebar.multiselect('Select Name', options=df_eod['name'].unique(), default=df_eod['name'].unique())
        
        # report_type = st.sidebar.radio(
        # "Select Report Type",
        # ('Daily', 'Weekly', 'Monthly'), index=0, key="eod"  # default selection to "Daily"
        # )
        
        # date input based on report type
        if report_type == 'Daily':
            # Filter by Date Range
            # start_date = st.sidebar.date_input('eod date')
            # Apply filters to the dataset
            filtered_df_eod = df_eod[(df_eod['name'].isin(name_filter)) & (df_eod['date'] == (pd.to_datetime(start_date)))]
        elif report_type == 'Weekly':
            week_start = current_date - datetime.timedelta(days=current_date.weekday())  # Get the most recent Monday
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
            current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

            # Filter the dataframe to include the week range
            filtered_df_eod = df_eod[(df_eod['name'].isin(name_filter)) & (df_eod['date'].between(week_start, current_date_normalized))]
        elif report_type == 'Monthly':
        # Get the first day of the current month
            month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Normalize to midnight
            current_date_normalized = current_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Normalize current date

            # Filter the dataframe to include the month range
            filtered_df_eod = df_eod[(df['name'].isin(name_filter)) & (df_eod['date'].between(month_start, current_date_normalized))]

            # Reset the index to start from 0, 1, 2, etc.
            filtered_df_eod.reset_index(drop=True, inplace=True)
            
            
            
        st.dataframe(filtered_df_eod)
        
    
    
