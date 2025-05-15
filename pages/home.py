import streamlit as st

st.set_page_config(
    page_title="Adventure Board"
)

import sqlite3
from db import get_connection
import time
import datetime

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.switch_page("startup.py")

def convert_date(date):
    year, month, day = [int(x) for x in date.split("-")]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[month - 1]} {day}, {year}"

def convert_time(time):
    hour, minute = [x for x in time.split(":")]
    hour = int(hour)
    am_pm = "a.m."
    if hour >= 12:
        hour -= 12
        am_pm = "p.m."
    return f"{hour}:{minute} {am_pm}"

st.write(f"Welcome, {st.session_state.current_user}")

sb = st.sidebar
home = sb.page_link("pages/home.py", label="Home")
profile = sb.page_link("pages/profile.py", label="Profile")
log_out = sb.button("Log out")

if log_out:
    st.session_state.current_user = None
    with st.spinner("Logging out..."):
        time.sleep(5)
    st.switch_page("startup.py")

createpost = st.button("Create post", key="post_creator")

# display posts using a SELECT FROM query for now
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts")
    conn.commit()
    events = cursor.fetchall()
    if not events:
        st.write("No events yet. Why don't you create one?")
    else:
        for x in events:
            with st.container(border=True):
                title, start_date, end_date, start_time, end_time, location_name, location_link, details, creator = [y for y in x]
                sd = convert_date(start_date)
                ed = convert_date(end_date)
                strt = convert_time(start_time)
                et = convert_time(end_time)
                cursor.execute("SELECT * FROM Accounts WHERE username = ?", (creator,))
                user_exists = cursor.fetchone()
                creator_name = "ACCOUNT DELETED"
                if user_exists:
                    creator_name = user_exists[0]
                st.markdown(f"**{title}**")
                st.write(f"{sd} {strt} - {ed} {et}")
                st.write(f"Created by {creator} ({creator_name})")
                st.write(details)



if createpost:
    st.switch_page("pages/create_post.py")