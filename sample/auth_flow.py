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
    st.write(
        "A new tab will open to authenticate with Google. You may need to allow pop-ups."
    )
    st.write("Please close this tab after logging in.")
    login_button = st.button("Login with Google")
    if login_button:
        url = return_google_login_link(supabase)
        nav_to(url)


# Function to authenticate the user
def authenticate_user(supabase, g_session: dict, st_ls):
    if g_session is not None:
        access_token = g_session["access_token"]
        refresh_token = g_session["refresh_token"]
        try:
            response = supabase.auth.set_session(
                access_token=access_token, refresh_token=refresh_token
            )
            return response.user
        except Exception as e:
            if type(e).__name__ == "AuthApiError":
                if e.message == "Invalid Refresh Token: Already Used":
                    st.error("The refresh token was already used. Please login again.")
                elif e.message == "User from sub claim in JWT does not exist":
                    st.error("The access token was messed with. Please login again.")
                else:
                    st.error("Error:", e)
                st_ls.delete("g_session")
                st.info("Logging out...")
                st.session_state.clear()
            else:
                st.write("Error:", e)
            return None
