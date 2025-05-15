import streamlit as st

if "current_user" not in st.session_state:
    st.session_state.current_user = None

st.set_page_config(
    page_title=f"{st.session_state.current_user}'s Profile - Adventure Board"
)

from db import get_connection, side_bar
from time import sleep

if st.session_state.current_user is None:
    st.switch_page("startup.py")

if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

side_bar()

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

st.markdown("<span class='delete-account'></span>", unsafe_allow_html=True)
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