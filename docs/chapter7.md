# 📖 Chapter 7: Wrapping Up

## Hiding the `/auth` route

When using [Streamlit Multipage App](https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app), the `/auth` route is visible to the user in the sidebar. This is not ideal, as the user should not be able to see the `/auth` route after logging in.

Write the following into `.streamlit/config.toml` to hide the `/auth` route:

```toml
[client]
showSidebarNavigation = false
```

This will hide the sidebar by default, not showing ANY pages in the `pages` folder. To show the pages, you can use the `st.sidebar` method to create a sidebar with links to the pages.

## Adding multiple pages

To add multiple pages, create a `pages` folder in the root directory of the project. Inside the `pages` folder, create a Python file for each page. For example, create a `other.py` file for an "Example" page.

In the `other.py` file, write the following code:

```python
import streamlit as st
from sample.utils import set_sidebar
from streamlit_extras.switch_page_button import switch_page

if "user" not in st.session_state:
    switch_page("app")
else:
    set_sidebar(st.session_state.user)

st.header("Example Page (Other)")
st.write("This is an example page.")
```

### Adding those pages to the sidebar

There is a `set_sidebar()` function in the [utils.py](../sample/utils.py) file that sets the sidebar for the user. This function is used to set the sidebar for each page.

```python
def set_sidebar(user: dict):
    # Put in sidebar
    st.sidebar.write(f"Welcome {user['full_name']}")
    st.sidebar.image(user["avatar_url"], width=100)
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/other.py", label="Example Page")
    with st.sidebar:
        show_logout(st_ls)
```

Since we disabled the sidebar navigation, the sidebar will not be visible by default. We manually add each page to the sidebar using the `st.sidebar.page_link()` method.

The `show_logout()` function is added to the sidebar to allow the user to log out.

Since the user could be logged out on any page, in each page we check the `st.session_state.user` key. If the key is not present, we switch the page to the login page, as shown in the "Example" page.

## Conclusion

This concludes the explanation of the demo app. I hope this template helps you understand how to use Google OAuth with Supabase and Streamlit. 

if you find any improvements, please feel free to open an issue or a pull request. Read the [CONTRIBUTING.md](../CONTRIBUTING.md) file to learn how to contribute.

---

⇦ [Chapter 6: Logging Out the User](chapter6.md)