# 📖 Chapter 6: Logging Out the User

## The logout button

Use the `delete()` method from the `st_ls` object to delete the `g_session` key. This will log out the user from the app.

```python
def show_logout(st_ls):
    if st.button("Logout"):
        st_ls.delete("g_session")
        st.info("Logging out...")
        st.session_state.clear()
```

Trying to use `try` and `except` blocks to catch exceptions causes the app to go into an infinite loop. This is because `st_ls.delete()` takes a few seconds to delete the key, and the `except` block is triggered before the key is deleted. This causes the app to re-render, and the `except` block is triggered again, causing the app to go into an infinite loop.

The `st_ls.delete()` method is asynchronous, and the `st.info()` method is synchronous. This causes the `st.info()` message to be displayed before the key is deleted. The `st.session_state.clear()` method is synchronous and clears the session state immediately.

Clearing the session state removes the `st.session_state.user` key, and since `st_ls.delete()` reruns the app as mentioned in [Chapter 4 -> Using the st\_local\_storage.py module](chapter4.md/#using-the-st_local_storagepy-module), the `st.session_state.user` key is set to `None` when the app reruns. 

This causes the app to go back to the login page, as is intended when the user logs out.

## The `authenticate_user()` function

The `authenticate_user()` function from [auth_flow.py](../sample/auth_flow.py) is used to check if the user is logged in. If there are errors, we also log out the user.

```python
def authenticate_user(supabase, g_session: dict, st_ls):
    # Code...
    # ....
        except Exception as e:
            if type(e).__name__ == "AuthApiError":
                # Handing errors...
                # Then
                # Log out the user
                st_ls.delete("g_session")
                st.info("Logging out...")
                st.session_state.clear()
            else:
                st.write("Error:", e)
            return None
```

This is done when the access token expires, and the token pair in the local storage is no longer valid. The user is logged out, and the app goes back to the login page.

---

In the next chapter, we will discuss how to hide the `/auth` route from the user, and how to add multiple pages.

---

⇦ [Chapter 5: The Home Route](chapter5.md) | [Chapter 7: Wrapping Up](chapter7.md) ⇨