import streamlit as st
import admin.auth as admin_login
import employee.login as employee_login
import employee.register as employee_register

if 'user' not in st.session_state:
    st.session_state.user = None
if 'access' not in st.session_state:
    st.session_state.access = "member_login"
if 'name' not in st.session_state:
    st.session_state.name = None
if 'default' not in st.session_state:
    st.session_state.default = None



if st.session_state.default:
    employee_login = st.Page("employee/login.py", title = "Member Login", icon=":material/history:",  default=True)
    employee_register = st.Page("employee/register.py", title = "Member Register", icon=":material/notification_important:")
    admin_login = st.Page("admin/auth.py", title = "Admin Login", icon = ":material/login:")

    pg = st.navigation(
        {
        "Admin":[admin_login],
        "Team":[employee_login, employee_register]
    }
    )

    pg.run()
else:    
    
    # URL of the image
    image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/letsVybe.webp"

    # Display the image
    st.image(image_url, caption="Let's Vybe", use_column_width=True)
    st.markdown("""
    <style>
    div.stButton > button {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)
    if st.button("click to Vybe!"):
        st.session_state.default = True
        st.rerun()