import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import pandas as pd
import plotly.express as px
from tensorflow.keras.preprocessing import image
from io import BytesIO
from datetime import datetime

# For MongoDB and GridFS
from pymongo import MongoClient
import gridfs  # Add this line

# For PDF generation
from fpdf import FPDF

# ---------------------------
# MongoDB Connection Setup
def check_mongodb_connection():
    try:
        client.admin.command('ping')  # Simple command to check connection
        return True
    except Exception as e:
        return False

mongo_uri = "mongodb+srv://joshuailangovansamuel:HHXm1xKAsKxZtQ6I@cluster0.pbvcd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client['pneumonia']
fs = gridfs.GridFS(db)
patients_collection = db['patients']
classifications_collection = db['classifications']

if check_mongodb_connection():
    st.success("Connected to MongoDB successfully!")
else:
    st.error("Failed to connect to MongoDB. Please check your connection.")
    st.stop()

# ---------------------------
# Load the pre-trained model
@st.cache_resource
def load_model():
    model = tf.keras.models.load_model("model.keras")  # Ensure the model file is in the project folder
    return model

model = load_model()

# ---------------------------
# Integrated Gradients Function
def integrated_gradients(model, x, target_class_idx=0, baseline=None, steps=50):
    if baseline is None:
        baseline = tf.zeros(shape=x.shape, dtype=x.dtype)
    interpolated_x = [baseline + (float(i)/steps) * (x - baseline) for i in range(steps + 1)]
    interpolated_x = tf.concat(interpolated_x, axis=0)
    with tf.GradientTape() as tape:
        tape.watch(interpolated_x)
        preds = model(interpolated_x)
        outputs = preds[:, 0] if preds.shape[1] == 1 else preds[:, target_class_idx]
    grads = tape.gradient(outputs, interpolated_x)
    grads = tf.reshape(grads, (steps + 1, ) + x.shape[1:])
    avg_grads = (grads[1:] + grads[:-1]) / 2.0
    integrated_grad = tf.reduce_mean(avg_grads, axis=0)
    integrated_grad = (x - baseline) * integrated_grad
    integrated_grad = tf.reduce_sum(integrated_grad, axis=-1)
    return integrated_grad.numpy().squeeze()

# ---------------------------
# Image Processing Function
def process_image_file(file_bytes):
    file_arr = np.asarray(bytearray(file_bytes), dtype=np.uint8)
    cv2_img = cv2.imdecode(file_arr, cv2.IMREAD_COLOR)
    cv2_img = cv2.resize(cv2_img, (150, 150))
    rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    x = image.img_to_array(rgb_img) / 255.0
    x = np.expand_dims(x, axis=0)
    return x, rgb_img

# ---------------------------
# PDF Report Generator
def generate_pdf_report(patient, classification_result, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Patient Report: {patient['name']}", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Age: {patient.get('age', 'N/A')}", ln=2, align='C')
    pdf.cell(200, 10, txt=f"Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}", ln=3, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Classification: {classification_result}", ln=4, align='L')
    pdf.cell(200, 10, txt=f"Confidence: {confidence:.2f}", ln=5, align='L')
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer, dest='S')  # Corrected PDF output
    return pdf_buffer.getvalue()

# ---------------------------
# Streamlit UI
tab1, tab2 = st.tabs(["Upload Patient Data", "Process Patients & Generate Reports"])

with tab1:
    st.header("Upload Patient X-ray and Details")
    with st.form("upload_form"):
        patient_name = st.text_input("Patient Name")
        patient_age = st.text_input("Patient Age")
        uploaded_file = st.file_uploader("Upload X-ray image", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Upload")
    
    if submitted:
        if patient_name and uploaded_file is not None:
            try:
                file_bytes = uploaded_file.read()
                image_id = fs.put(file_bytes, filename=uploaded_file.name, content_type=uploaded_file.type)
                patient_doc = {"name": patient_name, "age": patient_age, "upload_time": datetime.utcnow(), "image_id": image_id}
                patients_collection.insert_one(patient_doc)
                st.success(f"Patient {patient_name} and image uploaded successfully!")
            except Exception as e:
                st.error(f"Error saving data: {e}")
        else:
            st.error("Please provide all required fields.")

with tab2:
    st.header("Process Patients and Generate Reports")
    patients = list(patients_collection.find())
    if patients:
        for patient in patients:
            st.subheader(f"Patient: {patient['name']}")
            try:
                file_data = fs.get(patient['image_id']).read()
            except Exception as e:
                st.error(f"Error retrieving image for {patient['name']}: {e}")
                continue
            x, rgb_img = process_image_file(file_data)
            prediction = model.predict(x)
            result = "Positive" if prediction[0][0] > 0.5 else "Negative"
            confidence = float(prediction[0][0])
            st.image(rgb_img, caption="X-ray Image", use_column_width=True)
            st.write(f"Classification: **{result}** with confidence **{confidence:.2f}**")
            pdf_data = generate_pdf_report(patient, result, confidence)
            st.download_button("Download Report PDF", data=pdf_data, file_name=f"{patient['name']}_report.pdf", mime="application/pdf")
            st.markdown("---")
    else:
        st.write("No patient records found.")
