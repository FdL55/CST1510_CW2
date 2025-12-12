import streamlit as st
import pandas as pd

# Hide Streamlit default sidebar nav
st.markdown("""
    <style>
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

st.set_page_config(page_title="Cybersecurity")
st.title("Cyber Incidents")

from models.security_incident import SecurityIncident
from services.database_manager import DatabaseManager

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

st.title("Cybersecurity Incidents - OOP Visualisation")

db = DatabaseManager("cyberincidents.db")
db.connect()

rows = db.fetch_all(
    "SELECT id, i_date, i_type, severity, status, description FROM cyber_incidents ORDER BY id ASC"
)

incidents = []
for r in rows:
    incident = SecurityIncident(
        incident_id=r[0],
        incident_type=r[2],
        severity=r[3],
        status=r[4],
        description=r[5]
    )
    incidents.append(incident)

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

st.subheader("Data Overview")
st.dataframe(df)

st.subheader("Incidents by Type")
type_counts = df["i_type"].value_counts()
st.bar_chart(type_counts)

st.markdown("---")
st.subheader("Manage Incidents (Create / Update / Delete)")

# -----------------------
# CREATE INCIDENT (Updated)
# -----------------------
with st.form("create_incident", clear_on_submit=True):
    c_id = st.number_input("Incident ID", min_value=1, step=1)  # Added
    c_i_date = st.date_input("Incident Date")
    c_i_type = st.text_input("Incident Type")
    c_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    c_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    c_description = st.text_area("Description")
    c_submitted = st.form_submit_button("Add Incident")

    if c_submitted:
        db.execute_query(
            """
            INSERT INTO cyber_incidents
            (id, i_date, i_type, severity, status, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (int(c_id), str(c_i_date), c_i_type, c_severity, c_status, c_description)
        )
        st.success("Incident added successfully.")
        st.rerun()

# -----------------------
# UPDATE / DELETE INCIDENT
# -----------------------
if not df.empty:

    # Remove NaN and invalid IDs
    clean_df = df[df["id"].notna() & df["id"].apply(lambda x: str(x).replace('.', '', 1).isdigit())]

    if clean_df.empty:
        st.error("No valid IDs found in the database.")
    else:
        id_list = clean_df["id"].astype(str).tolist()

        selected_id = st.selectbox("Select incident ID to manage", id_list)

        sel_row = clean_df[clean_df["id"].astype(str) == selected_id].iloc[0]

        with st.form("update_incident"):
            u_i_type = st.text_input("Incident Type", value=sel_row["i_type"])

            severity_options = ["Low", "Medium", "High", "Critical"]
            status_options = ["Open", "In Progress", "Resolved", "Closed"]

            try:
                sev_index = severity_options.index(sel_row["severity"])
            except:
                sev_index = 0

            try:
                stat_index = status_options.index(sel_row["status"])
            except:
                stat_index = 0

            u_severity = st.selectbox("Severity", severity_options, index=sev_index)
            u_status = st.selectbox("Status", status_options, index=stat_index)
            u_description = st.text_area("Description", value=sel_row["description"])

            update_btn = st.form_submit_button("Update Incident")
            delete_btn = st.form_submit_button("Delete Incident")

            if update_btn:
                db.execute_query(
                    "UPDATE cyber_incidents SET i_type=?, severity=?, status=?, description=? WHERE id=?",
                    (u_i_type, u_severity, u_status, u_description, int(float(selected_id)))
                )
                st.success("Incident updated.")
                st.rerun()

            if delete_btn:
                db.execute_query(
                    "DELETE FROM cyber_incidents WHERE id=?",
                    (int(float(selected_id)),)
                )
                st.success("Incident deleted.")
                st.rerun()

db.close()