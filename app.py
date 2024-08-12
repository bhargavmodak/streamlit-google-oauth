# Pip packages
import streamlit as st
from supabase import create_client, Client
import time

# Local imports
import sample.st_local_storage as st_local_storage
from sample.auth_flow import show_login, authenticate_user
from sample.utils import set_sidebar

# Local storage
st_ls = st_local_storage.StLocalStorage()

# Here supabase is a global variable for the Supabase client, but
# you can also create a client in a function and pass it around.
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


# Main program after login
def main():
    st.header("Streamlit Supabase Auth")
    if "user" not in st.session_state:
        with st.spinner("Checking cookies..."):
            g_session: dict = st_ls.get("g_session")
            time.sleep(0.5)
            if g_session is None or len(g_session) == 0:
                show_login(supabase)
            else:
                user: object = authenticate_user(supabase, g_session, st_ls)
                if user is not None:
                    st.session_state.user = dict(user)["user_metadata"]
                    st.rerun()
    else:
        set_sidebar(st.session_state.user)
        st.markdown("---")
        st.markdown("### Here you can add your content")


main()
