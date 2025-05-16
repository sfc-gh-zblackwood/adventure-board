import streamlit as st

st.set_page_config(
    page_title="Create new post - Adventure Board"
)

import sqlite3
from db import get_connection, side_bar, is_empty
from time import sleep
import validators
from datetime import datetime

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.switch_page("startup.py")

side_bar()

post_form = st.form(key="post")
title = post_form.text_input("Title", max_chars=50)
start_date = post_form.date_input("Start date")
end_date = post_form.date_input("End date")
start_time = post_form.time_input("Start time")
end_time = post_form.time_input("End time")
location_name = post_form.text_input("Location Name", max_chars=50)
location_link = post_form.text_input("Location Link (Google Maps, Waze, etc.)")
details = post_form.text_area("Details", max_chars=500)
create = post_form.form_submit_button("Post event!")
if create:
    if is_empty(title):
        st.error("You need a title. What's your event called?")
    elif start_date > end_date:
        st.error("Your start date comes after your end date. Are you a time traveler?")
    elif start_date == end_date and start_time > end_time:
        st.error("Your start time comes after your end time. Are you a time traveler?")
    elif end_date < datetime.now().date():
        st.warning("Your event ends before today.")
    elif is_empty(location_name):
        st.warning("You need a location name. What's the location name?")
    elif is_empty(location_link) or (not validators.url(location_link)):
        st.warning("You need a valid link for your location. Where is your location?")
    elif is_empty(details):
        st.warning("You need details for your event. What is your event about?")
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Posts (title, start_date, end_date, start_time, end_time, location_name, location_link, details, creator) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                           (title,
                            str(start_date),
                            str(end_date),
                            str(start_time)[:5],
                            str(end_time)[:5],
                            location_name,
                            location_link,
                            details,
                            st.session_state.current_user))
            conn.commit()
            st.success("Post created!")
            with st.spinner("Redirecting to home page..."):
                sleep(3)
            st.switch_page("pages/home.py")