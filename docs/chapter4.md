# 📖 Chapter 4: Local Storage and the Auth Route

In the previous chapter we obtained the **google oauth session object** from the `get_session_from_fragment()` method in the `/auth` route. (Of course, in Python it is a dictionary.) We stored this session object in the streamlit state. But, the session object is lost when the user refreshes the page or closes the browser. To persist the session object, we can use the browser's local storage.

## Local Storage vs Cookies

As seen in [Chapter 0](chapter0.md), we can use local storage or cookies to persist the session object. Cookies are more secure than local storage, but local storage is easier to use. We will use local storage in this tutorial.

If you want to contribute to this tutorial by adding a cookie-based solution, please refer to the [Contributing](contributing.md) section and make a pull request.

## Using local storage

As mentioned in [Chapter 0](chapter0.md), there is a discussion on Streamlit forums titled '[Saving data in local storage via streamlit](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/1)', which has possible solutions. 

1. User [gagangoku](https://github.com/gagangoku) built a [synchronous way to access localStorage](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/8) from Streamlit using websockets at [streamlit-ws-localstorage](https://pypi.org/project/streamlit-ws-localstorage/1.0.0/).
   1. This solution requires a second server to be running somewhere. You can host your own, or use `wsauthserver.supergroup.ai`, which user gagangoku has provided.
   2. Obviously, depending on a third-party server is not ideal.
2. User [toolittlecakes](https://github.com/toolittlecakes) built their own version of the [streamlit-javascript](https://pypi.org/project/streamlit-javascript/) library, [which allows you to run JavaScript code in Streamlit.](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/14)
   1. Building on the work of toolittlecakes, user [jcarroll](https://gist.github.com/sfc-gh-jcarroll) wrote a [small gist for an st_local_storage](https://gist.github.com/sfc-gh-jcarroll/e73f3ac80dadb5d0f2136d9d949c35a9) module that abstracts reading and writing keys to local storage to a dict/session_state like interface. 
   2. In the gist, user [duolabmeng6](https://github.com/duolabmeng6) added a [small modification](https://gist.github.com/sfc-gh-jcarroll/e73f3ac80dadb5d0f2136d9d949c35a9?permalink_comment_id=5127241#gistcomment-5127241) to the gist to add more methods.
   3. Note that user [dkn-vtl](https://github.com/dkn-vtl) figured out that [it doesn't work for multiple keys](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/19) and triggers a rerun when the JS code is executed, and provided a [solution](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/21).

I have used the gist by user jcarroll in this tutorial, but modified it slightly to suit our needs. The modified code is in [st_local_storage.py](../sample/st_local_storage.py).

## Using the st_local_storage.py module

Since the `st_local_storage.py` module is a Python file, we can import it and use it in our Streamlit app. As seen in `auth.py`, we can import the module and use it to store the session object in the local storage.

```python
import sample.st_local_storage as st_local_storage
# Local storage
st_ls = st_local_storage.StLocalStorage()
```

The `st_local_storage.py` module has the following methods:

1. `get(key: str) -> Any`: Get the value of the key from the local storage.
2. `set(key: str, value: Any) -> None`: Set the value of the key in the local storage.
3. `delete(key: str) -> None`: Remove the key from the local storage.

Note that for the `get()` method to work, we need to keep track of a UUID for each key to enable reruns. This means that when we use `set()` and `delete()`, streamlit reruns because the container id changes. There is no way to avoid this, as per user jcarrroll's [comment](https://discuss.streamlit.io/t/saving-data-in-local-storage-via-streamlit/28785/22). 

If you find a way to avoid reruns, please refer to the [Contributing](contributing.md) section and make a pull request.

## Using the st_local_storage.py module in the /auth route

The home route `/` [app.py](../app.py) must be blind as to whether user has logged in just now or was already in local storage. So, we will use the `st_local_storage.py` module in the `/auth` route to store the session object in the local storage.

This way, whenever the home route `/` is accessed, it will check the local storage for the session object. If it is present, the user is considered logged in. If not, the user is considered logged out.

Earlier, we implemented the `/auth` route as follows:
```python
current_fragment = get_fragment()
g_session = get_session_from_fragment(current_fragment)
```

Now, we will add some null checks and set the session object in the local storage:
```python
current_fragment = get_fragment()

if current_fragment is not None:
    g_session = get_session_from_fragment(current_fragment)

    if "error" in g_session:
        st.error("Error:", g_session["error"])
        st.info("Redirecting to login page...")
        time.sleep(1)
        switch_page("app")
    else:
        if g_session is not None:
            st_ls.set("g_session", g_session)
            # Anything after this would not be run as streamlit would rerun
```

The `error` key is present in the URL fragment, and subsequently, in the session object, if there is an error. [OAuth 2.0 for Client-side Web Applications -> Step 3: Handle the OAuth 2.0 server response](https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow#handlingresponse) explains this.

Since streamlit will rerun several times after `st_ls.set("g_session", g_session)`, we need to check if `st_ls.set("g_session", g_session)` finished successfully. We can do this by checking if the session object is present in the local storage:

```python
st.session_state.g_session = st_ls.get("g_session")
time.sleep(0.25)
if st.session_state.g_session is not None and len(st.session_state.g_session) > 0:
    switch_page("app")
```

The combination of the above code snippets results in [auth.py](../pages/auth.py).

## Why switch_page() instead of nav_to() like we used in Chapter 2?

`nav_to()` refreshes the entire page, but we do not want to redirect the user **again** after they have just been redirected twice from our app to Google and back. So, we use `switch_page()` to navigate to the [app.py](../app.py) home route `/` without refreshing the page.

Now, in the [app.py](../app.py) home route `/`, we can check the local storage for the session object and consider the user logged in if it is present. We will implement this in the next chapter.

---

⇦  [Chapter 3: The Session object](chapter3.md) | [Chapter 5: The Home Route](chapter5.md) ⇨