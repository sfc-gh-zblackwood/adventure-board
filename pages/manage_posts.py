import streamlit as st

st.set_page_config(
    page_title="Manage Posts - Adventure Board"
)

import sqlite3
from db import get_connection, side_bar, convert_date, convert_time
import time
import datetime

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.switch_page("startup.py")

if "current_post" not in st.session_state:
    st.session_state.current_post = 1

side_bar()

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts WHERE creator = ?", (st.session_state.current_user,))
    events = cursor.fetchall()
    for x in events:
        with st.container(border=True):
            ID, title, start_date, end_date, start_time, end_time, location_name, location_link, details, creator = [y for y in x]
            sd = convert_date(start_date)
            ed = convert_date(end_date)
            strt = convert_time(start_time)
            et = convert_time(end_time)
            cursor.execute("SELECT name FROM Accounts WHERE username = ?", (st.session_state.current_user,))
            user_exists = cursor.fetchone()
            creator_name = user_exists[0]
            st.write(ID)
            st.subheader(f"{title}")
            st.write(f"{sd} {strt} - {ed} {et}")
            st.write(f"[{location_name}]({location_link})")
            st.write(f"Created by {creator} ({creator_name})")
            st.write(details)
            col1, col2 = st.columns(2)
            with col1:
                edit = st.button("Edit", key=f"edit_{ID}")
                if edit:
                    st.session_state.current_post = ID
                    st.switch_page("pages/edit_post.py")
            with col2:
                delete = st.button("Delete", key=f"delete_{ID}")
                if delete:
                    cursor.execute("DELETE FROM Posts WHERE id = ?", (ID,))
                    conn.commit()
