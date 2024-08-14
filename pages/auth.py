# Pip packages
import streamlit as st
import time
from streamlit_extras.switch_page_button import switch_page

# Local imports
from sample.utils import get_fragment, get_session_from_fragment
import sample.st_local_storage as st_local_storage


# Local storage
st_ls = st_local_storage.StLocalStorage()

# Get the current fragment
current_fragment = get_fragment()

# Check if the session is already stored in the local storage
st.session_state.g_session = st_ls.get("g_session")
time.sleep(0.5)
if st.session_state.g_session is not None and len(st.session_state.g_session) > 0:
    switch_page("streamlit_app")

st.info("Checking your Google session...")

# If not, check if the current fragment has a session
if current_fragment is not None:
    g_session = get_session_from_fragment(current_fragment)

    if "error" in g_session:
        st.error("Error:", g_session["error"])
        st.info("Redirecting to login page...")
        time.sleep(1)
        switch_page("streamlit_app")
    else:
        if g_session is not None:
            st_ls.set("g_session", g_session)
