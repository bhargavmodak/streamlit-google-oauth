import streamlit as st
from streamlit_url_fragment import get_fragment


# Function to navigate to a URL
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (
        url
    )
    st.write(nav_script, unsafe_allow_html=True)


# Function to get the session from the URL fragment
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        session = dict(x.split("=") for x in fragment.split("&"))
        st.session_state.session = session
        return session


# Function to clear the URL fragment
def clear_fragment():
    fragment = get_fragment()
    if fragment is not None and len(fragment) > 0:
        nav_to(st.secrets["REDIRECT_URL"])
        return False
    else:
        return True
