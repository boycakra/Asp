import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for saving data
DATA_FILE = "production_data.csv"

# Function to load data from CSV or initialize empty list
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE).to_dict("records")
    else:
        return []

# Function to save data to CSV
def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_FILE, index=False)

# Initialize session state with loaded data
if "data" not in st.session_state:
    st.session_state.data = load_data()

st.title("📋 Production Data Entry")

# Side-by-side input fields for Date and Shift
col1, col2 = st.columns(2)
with col1:
    date = st.date_input("📅 Date", datetime.today())
with col2:
    shift = st.selectbox("👨‍🏭 Shift", ["non shift (komsah)", "shift a (desi & komsah)"])

# Side-by-side input fields for Material, Size, and Time
col1, col2, col3 = st.columns(3)
with col1:
    material = st.selectbox("🛠 Material", ["Softmax", "hyclons"])
with col2:
    size = st.selectbox("📏 Size", ["4", "5", "6", "7", "7T", "8", "9", "10", "11", "12"])
with col3:
    time = st.selectbox("⏰Time", [f"{h} AM" for h in range(7, 12)] + [f"{h} PM" for h in range(1, 5)])

# Side-by-side input fields for Model, Quantity, and Reworks Quantity
col1, col2, col3 = st.columns(3)
with col1:
    model = st.selectbox("👟Model", ["NSM", "Shox", "Ride"])
with col2:
    quantity = st.number_input("📦 Quantity", min_value=0, value=0, step=1)
with col3:
    reworks = st.number_input("🔄 Reworks Quantity", min_value=0, value=0, step=1)

# Calculate Reworks Percentage
reworks_percent = (reworks / quantity * 100) if quantity > 0 else 0
down_time = st.selectbox("⏳ Down Time", [f"{i} minutes" for i in range(15, 121, 15)])

# Function for grouped input fields
def grouped_inputs(label):
    col1, col2, col3 = st.columns(3)
    with col1:
        P = st.number_input(f"{label}_P", min_value=0, value=0, step=1)
    with col2:
        R = st.number_input(f"{label}_R", min_value=0, value=0, step=1)
    with col3:
        L = st.number_input(f"{label}_L", min_value=0, value=0, step=1)
    return P, R, L

st.write("### Production Details")

T_H_P, T_H_R, T_H_L = grouped_inputs("T&H")
M_M_P, M_M_R, M_M_L = grouped_inputs("M&M")
PNC_P, PNC_R, PNC_L = grouped_inputs("PNC")
CS_P, CS_R, CS_L = grouped_inputs("CS")
WSP_P, WSP_R, WSP_L = grouped_inputs("WSP")
WSPRINT_P, WSPRINT_R, WSPRINT_L = grouped_inputs("WSPRINT")
DFM_P, DFM_R, DFM_L = grouped_inputs("DFM")
Other_P, Other_R, Other_L = grouped_inputs("Other")

# Save data
if st.button("Save Entry"):
    new_entry = {
        "Date": date, "Shift": shift, "Time": time, "Model": model, "Material": material,
        "Size": size, "Quantity": quantity, "Reworks Quantity": reworks, "Reworks %": reworks_percent,
        "Down Time": down_time, "T&H_P": T_H_P, "T&H_R": T_H_R, "T&H_L": T_H_L,
        "M&M_P": M_M_P, "M&M_R": M_M_R, "M&M_L": M_M_L, "PNC_P": PNC_P, "PNC_R": PNC_R,
        "PNC_L": PNC_L, "CS_P": CS_P, "CS_R": CS_R, "CS_L": CS_L, "WSP_P": WSP_P,
        "WSP_R": WSP_R, "WSP_L": WSP_L, "WSPRINT_P": WSPRINT_P, "WSPRINT_R": WSPRINT_R,
        "WSPRINT_L": WSPRINT_L, "DFM_P": DFM_P, "DFM_R": DFM_R, "DFM_L": DFM_L,
        "Other_P": Other_P, "Other_R": Other_R, "Other_L": Other_L
    }
    st.session_state.data.append(new_entry)
    save_data(st.session_state.data)
    st.success("Entry saved!")
    st.rerun()  # Rerun the script to update the dataframe

# Convert to DataFrame and display
df = pd.DataFrame(st.session_state.data)

st.write("### Production Data Table")
st.dataframe(df)

# Select box to delete a row
if not df.empty:
    st.write("### Delete Entry")
    row_to_delete = st.selectbox("Select row to delete", df.index.tolist())

    if st.button("Delete Row"):
        del st.session_state.data[row_to_delete]
        save_data(st.session_state.data)
        st.success(f"Deleted row {row_to_delete}")
        st.rerun()  # Rerun the script to update the dataframe

# Save to CSV
if st.button("Download CSV"):
    df.to_csv("production_data.csv", index=False)
    st.success("Data saved as production_data.csv")
