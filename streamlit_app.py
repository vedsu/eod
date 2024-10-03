import streamlit as st
st.set_page_config(page_title="Vybe", page_icon="🚗")
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



if st.session_state.default is None :
    
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
    
    # URL of the image
    image_url = "https://vedsubrandwebsite.s3.amazonaws.com/miscellaneous/letsVybe.webp"
    st.markdown(f"""
            <div style='text-align: center;'>
                <img src="{image_url}" style="border-radius: 50%; width:200px; height:200px; margin-top:10px; box-shadow: rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset;">
            </div>
        """, unsafe_allow_html=True)
    # Display the image
    # st.image(image_url, caption="Let's Vybe", use_column_width=True)
    
   
else:    
    employee_login = st.Page("employee/login.py", title = "Member Login", icon="🧑‍💻",  default=True)
    employee_register = st.Page("employee/register.py", title = "Member Register", icon="📝")
    admin_login = st.Page("admin/auth.py", title = "Admin Login", icon = "🧊")

    pg = st.navigation(
        {
        "Admin":[admin_login],
        "Team":[employee_login, employee_register]
    }
    )

    pg.run()
    
    
