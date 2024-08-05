# Pip packages: streamlit, streamlit-url-fragment, pyjwt, supabase-py
import streamlit as st
from supabase import create_client, Client

# Local imports
import sample.st_local_storage as st_local_storage
from sample.auth_flow import show_login, show_logout
from sample.state import get_user
from sample.utils import get_fragment, get_session_from_fragment, clear_fragment


# Local storage
st_ls = st_local_storage.StLocalStorage()
token = st_ls.get("token")

# Here supabase is a global variable for the Supabase client, but
# you can also create a client in a function and pass it around.
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)


# Main program after login
def main():
    # Because we are using an implicit flow, we need to clear the URL fragment
    # This causes multiple refreshes, but it is necessary to prevent the token from being exposed
    # Use PKCE for a more secure flow, or don't use streamlit
    if clear_fragment():
        user = st.session_state.user
        st.write("Welcome", user["name"], "!")
        st.image(user["avatar_url"])
        st.write("Here you can provide an entrypoint to your program.")
        # Add your code here
        # ...
        # ...
        # ...


if __name__ == "__main__":
    st.title("Streamlit Supabase Auth")

    # If there is no token in the local storage, check the URL fragment
    if token is None:
        current_fragment = get_fragment()
        # If the fragment is empty, show the login button, else get the session
        if current_fragment is not None and len(current_fragment) == 0:
            show_login(supabase)
        else:
            session = get_session_from_fragment(current_fragment)
            if session is not None:
                # Save the auth token in the local storage
                st_ls.set("token", session["access_token"])

    # If there is a token in the local storage, get the user data
    else:
        st.session_state.user = get_user(token)
        main()
        show_logout(st_ls)
