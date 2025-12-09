import streamlit as st
import pandas as pd
from models.it_ticket import ITTicket

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

st.set_page_config(page_title="IT Operations")
st.title("IT Operations Dashboard")

# -----------------------
# LOGIN VALIDATION
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

st.subheader("IT Support Ticket Overview")

# -----------------------
# Load ticket CSV
# -----------------------
try:
    df = pd.read_csv("it_tickets.csv")
except FileNotFoundError:
    st.error("Error: it_tickets.csv not found in root folder!")
    st.stop()

# -----------------------
# Convert rows → Ticket Objects
# -----------------------
tickets = []
for _, row in df.iterrows():
    ticket = ITTicket(
        ticket_id=row["ticket_id"],
        priority=row["priority"],
        description=row["description"],
        status=row["status"],
        assigned_to=row["assigned_to"],
        created_at=row["created_at"],
        resolution_time_hours=row["resolution_time_hours"]
    )
    tickets.append(ticket)

# -----------------------
# Convert objects → DataFrame
# -----------------------
df_display = pd.DataFrame([
    {
        "ID": t.get_id(),
        "Priority": t.get_priority(),
        "Description": t.get_description(),
        "Status": t.get_status(),
        "Assigned To": t.get_assigned_to(),
        "Created At": t.get_created_at(),
        "Resolution Hours": t.get_resolution_time()
    }
    for t in tickets
])

st.dataframe(df_display)

# -----------------------
# Visualisation
# -----------------------
st.subheader("Tickets by Priority")
st.bar_chart(df_display["Priority"].value_counts())

st.subheader("Average Resolution Time by Priority")
resolution_avg = df_display.groupby("Priority")["Resolution Hours"].mean()
st.bar_chart(resolution_avg)
