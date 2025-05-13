import streamlit as st
from db import get_connection
import sqlite3
import config
from time import sleep

st.set_page_config(
    page_title="Log in to Adventure Board"
)

def is_empty(widget):
    return widget is None or len(widget) == 0 or widget.isspace()

st.page_link("pages/login.py", label="Login", icon="🔐")
st.write("or")
st.page_link("pages/create_account.py", label="Create an account", icon="📝")
st.write("to access the website")

with get_connection() as conn:
    cursor = conn.cursor()
    accounts_exist = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Accounts';").fetchone()
    if accounts_exist == []:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Accounts (
                    name TEXT NOT NULL,
                    username TEXT NOT NULL UNIQUE,
                    profile_pic BLOB NOT NULL UNIQUE,
                    password TEXT NOT NULL);''')
    
    posts_exist = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Posts';").fetchone()
    if posts_exist == []:
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Posts (
                    title TEXT(50) NOT NULL,
                    location_name TEXT(50) NOT NULL,
                    location_link TEXT NOT NULL,
                    creator TEXT NOT NULL
                    );
                    ''')
    conn.commit()