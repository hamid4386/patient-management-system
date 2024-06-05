import streamlit as st
import pandas as pd
import sqlite3
from datetime import date
from fpdf import FPDF

# Connect to the database
try:
    conn = sqlite3.connect('patient_records.db')
    c = conn.cursor()
except sqlite3.Error as e:
    st.error(f"An error occurred while connecting to the database: {e}")

# Create a table to store patient records
try:
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (name TEXT, age INTEGER, gender TEXT, contact TEXT, history TEXT, admitted BOOLEAN, admission_date TEXT, discharge_date TEXT, room INTEGER, doctor TEXT, diagnosis TEXT, treatment TEXT, follow_up TEXT, patient_id TEXT)''')
except sqlite3.Error as e:
    st.error(f"An error occurred while creating the table: {e}")

# Function to register a new patient
def register_patient():
    name = st.text_input("Enter patient name")
    age = st.number_input("Enter patient age", min_value=0, step=1)
    gender = st.selectbox("Select gender", ["Male", "Female", "Other"])
    contact = st.text_input("Enter contact details")
    history = st.text_area("Enter medical history")
    patient_id = st.text_input("Enter patient ID (optional)", key="patient_id")
    if age < 18:
        b_form_number = st.text_input("Enter B-form Number (for patients under 18)", key="b_form_number")
        if not patient_id and not b_form_number:
            st.warning("Please enter either Patient ID or B-form Number for patients under 18.")
            return

    if st.button("Register Patient"):
        if age < 18 and not patient_id:
            patient_id = b_form_number
        try:
            c.execute("INSERT INTO patients (name, age, gender, contact, history, admitted, admission_date, discharge_date, room, doctor, diagnosis, treatment, follow_up, patient_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (name, age, gender, contact, history, False, date.today(), None, None, None, None, None, None, patient_id))
            conn.commit()
            st.success("Patient registered successfully!")
        except sqlite3.Error as e:
            st.error(f"An error occurred while registering the patient: {e}")

# Function to admit a patient
def admit_patient():
    patient_name = st.selectbox("Select patient", [p[0] for p in c.execute("SELECT name FROM patients WHERE admitted = 0")])
    room_number = st.number_input("Enter room number", min_value=1, step=1)
    doctor_name = st.text_input("Enter attending doctor's name")

    if st.button("Admit Patient"):
        try:
            c.execute("UPDATE patients SET admitted = 1, admission_date = ?, discharge_date = ?, room = ?, doctor = ? WHERE name = ?", (date.today(), None, room_number, doctor_name, patient_name))
            conn.commit()
            st.success(f"Patient {patient_name} admitted to room {room_number} with doctor {doctor_name}.")
        except sqlite3.Error as e:
            st.error(f"An error occurred while admitting the patient: {e}")

# Function to discharge a patient
def discharge_patient():
    patient_name = st.selectbox("Select patient", [p[0] for p in c.execute("SELECT name FROM patients WHERE admitted = 1")])
    diagnosis = st.text_input("Enter patient's diagnosis")
    treatment = st.text_area("Enter treatment received")
    follow_up = st.text_area("Enter follow-up instructions")

    if st.button("Discharge Patient"):
        try:
            c.execute("UPDATE patients SET admitted = 0, discharge_date = ?, room = ?, doctor = ?, diagnosis = ?, treatment = ?, follow_up = ? WHERE name = ?",
                      (date.today(), None, None, diagnosis, treatment, follow_up, patient_name))
            conn.commit()
            st.success(f"Patient {patient_name} discharged from the hospital.")
        except sqlite3.Error as e:
            st.error(f"An error occurred while discharging the patient: {e}")

# Function to search for patients
def search_patients():
    search_term = st.text_input("Enter search term (name, contact, or ID)")
    search_by = st.selectbox("Search by", ["Name", "Contact", "ID"])

    try:
        if search_by == "Name":
            c.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + search_term + '%',))
        elif search_by == "Contact":
            c.execute("SELECT * FROM patients WHERE contact LIKE ?", ('%' + search_term + '%',))
        else:
            c.execute("SELECT * FROM patients WHERE patient_id LIKE ?", ('%' + search_term + '%',))

        search_results = c.fetchall()

        if search_results:
            st.write("Search Results:")
            df = pd.DataFrame(search_results, columns=['Name', 'Age', 'Gender', 'Contact', 'History', 'Admitted', 'Admission Date', 'Discharge Date', 'Room', 'Doctor', 'Diagnosis', 'Treatment', 'Follow-up', 'Patient ID'])
            st.dataframe(df)
        else:
            st.write("No matching patients found.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while searching for patients: {e}")


def generate_report():
    report_type = st.selectbox("Select report type", ["Admitted Patients", "Discharged Patients", "All Patients"])
    export_format = st.selectbox("Select export format", ["PDF", "CSV"])

    try:
        if report_type == "Admitted Patients":
            c.execute("SELECT * FROM patients WHERE admitted = 1")
        elif report_type == "Discharged Patients":
            c.execute("SELECT * FROM patients WHERE admitted = 0 AND discharge_date IS NOT NULL")
        else:
            c.execute("SELECT * FROM patients")

        report_data = c.fetchall()

        if report_data:
            if export_format == "PDF":
                generate_pdf_report(report_data, report_type)
            else:
                generate_csv_report(report_data, report_type)
        else:
            st.write(f"No data found for {report_type} report.")
    except sqlite3.Error as e:
        st.error(f"An error occurred while generating the report: {e}")

# Function to generate PDF reports
def generate_pdf_report(report_data, report_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add report title
    pdf.cell(200, 10, txt=f"{report_type} Report", ln=1, align="C")

    # Add table headers
    headers = ["Name", "Age", "Gender", "Contact", "History", "Admitted", "Admission Date", "Discharge Date", "Room", "Doctor", "Diagnosis", "Treatment", "Follow-up", "Patient ID"]
    for header in headers:
        pdf.cell(40, 10, txt=header, border=1)
    pdf.ln()

    # Add table data
    for row in report_data:
        for col in row:
            pdf.cell(40, 10, txt=str(col), border=1)
        pdf.ln()

    # Save and display the PDF report
    pdf_report = pdf.output(dest="S").encode("latin-1")
    st.download_button(
        label=f"Download {report_type} Report",
        data=pdf_report,
        file_name=f"{report_type}_report.pdf",
        mime="application/pdf",
    )

# Function to generate CSV reports (existing code)
def generate_csv_report(report_data, report_type):
    df = pd.DataFrame(report_data, columns=['Name', 'Age', 'Gender', 'Contact', 'History', 'Admitted', 'Admission Date', 'Discharge Date', 'Room', 'Doctor', 'Diagnosis', 'Treatment', 'Follow-up', 'Patient ID'])
    csv_report = df.to_csv(index=False)
    st.download_button(
        label=f"Download {report_type} Report",
        data=csv_report,
        file_name=f"{report_type}_report.csv",
        mime="text/csv",
    )

# Streamlit app
def main():
    st.title("Patient Management System")

    menu = ["Register Patient", "Admit Patient", "Discharge Patient", "Search Patients", "Generate Report"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Register Patient":
        register_patient()
    elif choice == "Admit Patient":
        admit_patient()
    elif choice == "Discharge Patient":
        discharge_patient()
    elif choice == "Search Patients":
        search_patients()
    elif choice == "Generate Report":
        generate_report()

if __name__ == "__main__":
    main()