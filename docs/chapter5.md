# 📖 Chapter 5: The Home Route

In the previous chapter we stored the `g_session` object in the local storage in the `/auth` route. Since we wanted the home route ([streamlit_app.py](../streamlit_app.py), or `/`) to be blind as to whether the user has logged in just now or was already in local storage, we switched to the `app` route after storing the `g_session` object in the local storage.

In this chapter, we will check the local storage for the `g_session` object in the home route [streamlit_app.py](../streamlit_app.py) and consider the user logged in if it is present.

## Getting the User Object from Supabase

As already seen in [Chapter 3 -> How to use the session object to authenticate the user](chapter3.md/#how-to-use-the-session-object-to-authenticate-the-user), we can use the `supabase.auth.set_session()` method to authenticate the user using the `access_token` and `refresh_token` pair. This method sets the session for the user and allows them to access Supabase resources.

`streamlit_app.py` is very simple, you can see the main function below:

```python
# Main program after login
def main():
    st.header("Streamlit Supabase Auth")
    if "user" not in st.session_state:
        with st.spinner("Checking cookies..."):
            # Check if the user is present in the local storage
            g_session: dict = st_ls.get("g_session")
            time.sleep(0.5)

            # If not, show the login page
            if g_session is None or len(g_session) == 0:
                show_login(supabase)
            else:
                # Else authenticate the user
                user: object = authenticate_user(supabase, g_session, st_ls)
                if user is not None:
                    st.session_state.user = dict(user)["user_metadata"]
                    st.rerun()
    else:
        set_sidebar(st.session_state.user)
        st.markdown("---")
        st.markdown("### Here you can add your content")
```

## The `authenticate_user()` function

The `authenticate_user()` function is defined in the [auth_flow.py](../sample/auth_flow.py) file. It uses the `supabase.auth.set_session()` method to authenticate the user and returns the user object.

```python
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
            # Several exceptions are handled here
            # ...
            st.write("Error:", e)
            return None
```

> [!TIP]
> To gain more understanding of how the `supabase.auth.set_session()` method works try printing the response object.

## The `response.user` object

The `response.user` object looks like this:

```json
{
  "id": "...",
  "app_metadata": {
    "provider": "google",
    "providers": ["google"]
  },
  "user_metadata": {
    "avatar_url": "...",
    "email": "...",
    "email_verified": true,
    "full_name": "...",
    "iss": "...",
    "name": "...",
    "phone_verified": false,
    "picture": "...",
    "provider_id": "...",
    "sub": "..."
  },
  "aud": "...",
  "confirmation_sent_at": null,
  "recovery_sent_at": null,
  "email_change_sent_at": null,
  "new_email": null,
  "new_phone": null,
  "invited_at": null,
  "action_link": null,
  "email": "...",
  "phone": "",
  "created_at": "...",
  "confirmed_at": "...",
  "email_confirmed_at": "...",
  "phone_confirmed_at": null,
  "last_sign_in_at": "...",
  "role": "...",
  "updated_at": "...",
  "identities": [{ 
        //...
    }],
  "is_anonymous": false,
  "factors": null
}
```

Of these, the `user_metadata` object is the most important. It contains the user's metadata, such as the `id`, `email`, `full_name`, and `avatar_url`.

We save this object in `st.session_state.user`. You may use it anywhere throughout the app. Since you also have the supabase session, you can use other Supabase methods from [Supabase Python Client -> Auth](https://supabase.com/docs/reference/python/auth-getsession)
to interact with Google Services like Drive or Sheets.

## Conclusion

The demo project uses `set_sidebar()` to show the user's profile in the sidebar. It also hides the `/auth` route from the sidebar, and shows how to do a multipage app in Streamlit.

Before that, we will take a look at logging out the user in the next chapter.

---

⇦  [Chapter 4: Local Storage and the Auth Route](chapter4.md) | [Chapter 6: Logging Out the User](chapter6.md) ⇨



