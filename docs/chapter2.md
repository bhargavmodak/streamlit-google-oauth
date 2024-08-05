# Chapter 2: The sign_in_with_oauth() method

The `sign_in_with_oauth()` method is provided by the Supabase Python client, as mentioned in earlier chapters. [This method allows users to authenticate using OAuth providers like Google.](https://supabase.com/docs/reference/python/auth-signinwithoauth)

## No Automatic Redirect

Unlike other authentication methods, the `sign_in_with_oauth()` method doesn't automatically redirect the user to the Google login page. Instead, it returns an object containing the login link. This object has the following form:

```python
{
    "provider": "google",
    "url": "https://your-supabase-project-url.supabase.co/auth/v1/oauth/authorize?provider=google"
}
```

The `provider` field indicates the authentication provider, in this case, "google". The `url` field contains the actual login URL.

This is performed in the `return_google_login_link()` method in [auth_flow.py](../sample/auth_flow.py).

```python
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
```

## Manual Redirect

To initiate the authentication flow, we need to redirect the user to the provided URL, which was returned by `return_google_login_link()`.

This can be achieved by using a redirect mechanism in your web application. For programmatically sending a user to the login page, there is a discussion: [Programmatically Send User to a Web Page with No Click](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904) which discusses several solutions.

[RyanMaley suggests using webbrowser.open()](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/2) to open the URL in the default web browser. This doesn't work in production. [Franky1 explains why:](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/4)

> What happens when webbrowser is used? A browser is started on the computer on which the python application is running. But there is no browser on streamlit cloud and even if there was, it would be the wrong computer.

[Ultimately the solution is to use simple HTML like this:](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/7)

```python
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)
```
This is included in [utils.py](../sample/utils.py).

There's another method for opening in a new tab:

```python
def nav_to(url):
    js = f'window.open("{url}", "_blank").then(r => window.parent.location.href);'
    st_javascript(js)
```

This is performed in the `show_login()` method in [auth_flow.py](../sample/auth_flow.py).

## Redirection from Google

Once the user successfully logs in with Google, Supabase automatically creates a new user in the Supabase authentication system. This user will have the necessary credentials to access Supabase resources. You can check this at the [Supabase dashboard](https://app.supabase.io/), under `Authentication` -> `Users`.

However, since we manually redirected the user to the Google login page, we need to redirect them back to the Streamlit app after the login is complete. This is where the `redirect_to` option in the `sign_in_with_oauth()` method **SHOULD** come into play. Unfortunately, this option doesn't work as expected. This is possibly because we manually redirected the user to the Google login page.

As such, it defaults to the `SITE_URL` specified in the Supabase project settings. As mentioned in the [previous chapter](chapter1.md), this URL should be set to the URL where the Streamlit app is hosted. For local development, this can be `http://localhost:8501/`.

## The URL fragment

After the user logs in with Google, they are redirected back to the Streamlit app. The URL will contain a fragment that looks like this:

```
http://localhost:8501/#access_token= ... &refresh_token= ... &expires_in= ... &token_type= ...
```

This fragment contains the access token, refresh token, and other information required for the user to access Google resources. We can extract this information from the URL fragment and use it to authenticate the user in the Streamlit app.

This is performed in the `get_session_from_fragment()` method in [utils.py](../sample/utils.py).

```python
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        session = dict(x.split("=") for x in fragment.split("&"))
        st.session_state.session = session
        return session
```

Note that it also stores the session information in the *Streamlit session state*. This is useful for persisting the session information across Streamlit app sessions. It does not, however, store the session information in the browser's local storage. This means that the session information will be lost if the user closes the browser tab or refreshes the page.

⇦ [Chapter 1: Prerequisites for Supabase and Streamlit](chapter1.md) | [Chapter 3: The Session object](chapter3.md) 


