import streamlit as st
from streamlit.source_util import page_icon_and_name

def page_start():
    if st.session_state.x:
        with st.sidebar:
            st.header("Application Menu")
            st.write("You are Signed in")
    st.header("You are Logged in")
    st.write("Logged in Content")

def authenticate_user():
        if name == 'a' and password == 'a':
            st.session_state.x = True
            st.session_state.go_page = True
            st.switch_page("pages/chartDisplay.py")
        else:
            st.write("Login Failed. Try Again.")
            st.session_state.x = False

if "x" not in st.session_state:
    st.session_state.x = False

st.set_page_config(
    page_title = "Multi-Domain Intelligence App",
    page_icon = "img/svg.jpg"
)

# Safe delayed routing
if "go_page" in st.session_state and st.session_state.go_page:
    st.session_state.go_page = False


if st.session_state.x :
    with st.sidebar:
        st.header("Application Options")
        st.write("You are signed in")

else:
    st.title("Hello")
    st.write("This will be shown on the page! ")
    name = st.text_input("username")
    password = st.text_input("password", type="password")
    if st.button("login"):
        authenticate_user()

with st.expander("See Application Details"):
    st.write("This is a Test Screen")
    st.write("I created this all by myself with no help of AI or Friends!")
    st.write("You can close this :)")
