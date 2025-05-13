import streamlit as st
import sqlite3
from db import get_connection
import config
import time

def create_post():
    post_form = st.form(key="post")
    title = post_form.text_input("Title", max_chars=50)
    location_name = post_form.text_input("Location Name", max_chars=50)
    location_link = post_form.text_input("Location Link (Google Maps, Waze, etc.)")
    create = post_form.form_submit_button("Create Post")
    if create:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Posts VALUES (?, ?, ?, ?)", (title, location_name, location_link, config.current_user))
            conn.commit()
            st.success("Post created!")

st.write(f"Welcome, {config.current_user}")

sb = st.sidebar
profile = sb.page_link("startup.py", label="Profile")
log_out = sb.button("Log out")
if log_out:
    config.current_user = None
    with st.spinner("Logging out..."):
        time.sleep(5)
    st.switch_page("startup.py")

# display posts as a table for now using a SELECT FROM query