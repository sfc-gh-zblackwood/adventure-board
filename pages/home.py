import streamlit as st
import sqlite3
from db import get_connection
import time
import datetime

if st.session_state.current_user is None:
    st.switch_page("startup.py")

st.write(f"Welcome, {st.session_state.current_user}")

sb = st.sidebar
profile = sb.page_link("pages/profile.py", label="Profile")
log_out = sb.button("Log out")

if log_out:
    st.session_state.current_user = None
    with st.spinner("Logging out..."):
        time.sleep(5)
    st.switch_page("startup.py")

createpost = st.button("Create post", key="post_creator")

# display posts as a table for now using a SELECT FROM query
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts")
    conn.commit()
    if not cursor.fetchone():
        st.write("No events yet. Why don't you create one?")
    else:
        for x in cursor.fetchall():
            st.write(x)

if createpost:
    st.switch_page("pages/create_post.py")