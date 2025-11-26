import streamlit as st
import pandas as pd
import uuid

# Load or initialize patient data
def load_data():
    try:
        return pd.read_csv("patients.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Patient ID", "Name", "Age", "Gender", "Diagnosis"])

# Save data to CSV
def save_data(data):
    data.to_csv("patients.csv", index=False)

# Add patient
def add_patient(name, age, gender, diagnosis):
    data = load_data()
    new_id = str(uuid.uuid4())[:8]
    new_patient = {"Patient ID": new_id, "Name": name, "Age": age, "Gender": gender, "Diagnosis": diagnosis}
    data = pd.concat([data, pd.DataFrame([new_patient])], ignore_index=True)
    save_data(data)
    st.success(f"Patient '{name}' added with ID: {new_id}")

# Delete patient
def delete_patient(patient_id):
    data = load_data()
    data = data[data["Patient ID"] != patient_id]
    save_data(data)
    st.success("Patient record deleted.")

# Update patient
def update_patient(patient_id, name, age, gender, diagnosis):
    data = load_data()
    if patient_id in data["Patient ID"].values:
        data.loc[data["Patient ID"] == patient_id, ["Name", "Age", "Gender", "Diagnosis"]] = [name, age, gender, diagnosis]
        save_data(data)
        st.success("Patient record updated.")
    else:
        st.error("Patient ID not found.")

# Streamlit App
st.title("🏥 Hospital Patient Manager")
st.sidebar.title("Navigation")

menu = st.sidebar.radio("Go to", ["Add Patient", "View Patients", "Update Patient", "Delete Patient", "Export to CSV"])

if menu == "Add Patient":
    st.header("➕ Add New Patient")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diagnosis = st.text_input("Diagnosis")

    if st.button("Add Patient"):
        if name and diagnosis:
            add_patient(name, age, gender, diagnosis)
        else:
            st.warning("Please fill all required fields.")

elif menu == "View Patients":
    st.header("📋 All Patients")
    data = load_data()
    st.dataframe(data)

elif menu == "Update Patient":
    st.header("✏️ Update Patient Record")
    data = load_data()
    patient_ids = data["Patient ID"].tolist()
    
    selected_id = st.selectbox("Select Patient ID to Update", patient_ids)
    if selected_id:
        patient_row = data[data["Patient ID"] == selected_id].iloc[0]
        name = st.text_input("Name", patient_row["Name"])
        age = st.number_input("Age", min_value=0, value=int(patient_row["Age"]))
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(patient_row["Gender"]))
        diagnosis = st.text_input("Diagnosis", patient_row["Diagnosis"])

        if st.button("Update Patient"):
            update_patient(selected_id, name, age, gender, diagnosis)

elif menu == "Delete Patient":
    st.header("🗑️ Delete Patient")
    data = load_data()
    patient_ids = data["Patient ID"].tolist()

    patient_id = st.selectbox("Select Patient ID to Delete", patient_ids)

    if st.button("Delete"):
        delete_patient(patient_id)

elif menu == "Export to CSV":
    st.header("📤 Export Data to CSV")
    data = load_data()
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download CSV", data=csv, file_name='patients.csv', mime='text/csv')
