import streamlit as st
import pandas as pd

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

st.set_page_config(page_title="Cybersecurity")
st.title("Cybersecurity")

from models.security_incident import SecurityIncident

# -----------------------
# LOGIN VALIDATION
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

st.title("Cybersecurity Incidents - OOP Visualisation")

# -----------------------
# Load CSV instead of Database
# -----------------------
try:
    df_raw = pd.read_csv("cyber_incidents.csv")
except FileNotFoundError:
    st.error("❌ Could not find 'cyber_incidents.csv' in the project root folder.")
    st.stop()

# -----------------------
# Convert CSV rows → OOP Objects
# -----------------------
incidents = []
for _, row in df_raw.iterrows():
    incident = SecurityIncident(
        incident_id=row["id"],
        incident_type=row["i_type"],
        severity=row["severity"],
        status=row["status"],
        description=row["description"]
    )
    incidents.append(incident)

# -----------------------
# Convert Objects → DataFrame
# -----------------------
df = pd.DataFrame([
    {
        "id": i.get_id(),
        "i_type": i.get_incident_type(),
        "severity": i.get_severity(),
        "status": i.get_status(),
        "description": i.get_description()
    }
    for i in incidents
])

# -----------------------
# Page Display
# -----------------------
st.subheader("Data Overview")
st.dataframe(df)

st.subheader("Incidents by Type")
type_counts = df["i_type"].value_counts()
st.bar_chart(type_counts)
