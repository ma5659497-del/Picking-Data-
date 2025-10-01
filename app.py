import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Picking Data Collector", page_icon="🌾", layout="centered")
st.title("🌾 Picking Data Collector")

# Path to your Excel file
DATA_FILE = "picking_data.xlsx"

# Load Excel
if os.path.exists(DATA_FILE):
    df = pd.read_excel(DATA_FILE)
else:
    # Create empty DataFrame if file doesn't exist
    df = pd.DataFrame(columns=[
        "Date",
        "PU Code",
        "Farmer Name",
        "Farmer CNIC",
        "Harvested Cotton Area (ha)",
        "Total seed cotton harvested (KGs)",
        "Activity 1",
        "Activity 2",
        "Activity 3"
    ])

# Picking Data Form
with st.form("picking_form", clear_on_submit=True):
    date = st.date_input("📅 Date")
    pu_code = st.text_input("PU Code")
    farmer_name = st.text_input("Farmer Name")
    farmer_cnic = st.text_input("Farmer CNIC")
    harvested_area = st.number_input("Harvested Cotton Area (ha)", min_value=0.0, step=0.1)
    seed_cotton = st.number_input("Total Seed Cotton Harvested (KGs)", min_value=0.0, step=1.0)

    st.subheader("📝 Additional Notes")
    note1 = st.text_input("Activity 1")
    note2 = st.text_input("Activity 2")
    note3 = st.text_input("Activity 3")

    submitted = st.form_submit_button("💾 Save Picking Data")

if submitted:
    # Append new row
    new_row = {
        "Date": date,
        "PU Code": pu_code,
        "Farmer Name": farmer_name,
        "Farmer CNIC": farmer_cnic,
        "Harvested Cotton Area (ha)": harvested_area,
        "Total seed cotton harvested (KGs)": seed_cotton,
        "Activity 1": note1,
        "Activity 2": note2,
        "Activity 3": note3
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save to Excel
    df.to_excel(DATA_FILE, index=False)
    st.success("✅ Picking data saved successfully!")

# Show existing records
st.subheader("📊 Saved Records")
st.dataframe(df)
