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

# -----------------------
# CRUD SECTION (Create / Update / Delete)
# -----------------------
st.markdown("---")
st.subheader("Manage Tickets (Create / Update / Delete)")

# -----------------------
# CREATE TICKET
# -----------------------
with st.form("create_ticket", clear_on_submit=True):
    c_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
    c_description = st.text_area("Description")
    c_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
    c_assigned_to = st.text_input("Assigned To")
    c_created_at = st.date_input("Created At")
    c_resolution_time = st.number_input("Resolution Time (hours)", min_value=0, step=1)
    c_submitted = st.form_submit_button("Add Ticket")

    if c_submitted:
        # Auto-generate ticket_id
        if "ticket_id" in df.columns and not df.empty:
            new_ticket_id = df["ticket_id"].max() + 1
        else:
            new_ticket_id = 1

        new_data = {
            "ticket_id": new_ticket_id,
            "priority": c_priority,
            "description": c_description,
            "status": c_status,
            "assigned_to": c_assigned_to,
            "created_at": str(c_created_at),
            "resolution_time_hours": c_resolution_time,
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv("it_tickets.csv", index=False)
        st.success("Ticket added successfully.")
        st.rerun()

# -----------------------
# UPDATE / DELETE TICKET
# -----------------------
if not df.empty:

    id_list = df["ticket_id"].astype(str).tolist()
    selected_id = st.selectbox("Select ticket ID to manage", id_list)

    # Get the selected row
    sel_row = df[df["ticket_id"].astype(str) == selected_id].iloc[0]

    with st.form("update_delete_form"):
        u_priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"], index=["Low", "Medium", "High", "Critical"].index(sel_row["priority"]))
        u_description = st.text_area("Description", value=sel_row["description"])
        u_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open", "In Progress", "Resolved", "Closed"].index(sel_row["status"]))
        u_assigned_to = st.text_input("Assigned To", value=sel_row["assigned_to"])
        u_created_at = st.date_input("Created At", value=pd.to_datetime(sel_row["created_at"]).date())
        u_resolution_time = st.number_input("Resolution Time (hours)", min_value=0, step=1, value=int(sel_row["resolution_time_hours"]))

        # Update and Delete buttons
        update_btn = st.form_submit_button("Update")
        delete_btn = st.form_submit_button("Delete")

        # Handle Update action
        if update_btn:
            df.loc[df["ticket_id"].astype(str) == selected_id,
                   ["priority", "description", "status", "assigned_to", "created_at", "resolution_time_hours"]] = \
                (u_priority, u_description, u_status, u_assigned_to, str(u_created_at), u_resolution_time)

            df.to_csv("it_tickets.csv", index=False)
            st.success("Ticket updated.")
            st.rerun()

        # Handle Delete action
        if delete_btn:
            df = df[df["ticket_id"].astype(str) != selected_id]
            df.to_csv("it_tickets.csv", index=False)
            st.success("Ticket deleted.")
            st.rerun()
