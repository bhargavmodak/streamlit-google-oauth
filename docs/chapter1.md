# Chapter 1: Prerequisites for Supabase and Streamlit

Before we start building the app, we need to set up a few things. This chapter will guide you through setting up Supabase and Streamlit.

## Setting up Supabase

### 1. Create a Project and obtain the Supabase URL and Anon Key

1. **Create a Supabase account**: Go to [Supabase](https://supabase.io/) and sign up for an account.
2. **Create a new project**: Once you have signed up, create a new project. You can name it whatever you want.
3. **Get the Supabase URL and Anon Key**: Once the project is created, go to the project settings and copy the Supabase URL and Anon Key. We will use these in the Streamlit app. See [Secrets](###secrets) for more information.

### 2. Set up Google OAuth in Supabase

- [Here](https://supabase.com/docs/guides/auth/social-login/auth-google) is a guide to set up Google OAuth in Supabase.
- [Here's](https://developers.google.com/identity/protocols/oauth2) a guide to set up Google OAuth in the Google Developer Console.
   
1.  Go to the `Authentication` tab in the project settings.
2.  Under `CONFIGURATION`, click on `Providers`.
3.  Turn off the `Email/Password` provider, if you're only going to use the Google OAuth provider.
4.  Click on `Google` and enable it.
5.  You will need to provide the `Client ID` and `Client Secret` from the Google Developer Console.
6.  Copy the callback URL for the Google OAuth provider. This will be used in the Google Developer Console.
7.  Set up the redirect URI in the Google Developer Console. This will be the URL where Google sends part of the OAuth response. It will be under `APIs & Services` -> `Credentials` -> `OAuth 2.0 Client IDs` -> `Your App` -> `Authorized redirect URIs`.
8.  Back in the Supabase project settings, under `Authentication` -> `CONFIGURATION` -> `URL Configuration`, set the `Redirect URL` to the URL where the Streamlit app will be hosted. This will be used to redirect the user back to the Streamlit app after the OAuth flow is complete. It can be `http://localhost:8501/` for local development.
9.  Save the settings.

## Setting up Streamlit

Follow the steps in the [README](/README.md) to set up the Streamlit app on your local machine.

### Secrets

In other frameworks we use a `.env` file to store secrets. Streamlit has a similar feature called `secrets.toml`. This file is stored in the `.streamlit` folder in the root directory of the project. It is used to store sensitive information like API keys, passwords, etc.

Create a `.streamlit` folder in the root directory and create a `secrets.toml` file inside it. Add the following lines to the `secrets.toml` file:

```toml
SUPABASE_URL = "YOUR_SUPABASE_URL"
SUPABASE_ANON_KEY = "YOUR_SUPABASE_ANON_KEY"
REDIRECT_URL = "http://localhost:8501/"
```

Replace `YOUR_SUPABASE_URL` and `YOUR_SUPABASE_ANON_KEY` with your Supabase URL and Supabase Anon Key respectively, which you obtained in the previous step.

⇦ [Chapter 0: Previous Work](chapter1.md) | [Chapter 2: The sign_in_with_oauth() method](chapter2.md) ⇨