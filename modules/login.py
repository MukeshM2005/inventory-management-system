import streamlit as st
from database import create_user, verify_user


def show_login_page():

    st.title("Inventory Management System")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # ------------------------------
    # LOGIN TAB
    # ------------------------------
    with tab1:

        st.subheader("Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_button"):

            user = verify_user(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]
                st.session_state.user_id = user["id"]

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid username or password")

    # ------------------------------
    # SIGNUP TAB
    # ------------------------------
    with tab2:

        st.subheader("Create Account")

        new_username = st.text_input("New Username", key="signup_username")
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        role = st.selectbox("Role", ["staff", "admin"], key="signup_role")

        if st.button("Create Account", key="signup_button"):

            if new_password != confirm_password:
                st.error("Passwords do not match")

            else:

                success = create_user(new_username, new_email, new_password, role)

                if success:
                    st.success("Account created successfully!")
                else:
                    st.error("Error creating account")