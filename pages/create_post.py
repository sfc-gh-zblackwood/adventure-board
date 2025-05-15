import streamlit as st

st.set_page_config(
    page_title="Create new post - Adventure Board"
)

import sqlite3
from db import get_connection, side_bar
from time import sleep

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
    if len(title) == 0 or title.isspace():
        st.warning("You need a title")
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