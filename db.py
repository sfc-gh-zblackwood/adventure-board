import streamlit as st
import sqlite3
from time import sleep

if "current_user" not in st.session_state:
    st.session_state.current_user = None

def get_connection():
    return sqlite3.connect("app_data.db")

def side_bar():
    sb = st.sidebar
    home = sb.page_link("pages/home.py", label="Home")
    profile = sb.page_link("pages/profile.py", label="Profile")
    manage_posts = sb.page_link("pages/manage_posts.py", label="Manage Posts")
    log_out = sb.button("Log out")
    if log_out:
        st.session_state.current_user = None
        st.logout
        with st.spinner("Logging out..."):
            sleep(5)
        st.switch_page("startup.py")

def convert_date(date):
    year, month, day = [int(x) for x in date.split("-")]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[month - 1]} {day}, {year}"

def convert_time(time):
    hour, minute = [x for x in time.split(":")]
    hour = int(hour)
    am_pm = "a.m."
    if hour > 12:
        hour -= 12
        am_pm = "p.m."
    elif hour == 12:
        am_pm = "p.m."
    elif hour == 0:
        hour = 12
    return f"{hour}:{minute} {am_pm}"

def is_empty(widget):
    return widget is None or len(widget) == 0 or widget.isspace()