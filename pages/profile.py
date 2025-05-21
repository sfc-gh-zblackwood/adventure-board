import streamlit as st

if "current_user" not in st.session_state:
    st.session_state.current_user = None

st.set_page_config(
    page_title=f"{st.session_state.current_user}'s Profile - Adventure Board"
)

from db import get_connection, side_bar
from time import sleep
import sqlite3

if st.session_state.current_user is None:
    st.switch_page("startup.py")

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

import face_recognition
from PIL import Image
import numpy as np
import io

side_bar()

st.title(f"{st.session_state.current_user}'s Profile")

col1, col2, col3 = st.columns(3)
with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT profile_pic FROM Accounts WHERE username = ?", (st.session_state.current_user,))
    data = cursor.fetchone()
    pic_data = data[0]
    with col1:
        image = st.image(pic_data, use_container_width="never")
    with col2:
        new_pfp = st.file_uploader("Upload new profile picture?", type=["jpg", "jpeg", "png"])
        update_pfp_submit = st.button("Update my profile picture!")
        match_result = 0
        if update_pfp_submit:
            new_pfp_data = new_pfp.getvalue()
            image1 = face_recognition.load_image_file(io.BytesIO(pic_data))
            image2 = face_recognition.load_image_file(io.BytesIO(new_pfp_data))
            face_encodings1 = face_recognition.face_encodings(image1)
            face_encodings2 = face_recognition.face_encodings(image2)
            if len(face_encodings1) == 0 or len(face_encodings2) == 0:
                st.error("Could not detect faces in one or both images.")
            else:
                match_result = face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0], tolerance=0.5)
                if match_result[0]:
                    st.success("They match!")
                    try:
                        cursor.execute("UPDATE Accounts SET profile_pic = ? WHERE username = ?", (new_pfp_data, st.session_state.current_user))
                        conn.commit()
                        with st.spinner("Updating profile picture..."):
                            sleep(3)
                            st.rerun()
                    except sqlite3.IntegrityError as e:
                        error_msg = str(e)
                        if "Accounts.profile_pic" in error_msg:
                            st.error("That profile picture is already in use. Is someone stealing your face or are you stealing theirs? :face_with_raised_eyebrow:")
                else:
                    st.error("Faces don't match.")

def delete_account():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Accounts WHERE username = ?", (st.session_state.current_user,))
        conn.commit()

st.markdown("""<style>.element-container:has(.red) + div button {
                  background-color: red;
                  color: white;
}</style>""", unsafe_allow_html=True)
st.markdown("""<style>.element-container:has(#normal) + div button {
                  color: white;
}</style>""", unsafe_allow_html=True)

st.markdown("<span class='red'></span>", unsafe_allow_html=True)
delete_1 = st.button("Delete Account")
if delete_1:
    st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    st.warning("Are you sure you want to delete your account? This cannot be undone.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<span id='normal'></span>", unsafe_allow_html=True)
        yes_delete = st.button("Yes, delete my account")
        if yes_delete:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Accounts WHERE username = ?", (st.session_state.current_user,))
                conn.commit()
            st.session_state.current_user = None
            st.session_state.confirm_delete = False

    if yes_delete:
        with st.spinner("Deleted account. Redirecting to home page..."):
            sleep(3)
            st.switch_page("startup.py")

    with col2:
        st.markdown("<span class='red'></span>", unsafe_allow_html=True)
        if st.button("Cancel"):
            st.session_state.confirm_delete = False