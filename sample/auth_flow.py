import streamlit as st
from sample.utils import nav_to


# Function to return the Google login link
def return_google_login_link(supabase):
    try:
        data = supabase.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {"redirect_to": st.secrets["REDIRECT_URL"]},
            }
        )

        return data.url
    except Exception as e:
        st.write("Error:", e)


# Function to show login button
def show_login(supabase):
    login_button = st.button("Login with Google")
    if login_button:
        url = return_google_login_link(supabase)
        nav_to(url)


# Function to show logout button
def show_logout(st_ls):
    if st.button("Logout"):
        try:
            st.session_state.user = None
            st_ls.delete("token")
        except:
            st.write("Error logging out.")
