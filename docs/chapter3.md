# Chapter 3: The session object

```python
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        session = dict(x.split("=") for x in fragment.split("&"))
        st.session_state.session = session
        return session
```

The session object returned by the `get_session_from_fragment()` looks like this:

```python
{
    "access_token": "...",
    "refresh_token": "...",
    "expires_in": "...",
    "token_type": "..."
    ...
}
```

From this, we can extract the `access_token` and `refresh_token` to authenticate the user in the Streamlit app. This is done in the `authenticate_user()` method in [auth_flow.py](../sample/auth_flow.py).

```python
def authenticate_user():
    if "session" in st.session_state:
        session = st.session_state.session
        access_token = session["access_token"]
        refresh_token = session["refresh_token"]
        supabase.auth.sign_in(
            access_token=access_token,
            refresh_token=refresh_token,
            provider="google"
        )
```