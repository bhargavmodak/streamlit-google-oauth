import streamlit as st
from sample.utils import set_sidebar
from streamlit_extras.switch_page_button import switch_page

if "user" not in st.session_state:
    switch_page("streamlit_app")
else:
    set_sidebar(st.session_state.user)

st.header("Example Page (Other)")

st.write("This is an example page.")
