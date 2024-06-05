# patient-management-system
 The Patient Management System is a Streamlit application built with Python that helps hospitals and healthcare facilities manage patient records, admissions, discharges, and generate reports. The application uses SQLite as the database to store patient information


# Features
    Register new patients with their name, age, gender, contact details, and medical history
    Admit patients to the hospital, assigning them a room number and attending doctor
    Discharge patients, recording their diagnosis, treatment received, and follow-up instructions
    Search for patients by name, contact details, or patient ID
    Generate reports in PDF or CSV format for admitted patients, discharged patients, or all patients


# Installation
    1.Clone the repository:
        `git clone https://github.com/hamid4386/patient-management-system.git`
    
    2. Install the required packages:
        `pip install streamlit pandas fpdf`

    3. Run the application:
        `streamlit run app.py`

# Usage
    1. Register a new patient by providing their details in the "Register Patient" section.
   
    2. Admit a patient by selecting their name from the list of registered patients and entering the room number and attending doctor's name.
   
    3. Discharge a patient by selecting their name from the list of admitted patients and providing their diagnosis, treatment received, and follow-up instructions.
   
    4. Search for patients by entering a search term (name, contact, or patient ID) and selecting the search criteria.
   
    5. Generate reports by selecting the report type (admitted patients, discharged patients, or all patients) and the desired export format (PDF or CSV).

# Use Cases
    The Patient Management System can be useful in the following scenarios:

    **Hospital Admissions**: The system can be used by hospital staff to register new patients, admit them to the hospital, and assign them a room and attending doctor.

    **Patient Discharge**: When a patient is ready for discharge, the system can be used to record their diagnosis, treatment received, and follow-up instructions.

    **Patient Record Management**: The system provides a centralized database to store and retrieve patient information, including their medical history, contact details, and admission/discharge records.

    **Report Generation**: Healthcare facilities can generate reports to analyze patient data, monitor admissions and discharges, and make informed decisions based on the collected information.

    **Patient Tracking**: The system allows searching for patients by name, contact details, or patient ID, enabling efficient tracking and retrieval of patient records.

# Contributing
    Contributions to the Patient Management System are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

# License
    This project is licensed under the MIT License.