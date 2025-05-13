import streamlit as st
import sqlite3
from db import get_connection

def login(username, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT FROM Accounts WHERE username = ? AND password = ?", (username, password))
        if not cursor.fetchone():
            st.error("Username or password is incorrect")
