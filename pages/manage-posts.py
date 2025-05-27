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
    if not events:
        st.write("You don't have any posts yet.")
    else:
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
                with st.expander("Details"):
                    st.write(details)
                with st.expander("Attendees"):
                    cursor.execute("SELECT user_id, status FROM Signups WHERE post_id = ?", (ID,))
                    all_attendees = cursor.fetchall()
                    if all_attendees:
                        for attendee in all_attendees:
                            attendee_username = attendee[0]
                            attendee_status = attendee[1]
                            cursor.execute("SELECT name, profile_pic FROM Accounts WHERE username = ?", (attendee_username,))
                            attendee_data = cursor.fetchone()
                            attendee_name, attendee_pic = [x for x in attendee_data]
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.image(attendee_pic, width=50)
                            with col2:
                                if attendee_status == "pending":
                                    st.write(f":orange[{attendee_username} ({attendee_name})]")
                                else:
                                    st.write(f"{attendee_username} ({attendee_name})")
                            with col3:
                                approve_attendee = st.button(":white_check_mark:", key=f"approve_{attendee_username}")
                                if approve_attendee:
                                    cursor.execute("UPDATE Signups SET status = 'approved' WHERE user_id = ? AND post_id = ?", (attendee_username, ID))
                                    conn.commit()
                                    st.rerun()
                            with col4:
                                remove_attendee = st.button(":x:", key=f"remove_{attendee_username}")
                                if remove_attendee:
                                    cursor.execute("DELETE FROM Signups WHERE user_id = ? AND post_id = ?", (attendee_username, ID))
                                    conn.commit()
                                    st.rerun()

                    else:
                        st.write("No sign-ups yet. Maybe you can join?")
                col1, col2 = st.columns(2)
                with col1:
                    edit = st.button("Edit", key=f"edit_{ID}")
                    if edit:
                        st.session_state.current_post = ID
                        st.switch_page("pages/edit-post.py")
                with col2:
                    delete = st.button("Delete", key=f"delete_{ID}")
                    if delete:
                        cursor.execute("DELETE FROM Posts WHERE id = ?", (ID,))
                        conn.commit()
