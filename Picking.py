import streamlit as st
import pandas as pd
import os

st.title("Farmer Data Collector (Update Existing Records)")

# Path to your master Excel file
DATA_FILE = "farmers_master.xlsx"

# Load Excel
if os.path.exists(DATA_FILE):
    df = pd.read_excel(DATA_FILE)
else:
    st.error("Farmer master file not found! Please upload farmers_master.xlsx")
    st.stop()

# Select Farmer
farmer_id = st.selectbox("Select Farmer by CNIC", df["Farmer CNIC"].unique())

# Get Farmer Record
farmer_record = df[df["Farmer CNIC"] == farmer_id].iloc[0]

st.subheader(f"Updating data for {farmer_record['Farmer Name']} (CNIC: {farmer_id})")

# Editable form with all fields
with st.form("update_form", clear_on_submit=False):
    col1, col2, col3 = st.columns(3)

    with col1:
        pp = st.text_input("PP", value=farmer_record["PP"])
        pu_code = st.text_input("PU Code", value=farmer_record["PU Code"])
        lg_code = st.text_input("LG/Hub Code", value=farmer_record["LG/Hub Code"])
        village = st.text_input("Village", value=farmer_record["Village"])
        mf_code = st.text_input("MF Code", value=farmer_record["MF Code"])

    with col2:
        farmer_name = st.text_input("Farmer Name", value=farmer_record["Farmer Name"])
        father_name = st.text_input("Father Name", value=farmer_record["Father Name"])
        cnic = st.text_input("Farmer CNIC", value=farmer_record["Farmer CNIC"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male","Female","Other"].index(farmer_record["Gender"]))
        contact = st.text_input("Contact Number", value=str(farmer_record["Contact Number"]))

    with col3:
        dob_year = st.number_input("Farmer DOB - Year", min_value=1900, max_value=2100, value=int(farmer_record["Farmer DOB - Year"]))
        education = st.text_input("Education", value=farmer_record["Education"])
        joining_date = st.text_input("Farmer Date of joining", value=str(farmer_record["Farmer Date of joining"]))
        sowing_date = st.text_input("Sowing Date", value=str(farmer_record["Sowing  Date"]))
        active = st.selectbox("Active/Inactive", ["Active", "Inactive"], index=["Active","Inactive"].index(farmer_record["Active/ Inactive"]))
        status = st.text_input("Farmer Status", value=farmer_record["Farmer Status"])
        continuity = st.text_input("Farmer Continuity", value=farmer_record["Farmer Continuity"])

    st.subheader("Land & Yield")
    cultivable_land = st.number_input("Total cultivable Land (ha)", value=float(farmer_record["Total cultivable Land (ha)"]))
    cotton_land = st.number_input("Total Land under Cotton Production (ha)", value=float(farmer_record["Total Land under Cotton Production (ha)"]))
    avg_yield = st.number_input("Average Yield (kg/ha)", value=float(farmer_record["Average Yield  (kg / ha)"]))

    st.subheader("Seed Cotton Transactions")
    transactions = []
    total_sold = 0
    for i in range(1, 7):
        sold = st.number_input(f"Seed Cotton Sold {i} (KGs)", value=float(farmer_record.get(f"Seed Cotton Sold in {['First','Second','Third','Fourth','Fifth','Sixth'][i-1]} Transaction KGs", 0)))
        date = st.text_input(f"Date of Selling {i}", value=str(farmer_record.get(f"Date of Selling", "")))
        buyer = st.text_input(f"Buyer Name {i}", value=str(farmer_record.get(f"Buyer Name", "")))
        buyer_contact = st.text_input(f"Buyer Contact {i}", value=str(farmer_record.get(f"Buyers Contact number", "")))
        transactions.extend([sold, date, buyer, buyer_contact])
        total_sold += sold

    submitted = st.form_submit_button("💾 Save Updates")

if submitted:
    # Update row
    row_index = df[df["Farmer CNIC"] == farmer_id].index[0]

    df.loc[row_index, "PP"] = pp
    df.loc[row_index, "PU Code"] = pu_code
    df.loc[row_index, "LG/Hub Code"] = lg_code
    df.loc[row_index, "Village"] = village
    df.loc[row_index, "MF Code"] = mf_code
    df.loc[row_index, "Farmer Name"] = farmer_name
    df.loc[row_index, "Father Name"] = father_name
    df.loc[row_index, "Farmer CNIC"] = cnic
    df.loc[row_index, "Gender"] = gender
    df.loc[row_index, "Contact Number"] = contact
    df.loc[row_index, "Farmer DOB - Year"] = dob_year
    df.loc[row_index, "Education"] = education
    df.loc[row_index, "Farmer Date of joining"] = joining_date
    df.loc[row_index, "Sowing  Date"] = sowing_date
    df.loc[row_index, "Active/ Inactive"] = active
    df.loc[row_index, "Farmer Status"] = status
    df.loc[row_index, "Farmer Continuity"] = continuity
    df.loc[row_index, "Total cultivable Land (ha)"] = cultivable_land
    df.loc[row_index, "Total Land under Cotton Production (ha)"] = cotton_land
    df.loc[row_index, "Average Yield  (kg / ha)"] = avg_yield

    # Transactions
    for i in range(1, 7):
        df.loc[row_index, f"Seed Cotton Sold {i} (KGs)"] = transactions[(i-1)*4]
        df.loc[row_index, f"Date of Selling {i}"] = transactions[(i-1)*4 + 1]
        df.loc[row_index, f"Buyer Name {i}"] = transactions[(i-1)*4 + 2]
        df.loc[row_index, f"Buyer Contact {i}"] = transactions[(i-1)*4 + 3]

    df.loc[row_index, "Total Quantity Sold in KGs"] = total_sold

    # Save back to Excel
    df.to_excel(DATA_FILE, index=False)
    st.success("✅ Farmer record updated successfully!")
