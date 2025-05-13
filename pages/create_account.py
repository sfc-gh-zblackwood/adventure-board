import streamlit as st
import sqlite3
from startup import is_empty
from db import get_connection
import config

account_form = st.form(key="account")
name = account_form.text_input("Name", placeholder="John Smith")
username = account_form.text_input("Username")
profile_picture = account_form.file_uploader("Upload a picture of your beautiful face!", type=["jpg", "jpeg", "png"])
password = account_form.text_input("Password", type="password")
create = account_form.form_submit_button("Create Account")
if create:   
    if is_empty(name):
        st.error("Please write your name")
    elif is_empty(username):
        st.error("Please provide a unique username")
    elif profile_picture is None:
        st.error("Please provide a picture of your face")
    elif is_empty(password):
        st.error("Please provide a password")
    else:
        picture_data = profile_picture.read()
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Accounts VALUES (?, ?, ?, ?)", (name, username, picture_data, password))
                conn.commit()
                config.current_user = username
                st.success("Created your new account!")
            except sqlite3.IntegrityError as e:
                error_msg = str(e)
                if "Accounts.username" in error_msg:
                    st.error("That username is already in use.")
                if "Accounts.profile_pic" in error_msg:
                    st.error("That profile picture is already in use.")