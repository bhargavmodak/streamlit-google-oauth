import streamlit as st
from streamlit_url_fragment import get_fragment
import jwt
from supabase import create_client, Client

url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def login_with_google():
    try: 
        data = supabase.auth.sign_in_with_oauth(
            {
                "provider": 'google',
                "options": {"redirect_to": 'https://improved-space-parakeet-p6477v544jrf7ppr-8501.app.github.dev'},
            }
        )

        return data
    except Exception as e:
        st.write("Error:", e)

def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)

def show_login():
    login_button = st.button("Login with Google")
    if login_button:
        data = login_with_google()
        nav_to(data.url)

def show_logout():
    logout_button = st.button("Logout")
    if logout_button:
        supabase.auth.sign_out()
        st.session_state.session = None
        st.session_state.user = None
        nav_to("/")

def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        session = dict(x.split("=") for x in fragment.split("&"))
        st.session_state.session = session


def get_user(access_token):
    try:
        data = jwt.decode(access_token, options={"verify_signature": False})
        user_metadata = data["user_metadata"]
        user = {
            "email": user_metadata["email"],
            "full_name": user_metadata["full_name"],
            "name": user_metadata["name"],
            "avatar_url": user_metadata["avatar_url"]
        }
        return user
    except Exception as e:
        st.write("Error:", e)

def mainloop():
        user = st.session_state.user
        st.write("Welcome", user["name"], "!")
        st.image(user["avatar_url"])

if __name__ == "__main__":
    # General template
    st.set_page_config(page_title="Which-Group-What-Project")
    st.title("Which-Group-What-Project")

    if "session" not in st.session_state:
        current_fragment = get_fragment()
        get_session_from_fragment(current_fragment)
        if "session" in st.session_state:
            session = st.session_state.session
            st.session_state.user = get_user(session["access_token"])
            mainloop()
            show_logout()
        if current_fragment is not None and len(current_fragment) == 0:
            show_login()
    else:
        mainloop()
        show_logout()



        

    
