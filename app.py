import streamlit as st
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
MASTER_FILE = DATA_DIR / "master.xlsx"
PICKING_FILE = DATA_DIR / "picking_data.xlsx"

# Load master farmer data
@st.cache_data
def load_master():
    return pd.read_excel(MASTER_FILE)

# Save picking data
def save_picking(record):
    if PICKING_FILE.exists():
        df = pd.read_excel(PICKING_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
    df.to_excel(PICKING_FILE, index=False)

st.title("Farmer Picking Data Entry")

master_df = load_master()

# Select farmer
farmer_id = st.selectbox("Select Farmer ID", master_df["FarmerID"].unique())

# Display farmer details
farmer_row = master_df[master_df["FarmerID"] == farmer_id].iloc[0]
st.write("**Farmer Name:**", farmer_row["FarmerName"])
st.write("**PU:**", farmer_row["PU"])

# Input picking details
date = st.date_input("Picking Date")
weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
quality = st.selectbox("Quality", ["Good", "Average", "Poor"])
remarks = st.text_area("Remarks")

if st.button("Save Picking Record"):
    record = {
        "FarmerID": farmer_id,
        "FarmerName": farmer_row["FarmerName"],
        "PU": farmer_row["PU"],
        "Date": str(date),
        "Weight": weight,
        "Quality": quality,
        "Remarks": remarks
    }
    save_picking(record)
    st.success("✅ Record saved successfully!")
