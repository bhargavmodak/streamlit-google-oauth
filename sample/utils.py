import streamlit as st
from streamlit_url_fragment import get_fragment
import time
import sample.st_local_storage as st_local_storage

st_ls = st_local_storage.StLocalStorage()


# Function to navigate to a URL
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (
        url
    )
    st.write(nav_script, unsafe_allow_html=True)


# Function to get the Google session from the URL fragment
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        g_session = dict(x.split("=") for x in fragment.split("&"))
        return g_session


# Function to clear the URL fragment
def clear_fragment():
    fragment = get_fragment()
    if fragment is not None and len(fragment) > 0:
        nav_to(st.secrets["REDIRECT_URL"])
        return False
    else:
        return True


# Function to show logout button
def show_logout(st_ls):
    if st.button("Logout"):
        st_ls.delete("g_session")
        st.info("Logging out...")
        st.session_state.clear()


def set_sidebar(user: dict):
    # Put in sidebar
    st.sidebar.write(f"Welcome {user['full_name']}")
    st.sidebar.image(user["avatar_url"], width=100)
    st.sidebar.page_link("streamlit_app.py", label="Home")
    st.sidebar.page_link("pages/other.py", label="Example Page")
    with st.sidebar:
        show_logout(st_ls)
