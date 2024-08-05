<h1 align="center">Supabase-Streamlit Google OAuth</h1>
<p align="center">
  <img src="https://img.shields.io/github/license/bhargavmodak/streamlit-google-oauth" alt="License">
  <img src="https://img.shields.io/github/issues/bhargavmodak/streamlit-google-oauth" alt="Issues">
  <img src="https://img.shields.io/github/forks/bhargavmodak/streamlit-google-oauth" alt="Forks">
  <img src="https://img.shields.io/github/stars/bhargavmodak/streamlit-google-oauth" alt="Stars">
</p>
<p align="center">
  <a href="https://blank-app-template.streamlit.app/">
    <img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit">
  </a>
</p>
<p align="center">
An example of how to use Google OAuth with Supabase and Streamlit.
</p>
<hr style="height:2px;border-width:0;color:gray;background-color:gray">

There is relatively little information on how to use Google OAuth with Supabase and Streamlit, I decided to create a simple template that demonstrates how to use Google OAuth with Supabase and Streamlit.

## 🧑‍🔬 How does it work?

### ▹ Pre-requisites
   - You know what [Supabase](https://supabase.io/) is and have an account.
   - You know what [Streamlit](https://streamlit.io/) is.
   - You have a [Google Cloud Platform](https://console.cloud.google.com/) account.

### ▹ TLDR

Supabase's [Python Client](https://supabase.com/docs/reference/python/introduction) provides the [Sign in user through OAuth](https://supabase.com/docs/reference/python/auth-signinwithoauth) method to authenticate users using OAuth providers like Google, but doesn't directly open the OAuth provider's login page, and even when manually opened, returns the token pair in the [URL Fragement](https://developer.mozilla.org/en-US/docs/Web/API/URL/hash).

We prevent the token pair from being exposed indefinitely, and also use local storage to persist the token pair, by using [streamlit-js.]

It's a hacky fix, and the recommended way is to use a backend server to handle the OAuth flow, but this is a simple way to get started.

### ▹ Chapters

| Chapter                        | Title                                    |
| ------------------------------ | ---------------------------------------- |
| [Chapter 0](/docs/chapter0.md) | Previous Work                            |
| [Chapter 1](/docs/chapter1.md) | Prerequisites for Supabase and Streamlit |
| [Chapter 2](/docs/chapter2.md) | The sign_in_with_oauth() method          |
| [Chapter 3](/docs/chapter3.md) | The session object                       |
| [Chapter 4](/docs/chapter4.md) | Conclusion                               |

## How to run this project on your own machine

### 1. Clone the repository

   ```bash
   $ git clone https://github.com/bhargavmodak/streamlit-google-oauth.git
   $ cd streamlit-google-oauth
   ```

### 2. Create a virtual environment

   ```bash
   $ python -m venv venv
   $ source venv/bin/activate
   ```
   or
   ```bash
   $ python -m venv venv
   $ venv\Scripts\activate
   ```

   Note: You can also use `conda` to create a virtual environment. Learn more about it [here](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html).

### 3. Install the dependencies

   ```bash
   $ pip install -r requirements.txt
   ```

### 4. Set up Supabase and Google OAuth

Read [Chapter 1](/docs/chapter1.md) to learn how to set up Supabase and Google OAuth.

### 5. Read the docs

Read the [documentation](/docs/chapter0.md) to understand how the project works.
