import os
import pickle
import streamlit as st
from streamlit_option_menu import option_menu


# Set page configuration
st.set_page_config(page_title="Preeclampsia Prediction App", layout="wide", page_icon="🧑‍⚕️")

# Load the saved Preeclampsia model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trained_model.sav')
# Load the saved Preeclampsia model
preeclampsia_model = pickle.load(open(f'{working_dir}/saved_models/trained_model.sav', 'rb'))

# Sidebar navigation
st.sidebar.title("Navigation")
user_role = st.sidebar.selectbox("Select your role", ["Select", "Patient", "Doctor"])

# Doctor input form with validation
def get_doctor_input():
    try:
        hb = st.number_input('Hemoglobin (hb)', min_value=0.0, step=0.1)
        pcv = st.number_input('Packed Cell Volume (pcv)', min_value=0.0, step=0.1)
        tsh = st.number_input('Thyroid-Stimulating Hormone (tsh)', min_value=0.0, step=0.1)
        platelet = st.number_input('Platelet count', min_value=0.0, step=1.0)
        creatinine = st.number_input('Creatinine', min_value=0.0, step=0.1)
        plgf_sflt = st.number_input('PLGF/sFlt-1 Ratio', min_value=0.0, step=0.1)
        seng = st.number_input('Soluble Endoglin (sEng)', min_value=0.0, step=0.1)
        cysc = st.number_input('Cystatin C (cysC)', min_value=0.0, step=0.1)
        pp_13 = st.number_input('PAPP-A (pp_13)', min_value=0.0, step=0.1)
        glycerides = st.number_input('Triglycerides', min_value=0.0, step=0.1)
        htn = st.selectbox('History of Hypertension (htn)', ['No', 'Yes'])
        diabetes = st.selectbox('History of Diabetes', ['No', 'Yes'])
        fam_htn = st.selectbox('Family History of Hypertension (fam_htn)', ['No', 'Yes'])
        sp_art = st.number_input('Systolic Pulmonary Artery Pressure (sp_art)', min_value=0.0, step=0.1)

        # Convert categorical features to numerical
        htn = 1 if htn == 'Yes' else 0
        diabetes = 1 if diabetes == 'Yes' else 0
        fam_htn = 1 if fam_htn == 'Yes' else 0

        return [hb, pcv, tsh, platelet, creatinine, plgf_sflt, seng, cysc, pp_13, glycerides, htn, diabetes, fam_htn, sp_art]
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return [None] * 14

# Main application
if user_role == "Doctor":
    if st.sidebar.button("Login"):
        st.title("Preeclampsia Prediction for Doctors")
        doctor_input = get_doctor_input()
        if all(doctor_input) and st.button("Preeclampsia Test Result"):
            user_input = doctor_input
            preeclampsia_prediction = preeclampsia_model.predict([user_input])
            diagnosis = "The person is at risk of preeclampsia" if preeclampsia_prediction[0] == 1 else "The person is not at risk of preeclampsia"
            st.success(diagnosis)
else:
    st.sidebar.info("Please select a role to proceed.")
