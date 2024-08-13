# 📖 Chapter 2: The sign_in_with_oauth() method

The `sign_in_with_oauth()` method is provided by the Supabase Python client, as mentioned in earlier chapters. [This method allows users to authenticate using OAuth providers like Google. Read the documentation here.](https://supabase.com/docs/reference/python/auth-signinwithoauth)

## No Automatic Redirect

Unlike other authentication methods, the `sign_in_with_oauth()` method doesn't automatically redirect the user to the Google login page. Instead, it returns an object containing the login link. This object has the following form:

```json
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

We are using the `redirect_to` option to specify the URL where the user should be redirected after logging in with Google. To understand what we should use as a `redirect_to` URL, we need to understand the authentication flow in more detail. ↓

## Manual Redirect

To initiate the authentication flow, we need to redirect the user to the provided URL, which was returned by `return_google_login_link()`.

This can be achieved by using a redirect mechanism in your web application. For programmatically sending a user to the login page, there is a discussion on Streamlit Forums, titled '[Programmatically Send User to a Web Page with No Click](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904)', which discusses several solutions.

[RyanMaley suggests using webbrowser.open()](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/2) to open the URL in the default web browser. 

However, this doesn't work in production. [Franky1 explains why:](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/4)

> What happens when webbrowser is used? A browser is started on the computer on which the python application is running. But there is no browser on streamlit cloud and even if there was, it would be the wrong computer.

[Another solution by user Adamih](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/7) is to use simple HTML like this:

```python
def nav_to(url):
    nav_script = """
        <meta http-equiv="refresh" content="0; url='%s'">
    """ % (url)
    st.write(nav_script, unsafe_allow_html=True)
```

This solution does work for some websites, but not for all. For example, it doesn't work for Google OAuth. This is because Streamlit Community Cloud wraps the app in an iframe, and Google doesn't allow its login page to be opened in an iframe.

[There is an active issue on the Streamlit GitHub repository regarding this. (7123)↗](https://github.com/streamlit/streamlit/issues/7123)

In the same thread, [Vince_Fleming suggests using JavaScript](https://discuss.streamlit.io/t/programmatically-send-user-to-a-web-page-with-no-click/21904/10) to open the URL in a new tab. This is the solution we will use in this template.

```python
def nav_to(url):
    js = f'window.open("{url}", "_blank").then(r => window.parent.location.href);'
    st_javascript(js)
```
However, the javascript console says that `window.open().then()` is not a function. So, we can use the code below instead.

```python
def nav_to(url):
    js = f'window.open("{url}", "_blank");'
    st_javascript(js)
```

Check [utils.py](../sample/utils.py) for the implementation.

There's nothing that can be done about the already opened tab, it has to be closed manually. Submit feedback at the issue mentioned above to help the Streamlit team improve the platform.

## Redirection from Google

To make the user log in, we use a button, `show_login()` method in [auth_flow.py](../sample/auth_flow.py).

Once the user successfully logs in with Google, Supabase automatically creates a new user in the Supabase authentication system. *How?* In [Chapter 1](chapter1.md), we added Supabase's callback URL to the Google OAuth consent screen. This allows Supabase to receive the user's information after they log in with Google.

This user will have the necessary credentials to access Supabase resources. You can check users at the [Supabase dashboard](https://app.supabase.io/), under `Authentication` -> `Users`.

Since we redirected the user to the Google OAuth consent screen without opening a new tab, we need to redirect them back to the Streamlit app after the login is complete. This is where the `redirect_to` option in the `sign_in_with_oauth()` method comes into play. 

It would default to the `SITE_URL` specified in the Supabase project settings. But we can override it by specifying the `redirect_to` option in the `sign_in_with_oauth()` method.

***Why would we want to override it?***

## The URL fragment

After the user logs in with Google, they are redirected back to the Streamlit app. The URL will contain a fragment that looks like this:

```
http://localhost:8501/#access_token= ... &refresh_token= ... &expires_in= ... &token_type= ...
```

This fragment contains the access token, refresh token, and other information required for the user to access Google resources. We can extract this information from the URL fragment and use it to authenticate the user in the Streamlit app.

> [!WARNING]
> However, since the fragment is simply `#` followed by the token information, users might notice and direclty manipulate the URL. **This is a security risk.** Removing the fragment from the URL would require a page reload, which is not ideal.

To prevent the above warning, we set the `REDIRECT_URL` option above, not to the home 'route' of the Streamlit app, but to a specific route that handles the authentication flow. This route will extract the token information from the URL fragment and use it to authenticate the user.
In our case, we set it to `/auth`.

```
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY"
BASE_URL = "http://localhost:8501"
REDIRECT_URL = "http://localhost:8501/auth"
```

> [!TIP]
> You don't have to use `/auth` as the route. You can use any route you like. 
> Learn more about Streamlit multipage apps at [Get Started with Multipage Apps](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app). and [Multipage Apps in Streamlit](https://docs.streamlit.io/develop/concepts/multipage-apps).

## Extracting the session information

To extract the session information from the URL fragment, we need to parse the fragment and extract the token information. Since we redirected the user to the `/auth` route, we can perform this extraction in the `/auth` page like so:

```python
# auth.py
from sample.utils import get_fragment, get_session_from_fragment
from streamlit_extras.switch_page_button import switch_page

current_fragment = get_fragment()
g_session = get_session_from_fragment(current_fragment)

# Optional:
st.session_state.g_session = g_session
.
.
.
```

The method `get_session_from_fragment()` from [utils.py](../sample/utils.py).

```python
def get_session_from_fragment(fragment):
    if fragment is not None and len(fragment) > 10:
        fragment = fragment.replace("#", "")
        g_session = dict(x.split("=") for x in fragment.split("&"))
        return g_session
```

> [!NOTE]
> The actual implementation of the `/auth` route in the [auth.py](../sample/auth.py) file is different than the above code snippet. The above code snippet is a simplified version to demonstrate how to extract the session information from the URL fragment.

Once we get the `g_session` object, we can store it in the streamlit state and access it throughout the app.

But, before we authenticate the user, we need to understand the `Session` object, which is used to store the user's session information.

---

⇦ [Chapter 1: Prerequisites for Supabase and Streamlit](chapter1.md) | [Chapter 3: The Session object](chapter3.md) ⇨


