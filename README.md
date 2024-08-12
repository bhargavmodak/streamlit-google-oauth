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

### ↝ Pre-requisites
   - You know what [Supabase](https://supabase.io/) is and have an account.
   - You know what [Streamlit](https://streamlit.io/) is.
   - You have a [Google Cloud Platform](https://console.cloud.google.com/) account.

### ↝ TLDR

Supabase's [Python Client](https://supabase.com/docs/reference/python/introduction) provides the [Sign in user through OAuth](https://supabase.com/docs/reference/python/auth-signinwithoauth) method to authenticate users using OAuth providers like Google, but doesn't directly open the OAuth provider's login page, and even when manually opened, returns the token pair in the [URL Fragement](https://developer.mozilla.org/en-US/docs/Web/API/URL/hash).

This demo app prevents the token pair from being exposed indefinitely, and also use local storage to persist the token pair, by using [streamlit-js.] Then it uses the token pair to set session in Supabase, and uses the session to fetch user data.

### ↝ Chapters

| Chapter                        | Title                                    |
| ------------------------------ | ---------------------------------------- |
| [Chapter 0](/docs/chapter0.md) | Previous Work                            |
| [Chapter 1](/docs/chapter1.md) | Prerequisites for Supabase and Streamlit |
| [Chapter 2](/docs/chapter2.md) | The sign_in_with_oauth() method          |
| [Chapter 3](/docs/chapter3.md) | The session object                       |
| [Chapter 4](/docs/chapter4.md) | Local Storage and the Auth Route         |
| [Chapter 5](/docs/chapter5.md) | The Home Route                           |
| [Chapter 6](/docs/chapter6.md) | Logging Out the User                     |
| [Chapter 7](/docs/chapter7.md) | Wrapping Up                              |


## 🚀 Run this project on your own machine

<!-- Create note -->
> **Note:** This project uses environment variables to store sensitive information. Please read [Chapter 1](/docs/chapter1.md) to learn how to set up Streamlit secrets

#### 1. Clone the repository

   ```bash
   $ git clone https://github.com/bhargavmodak/streamlit-google-oauth.git
   $ cd streamlit-google-oauth
   ```

#### 2. Create a virtual environment

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

#### 3. Install the dependencies

   ```bash
   $ pip install -r requirements.txt
   ```

#### 4. Set up Supabase and Google OAuth

Read [Chapter 1](/docs/chapter1.md) to learn how to set up Supabase and Google OAuth.
You might also want to read the other docs to understand how the app works.

#### 5. Run the Streamlit app

   ```bash
   $ streamlit run streamlit_app.py
   ```
   
## 🛠️ Project Maintainer

<div align="center">
   <table>
      <tbody>
         <td align="center">
            <a href="https://github.com/bhargavmodak">
               <img alt="github profile" src="https://avatars.githubusercontent.com/u/82528318?v=4" width="130px;">
               <br>
               <sub><b> Bhargav Modak </b></sub>
            </a>
            <br>
         </td>
      </tbody>
      <tbody>
         <td align="center">
            <a href="mailto:bhargav0modak@gmail.com">
               <img src="https://img.shields.io/badge/-Contact%20Me-informational?style=flat&logo=gmail&logoColor=white&color=2bbc8a" alt="Contact Me">
            </a>
            <br>
         </td>
      </tbody>
      <tbody>
         <td align="center">
            Web Developer
         </td>
      </tbody>
   </table>
</div>
