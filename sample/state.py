import jwt
import streamlit as st


# Function to get user data from the access token
def get_user(access_token):
    try:
        data = jwt.decode(access_token, options={"verify_signature": False})
        user_metadata = data["user_metadata"]
        user = {
            "email": user_metadata["email"],
            "full_name": user_metadata["full_name"],
            "name": user_metadata["name"],
            "avatar_url": user_metadata["avatar_url"],
        }
        return user
    except Exception as e:
        st.write("Error:", e)
