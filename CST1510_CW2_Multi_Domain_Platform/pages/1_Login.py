import streamlit as st
import sqlite3
import bcrypt
from dbHelper import connect_database

# Hide Streamlit default sidebar nav
st.markdown("""
    <style>
        /* Hide built-in page navigation */
        div[data-testid="stSidebarNav"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📌 Navigation")

st.sidebar.page_link("Home.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Login.py", label="🔐 Login")
st.sidebar.page_link("pages/Cybersecurity.py", label="🛡️ Cybersecurity")
st.sidebar.page_link("pages/Data_Science.py", label="📊 Data Science")
st.sidebar.page_link("pages/IT_Operations.py", label="🛠️ IT Operations")
st.sidebar.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")


st.set_page_config(page_title="Login / Register", page_icon="🔐")

# -------------------------------
# BCRYPT HASHING FUNCTIONS
# -------------------------------
def hash_password(password: str) -> str:
    """Return a secure bcrypt hash."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify bcrypt password."""
    return bcrypt.checkpw(password.encode(), hashed.encode())


# -------------------------------
# PAGE MODE SWITCHER
# -------------------------------
mode = st.radio("Select an option:", ["Login", "Register"], horizontal=True)


# ======================================================
# 🔑 LOGIN SECTION
# ======================================================
if mode == "Login":
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = connect_database()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()

        if user and verify_password(password, user["password_hash"]):
            st.success(f"Welcome back, {username}! 🎉")

            # Set session state
            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            st.switch_page("Home.py")   # Redirect to home
        else:
            st.error("Invalid username or password.")


# ======================================================
# 📝 REGISTER SECTION
# ======================================================
else:
    st.title("📝 Create a New Account")

    username = st.text_input("Choose a username")
    password = st.text_input("Choose a password", type="password")
    password2 = st.text_input("Confirm password", type="password")

    if st.button("Create Account"):
        # Basic validation
        if password != password2:
            st.error("Passwords do not match!")
        elif len(username.strip()) < 3:
            st.error("Username must be at least 3 characters long.")
        elif len(password) < 4:
            st.error("Password must be at least 4 characters long.")
        else:
            conn = connect_database()
            cur = conn.cursor()

            # Check if username already exists
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
            if cur.fetchone():
                st.error("This username already exists. Try another one.")
            else:
                hashed_pw = hash_password(password)

                # Insert new user
                cur.execute("""
                    INSERT INTO users (username, password_hash)
                    VALUES (?, ?)
                """, (username, hashed_pw))

                conn.commit()
                st.success("Account created successfully! 🎉")
                st.info("You can now switch back to Login and sign in.")

            conn.close()
