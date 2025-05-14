import streamlit as st
from db import get_connection
from time import sleep

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

st.set_page_config(
    page_title=f"{st.session_state.current_user}'s Profile - Adventure Board"
)


def delete_account():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Accounts WHERE username = ?", (st.session_state.current_user,))
        conn.commit()

st.markdown("""<style>
               div.stButton > button:first-child {
                  background-color: red;
                  color: white;
               } 
               div.stButton > button:first-child:hover {
                  background-color: red;
                  color: white;
               }
               </style>""", unsafe_allow_html=True)


delete_1 = st.button("Delete Account")
if delete_1:
    st.session_state.confirm_delete = True

if st.session_state.confirm_delete:
    st.warning("Are you sure you want to delete your account? This cannot be undone.")
    col1, col2, col3 = st.columns(3)
    with col1:
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
        if st.button("Cancel"):
            st.session_state.confirm_delete = False