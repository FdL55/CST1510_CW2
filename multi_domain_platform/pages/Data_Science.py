import streamlit as st
import pandas as pd
from models.dataset import Dataset

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

st.set_page_config(page_title="Data Science")
st.title("Data Science Dashboard")

# -----------------------
# LOGIN VALIDATION
# -----------------------
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.error("You must log in to access this page.")
    st.stop()

st.subheader("Uploaded Datasets Overview")

# -----------------------
# Load CSV Metadata
# -----------------------
try:
    df = pd.read_csv("datasets_metadata.csv")
except FileNotFoundError:
    st.error("Error: datasets_metadata.csv not found in root folder!")
    st.stop()

# -----------------------
# Convert rows → Objects
# -----------------------
datasets = []
for _, row in df.iterrows():
    ds = Dataset(
        dataset_id=row["dataset_id"],
        name=row["name"],
        rows=row["rows"],
        columns=row["columns"],
        uploaded_by=row["uploaded_by"],
        upload_date=row["upload_date"]
    )
    datasets.append(ds)

# -----------------------
# Convert objects → DataFrame
# -----------------------
df_display = pd.DataFrame([
    {
        "ID": d.get_id(),
        "Name": d.get_name(),
        "Rows": d.get_rows(),
        "Columns": d.get_columns(),
        "Uploaded By": d.get_uploaded_by(),
        "Upload Date": d.get_upload_date()
    }
    for d in datasets
])

st.dataframe(df_display)

# -----------------------
# Visualisation
# -----------------------
st.subheader("Rows per Dataset")
st.bar_chart(df_display.set_index("Name")["Rows"])
