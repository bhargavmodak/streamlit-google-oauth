# 📖 Chapter 3: The Session object

In the [previous chapter](./chapter2.md), we saw how the user can authenticate themselves using the Google OAuth2 provider. Once the user is authenticated, the URL fragment is converted into a session object. This session object contains the user's access token, refresh token, and other information required to access Google resources.

## The session object

The session object returned by the `get_session_from_fragment()` looks like this:

```python
{
    "access_token": "...",
    "refresh_token": "...",
    "expires_at": "...",
    "expires_in": "...",
    "token_type": "..."
    ...
}
```
The `access_token` is used to authenticate the user and access Google resources. The `refresh_token` is used to get a new access token when the current access token expires. The `expires_at` and `expires_in` fields are used to determine when the access token expires.

> [!TIP]
> Learn more about the token pair is used to authenticate the user in the [Google OAuth2 documentation](https://developers.google.com/identity/protocols/oauth2).

## How to use the session object to authenticate the user

Supabase's `Client` object has a method called `supabase.auth.set_session()` that takes the access token-refresh token pair and sets it as the session for the user. Hence one does not have to use jwt to decode the access token and refresh token.

``` python
response = supabase.auth.set_session(access_token, refresh_token)
```

Supabase compares the token pair with the User and session already stored in the Supabase authentication system. (Check [Chapter 2 -> Redirection from Google](chapter2.md/#redirection-from-google) for more information on how the user is created in the Supabase authentication system.)

If the token pair matches, the user is authenticated and can access Supabase resources. This also prevents a malicious user from accessing resources by manipulating the URL fragment.

> [!NOTE]
> This flow is all you need for a general authentication. From chapters 1 to 3, you redirected the user to the Google OAuth consent screen, received the token pair in the URL fragment, and used it to authenticate the user via Supabase. You may use the user object returned by the `set_session()` method to access the user's information.

The following chapters will discuss using local storage, using the returned user object, hiding the `/auth` route from streamlit sidebar, and how to logout the user.

---

⇦ [Chapter 2: The sign_in_with_oauth() method](chapter2.md) | [Chapter 4: Local Storage and the Auth Route](chapter4.md) ⇨