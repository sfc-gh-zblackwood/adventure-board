import streamlit as st

st.set_page_config(
    page_title="Edit Post - Adventure Board"
)

from db import get_connection, side_bar, convert_date, convert_time, is_empty

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if st.session_state.current_user is None:
    st.switch_page("startup.py")

from datetime import datetime
import validators
from time import sleep
 
if "current_post" not in st.session_state:
    st.session_state.current_post = 1

side_bar()

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts WHERE id = ?", (st.session_state.current_post,))
    x = cursor.fetchone()
    ID, title, start_date, end_date, start_time, end_time, location_name, location_link, details, creator = [y for y in x]
    sd = datetime.strptime(start_date, "%Y-%m-%d").date()
    ed = datetime.strptime(end_date, "%Y-%m-%d").date()
    strt = datetime.strptime(start_time, "%H:%M").time()
    et = datetime.strptime(end_time, "%H:%M").time()

    post_form = st.form(key="post")
    new_title = post_form.text_input("Title", max_chars=50, value=title)
    new_start_date = post_form.date_input("Start date", value=sd)
    new_end_date = post_form.date_input("End date", value=ed)
    new_start_time = post_form.time_input("Start time", value=strt)
    new_end_time = post_form.time_input("End time", value=et)
    new_location_name = post_form.text_input("Location Name", max_chars=50, value=location_name)
    new_location_link = post_form.text_input("Location Link (Google Maps, Waze, etc.)", value=location_link)
    new_details = post_form.text_area("Details", max_chars=500, value=details)
    create = post_form.form_submit_button("Post event!")
    if create:
        if is_empty(new_title):
            st.error("You need a title. What's your event called?")
        elif new_start_date > new_end_date:
            st.error("Your start date comes after your end date. Are you a time traveler?")
        elif new_start_date == new_end_date and new_start_time > new_end_time:
            st.error("Your start time comes after your end time. Are you a time traveler?")
        elif new_end_date < datetime.now().date():
            st.warning("Your event ends before today.")
        elif is_empty(new_location_name):
            st.warning("You need a location name. What's the location name?")
        elif is_empty(new_location_link) or (not validators.url(new_location_link)):
            st.warning("You need a valid link for your location. Where is your location?")
        elif is_empty(new_details):
            st.warning("You need details for your event. What is your event about?")
        else:
            cursor.execute("UPDATE Posts SET title = ?, start_date = ?, end_date = ?, start_time = ?, end_time = ?, location_name = ?, location_link = ?, details = ? WHERE id = ?", (new_title, str(new_start_date), str(new_end_date), str(new_start_time)[:5], str(new_end_time)[:5], new_location_name, new_location_link, new_details, st.session_state.current_post,))
            conn.commit()
            st.success("Post created!")
            with st.spinner("Redirecting to home page..."):
                sleep(3)
            st.switch_page("pages/home.py")