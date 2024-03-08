import streamlit as st


def check_password():
    """Returns `True` when the user enters the correct password"""

    def _password_entered() -> bool:
        """Check if the password is correct"""
        if st.session_state["password"] == st.secrets.app["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", type="password", on_change=_password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        st.text_input(
            "Password", type="password", on_change=_password_entered, key="password"
        )
        st.error("Incorrect password!")
        return False

    return True
