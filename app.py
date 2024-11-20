import os
import pickle
import streamlit as st

# Set page configuration
st.set_page_config(page_title="Preeclampsia Prediction App",
                   layout="wide",
                   page_icon="🧑‍⚕️")

# Load the saved Preeclampsia model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trained_model.sav')
preeclampsia_model = pickle.load(open(model_path, 'rb'))

# Sidebar navigation
st.sidebar.title("Navigation")
user_role = st.sidebar.selectbox("Select your role", ["Select", "Patient", "Doctor"])

# Function for patient login
def patient_login():
    st.sidebar.title("Patient Login")
    patient_email = st.sidebar.text_input("Email")
    patient_name = st.sidebar.text_input("Name")
    if st.sidebar.button("Login"):
        st.success(f"Welcome, {patient_name}!")
        return True
    return False

# Function for doctor login
def doctor_login():
    st.sidebar.title("Doctor Login")
    doctor_id = st.sidebar.text_input("Doctor ID")
    doctor_name = st.sidebar.text_input("Name")
    if st.sidebar.button("Login"):
        st.success(f"Welcome, Dr. {doctor_name}!")
        return True
    return False

# Function to validate float inputs
def validate_float(input_value, field_name):
    try:
        value = float(input_value)
        return value
    except ValueError:
        st.warning(f"Please enter a valid number for {field_name}.")
        return None

# Patient input form with validation
def get_patient_input():
    col1, col2, col3 = st.columns(3)
    with col1: age = validate_float(st.text_input('Age'), 'Age')
    with col2: gest_age = validate_float(st.text_input('Gestational Age'), 'Gestational Age')
    with col3: height = validate_float(st.text_input('Height (cm)'), 'Height')
    with col1: weight = validate_float(st.text_input('Weight (kg)'), 'Weight')
    
    # Calculate BMI if height and weight are valid
    bmi = None
    if height and weight:
        height_m = height / 100  # convert cm to meters
        bmi = weight / (height_m ** 2)
        st.write(f"Calculated BMI: {bmi:.2f}")

    with col3: sysbp = validate_float(st.text_input('Systolic Blood Pressure'), 'Systolic Blood Pressure')
    with col1: diabp = validate_float(st.text_input('Diastolic Blood Pressure'), 'Diastolic Blood Pressure')
    
    return [age, gest_age, height, weight, bmi, sysbp, diabp]

# Doctor input form with validation
def get_doctor_input():
    col1, col2, col3 = st.columns(3)
    with col1: hb = validate_float(st.text_input('Hemoglobin (hb)'), 'Hemoglobin')
    with col2: pcv = validate_float(st.text_input('Packed Cell Volume (pcv)'), 'Packed Cell Volume')
    with col3: tsh = validate_float(st.text_input('Thyroid-Stimulating Hormone (tsh)'), 'Thyroid-Stimulating Hormone')
    with col1: platelet = validate_float(st.text_input('Platelet count'), 'Platelet count')
    with col2: creatinine = validate_float(st.text_input('Creatinine'), 'Creatinine')
    with col3: plgf_sflt = validate_float(st.text_input('PLGF/sFlt-1 Ratio'), 'PLGF/sFlt-1 Ratio')
    with col1: seng = validate_float(st.text_input('Soluble Endoglin (sEng)'), 'Soluble Endoglin')
    with col2: cysc = validate_float(st.text_input('Cystatin C (cysC)'), 'Cystatin C')
    with col3: pp_13 = validate_float(st.text_input('PAPP-A (pp_13)'), 'PAPP-A')
    with col1: glycerides = validate_float(st.text_input('Triglycerides'), 'Triglycerides')
    with col2: htn = st.selectbox('History of Hypertension (htn)', ['No', 'Yes'])
    with col3: diabetes = st.selectbox('History of Diabetes', ['No', 'Yes'])
    with col1: fam_htn = st.selectbox('Family History of Hypertension (fam_htn)', ['No', 'Yes'])
    with col2: sp_art = validate_float(st.text_input('Systolic Pulmonary Artery Pressure (sp_art)'), 'Systolic Pulmonary Artery Pressure')

    # Convert categorical features to numerical
    htn = 1 if htn == 'Yes' else 0
    diabetes = 1 if diabetes == 'Yes' else 0
    fam_htn = 1 if fam_htn == 'Yes' else 0

    return [hb, pcv, tsh, platelet, creatinine, plgf_sflt, seng, cysc, pp_13, glycerides, htn, diabetes, fam_htn, sp_art]

# Main application
if user_role == "Patient":
    if patient_login():
        st.title("Preeclampsia Prediction for Patients")
        patient_input = get_patient_input()
        if all(patient_input) and st.button("Preeclampsia Test Result"):
            user_input = patient_input  # + doctor_input (if you have them)
            preeclampsia_prediction = preeclampsia_model.predict([user_input])
            diagnosis = "The person is at risk of preeclampsia" if preeclampsia_prediction[0] == 1 else "The person is not at risk of preeclampsia"
            st.success(diagnosis)

elif user_role == "Doctor":
    if doctor_login():
        st.title("Preeclampsia Prediction for Doctors")
        doctor_input = get_doctor_input()
        if all(doctor_input) and st.button("Preeclampsia Test Result"):
            user_input = doctor_input  # + patient_input (if you have them)
            preeclampsia_prediction = preeclampsia_model.predict([user_input])
            diagnosis = "The person is at risk of preeclampsia" if preeclampsia_prediction[0] == 1 else "The person is not at risk of preeclampsia"
            st.success(diagnosis)
else:
    st.sidebar.info("Please select a role to proceed.")
