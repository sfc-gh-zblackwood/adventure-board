import streamlit as st

st.set_page_config(
    page_title="Adventure Board"
)

import sqlite3
from db import get_connection, side_bar, convert_date, convert_time
import time
from datetime import datetime

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.switch_page("startup.py")

st.write(f"Welcome, {st.session_state.current_user}!")

side_bar()

createpost = st.button("Create post", key="post_creator")

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts")
    events = cursor.fetchall()
    if not events:
        st.write("No events yet. Why don't you create one?")
    else:
        for x in events:
            with st.container(border=True):
                ID, title, start_date, end_date, start_time, end_time, location_name, location_link, details, creator = [y for y in x]
                ed_object = datetime.strptime(end_date, "%Y-%m-%d").date()
                if ed_object < datetime.now().date():
                    cursor.execute("DELETE FROM Posts WHERE id = ?", (ID,))
                    conn.commit()
                    continue
                sd = convert_date(start_date)
                ed = convert_date(end_date)
                strt = convert_time(start_time)
                et = convert_time(end_time)
                cursor.execute("SELECT name FROM Accounts WHERE username = ?", (creator,))
                user_exists = cursor.fetchone()
                st.write(ID)
                creator_name = "ACCOUNT DELETED"
                if user_exists:
                    creator_name = user_exists[0]
                st.subheader(f"{title}")
                st.write(f"{sd} {strt} - {ed} {et}")
                st.write(f"[{location_name}]({location_link})")
                st.write(f"Created by {creator} ({creator_name})")
                st.write(details)

if createpost:
    st.switch_page("pages/create_post.py")