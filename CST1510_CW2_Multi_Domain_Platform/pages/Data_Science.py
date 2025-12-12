import streamlit as st
import pandas as pd
import os

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


# Ensure the CSV file is available
csv_file_path = 'datasets_metadata.csv'

# Check if the file exists in the current directory
if not os.path.exists(csv_file_path):
    st.error(f"CSV file not found at {csv_file_path}")
    st.stop()

# -------------------------------------------------
# LOAD + CLEAN CSV
# -------------------------------------------------
df = pd.read_csv(csv_file_path)

# CLEAN DUPLICATE / BAD COLUMN NAMES
df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df.loc[:, ~df.columns.duplicated()]

rename_map = {
    "dataset id": "dataset_id",
    "uploaded by": "uploaded_by",
    "upload date": "upload_date"
}

df = df.rename(columns=rename_map)
df = df.loc[:, ~df.columns.duplicated()]  # clean again after rename

# -------------------------------------------------
# Data Overview Display
# -------------------------------------------------
st.subheader("Data Overview")
st.dataframe(df)

# -------------------------------------------------
# Rows per Dataset (Bar chart)
# -------------------------------------------------
if 'rows' in df.columns and 'name' in df.columns:
    st.subheader("Rows per Dataset")
    st.bar_chart(df.set_index("name")["rows"])
else:
    st.warning("The required columns ('rows' and 'name') are missing in the data.")

# -------------------------------------------------
# CRUD SECTION (Create / Update / Delete)
# -------------------------------------------------
st.markdown("---")
st.subheader("Manage Datasets (Create / Update / Delete)")

# -----------------------
# CREATE DATASET
# -----------------------
with st.form("create_dataset", clear_on_submit=True):
    c_name = st.text_input("Dataset Name")
    c_rows = st.number_input("Rows", min_value=0, step=1)
    c_columns = st.number_input("Columns", min_value=0, step=1)
    c_uploaded_by = st.text_input("Uploaded By")
    c_upload_date = st.date_input("Upload Date")
    c_submitted = st.form_submit_button("Add Dataset")

    if c_submitted:
        # Auto-generate dataset_id
        if "dataset_id" in df.columns and not df.empty:
            new_dataset_id = df["dataset_id"].max() + 1
        else:
            new_dataset_id = 1

        new_data = {
            "dataset_id": new_dataset_id,
            "name": c_name,
            "rows": c_rows,
            "columns": c_columns,
            "uploaded_by": c_uploaded_by,
            "upload_date": str(c_upload_date),
        }

        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(csv_file_path, index=False)
        st.success("Dataset added successfully.")
        st.rerun()

# -----------------------
# UPDATE / DELETE DATASET
# -----------------------
if not df.empty:

    id_list = df["dataset_id"].astype(str).tolist()
    selected_id = st.selectbox("Select dataset ID to manage", id_list)

    # Get the selected row
    sel_row = df[df["dataset_id"].astype(str) == selected_id].iloc[0]

    # Safely handle NaN values
    safe_rows = 0 if pd.isna(sel_row["rows"]) else int(sel_row["rows"])
    safe_cols = 0 if pd.isna(sel_row["columns"]) else int(sel_row["columns"])
    safe_uploaded_by = "" if pd.isna(sel_row["uploaded_by"]) else sel_row["uploaded_by"]
    safe_upload_date = (
        pd.to_datetime("today").date()
        if pd.isna(sel_row["upload_date"])
        else pd.to_datetime(sel_row["upload_date"]).date()
    )

    # UPDATE
    with st.form("update_dataset"):
        u_name = st.text_input("Dataset Name", value=sel_row["name"])
        u_rows = st.number_input("Rows", min_value=0, step=1, value=safe_rows)
        u_columns = st.number_input("Columns", min_value=0, step=1, value=safe_cols)
        u_uploaded_by = st.text_input("Uploaded By", value=safe_uploaded_by)
        u_upload_date = st.date_input("Upload Date", value=safe_upload_date)

        # Only one submit button for update and delete
        action = st.form_submit_button("Update Dataset")

        if action:
            # Update the dataset
            df.loc[df["dataset_id"].astype(str) == selected_id,
                   ["name", "rows", "columns", "uploaded_by", "upload_date"]] = \
                (u_name, u_rows, u_columns, u_uploaded_by, str(u_upload_date))

            df.to_csv(csv_file_path, index=False)
            st.success("Dataset updated.")
            st.rerun()

    # Buttons for Delete
    if st.button("Delete Dataset"):
        df = df[df["dataset_id"].astype(str) != selected_id]
        df.to_csv(csv_file_path, index=False)
        st.success("Dataset deleted.")
        st.rerun()