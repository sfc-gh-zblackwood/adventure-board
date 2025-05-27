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
                with st.expander("Details"):
                    st.write(details)
                with st.expander("Attendees"):
                    cursor.execute("SELECT user_id FROM Signups WHERE post_id = ? AND status = ?", (ID, "approved"))
                    all_attendees = cursor.fetchall()
                    if all_attendees:
                        for attendee in all_attendees:
                            attendee_username = attendee[0]
                            cursor.execute("SELECT name, profile_pic FROM Accounts WHERE username = ?", (attendee_username,))
                            attendee_data = cursor.fetchone()
                            attendee_name, attendee_pic = [x for x in attendee_data]
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.image(attendee_pic, width=50)
                            with col2:
                                st.write(f"{attendee_username} ({attendee_name})")
                    else:
                        st.write("No sign-ups yet. Maybe you can join?")
                col1, col2 = st.columns(2)
                own_event = (creator == st.session_state.current_user)
                with col1:
                    sign_up = st.button("Sign Up", key=f"sign_up_{ID}", disabled=own_event)
                    if sign_up:
                        cursor.execute("INSERT OR IGNORE INTO Signups (user_id, post_id, status) VALUES (?, ?, ?)", (st.session_state.current_user, ID, "pending"))
                        conn.commit()
                        st.info(f"Your sign-up for {title} is pending approval.")
                with col2:
                    leave = st.button("Leave", key=f"leave_{ID}", disabled=own_event)
                    if leave:
                        cursor.execute("DELETE FROM Signups WHERE user_id = ? AND post_id = ?", (st.session_state.current_user, ID))
                        conn.commit()
                        st.info(f"Left {title}.")
                if own_event:
                    st.write("**This is your event!**")