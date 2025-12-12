import streamlit as st
from dbHelper import init_db
init_db()

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

st.sidebar.page_link("pages/Home.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Login.py", label="🔐 Login")
st.sidebar.page_link("pages/Cybersecurity.py", label="🛡️ Cybersecurity")
st.sidebar.page_link("pages/Data_Science.py", label="📊 Data Science")
st.sidebar.page_link("pages/IT_Operations.py", label="🛠️ IT Operations")
st.sidebar.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")

st.set_page_config(page_title="Home")

# -----------------------
# LOGIN CHECK
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access the platform.")
    st.stop()

# -----------------------
# Page Title
# -----------------------
st.title("🏠 Multi-Domain Intelligence Platform")
st.write(
    "Welcome to your dashboard 🎉. "
    "Choose a domain from below ⏬ or from the sidebar ⬅️ to explore insights."
)

# -----------------------
# Domain Cards (Aligned)
# -----------------------

st.subheader("Available Domains")

col1, col2 = st.columns(2)

CARD_STYLE = """
    <div style="
        background-color:#1e1e1e;
        padding:20px;
        border-radius:12px;
        border:1px solid #333;
        margin-bottom:20px;
        height:150px;
        display:flex;
        flex-direction:column;
        justify-content:center;
    ">
        <h3 style="margin:0; font-size:22px;">{title}</h3>
        <p style="margin-top:10px; color:#ccc; font-size:16px;">{desc}</p>
    </div>
"""

# ---- LEFT COLUMN ----
with col1:

    if st.button("🛡️ Cybersecurity", use_container_width=True):
        st.switch_page("pages/Cybersecurity.py")
    st.markdown(CARD_STYLE.format(
        title="🛡️ Cybersecurity",
        desc="View cyber incident activity, severity, and attack patterns."
    ), unsafe_allow_html=True)

    if st.button("📊 Data Science", use_container_width=True):
        st.switch_page("pages/Data_Science.py")
    st.markdown(CARD_STYLE.format(
        title="📊 Data Science",
        desc="Explore datasets, metadata, and statistics."
    ), unsafe_allow_html=True)


# ---- RIGHT COLUMN ----
with col2:

    if st.button("🛠️ IT Operations", use_container_width=True):
        st.switch_page("pages/IT_Operations.py")
    st.markdown(CARD_STYLE.format(
        title="🛠️ IT Operations",
        desc="Monitor support tickets and operational workload."
    ), unsafe_allow_html=True)

    # 🔥 FIXED — use the correct file name here
    if st.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/3_AI_Assistant.py")

    st.markdown(CARD_STYLE.format(
        title="🤖 AI Assistant",
        desc="Ask questions, analyse data, and get automated help."
    ), unsafe_allow_html=True)