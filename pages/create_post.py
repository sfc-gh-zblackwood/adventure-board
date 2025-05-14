import streamlit as st
import sqlite3
from db import get_connection

post_form = st.form(key="post")
title = post_form.text_input("Title", max_chars=50)
date = post_form.date_input("Date")
start_time = post_form.time_input("Start time")
end_time = post_form.time_input("End time")
location_name = post_form.text_input("Location Name", max_chars=50)
location_link = post_form.text_input("Location Link (Google Maps, Waze, etc.)")
create = post_form.form_submit_button("Post event!")
if create:
    if len(title) == 0 or title.isspace():
        st.warning("You need a title")
    else:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Posts VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (title, str(date),
                            str(start_time),
                            str(end_time),
                            location_name,
                            location_link,
                            st.session_state.current_user))
            conn.commit()
            st.success("Post created!")