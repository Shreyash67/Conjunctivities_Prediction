import streamlit as st
import cv2
import numpy as np
import subprocess
from tensorflow import keras
import matplotlib.pyplot as plt
import base64
import os

# Load the models
model_path = r'iphone/con_i.h5'  # Conjunctivitis detection model
model = keras.models.load_model(model_path, compile=False)

i_model_path = r'iphone/m_model_7.h5'  # Human eye detection model
i_model = keras.models.load_model(i_model_path, compile=False)

# Function to resize the image
def resize_image(image, size=(150, 150)):
    return cv2.resize(image, size)

# Function to load and preprocess image from file uploader
def load_image_from_file_uploader(file_uploader):
    try:
        image_bytes = file_uploader.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        return image
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

# Function to run live capture and return image
def run_live_capture():
    result = subprocess.run(['python', 'iphone\iphone_live.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        st.error(f"Error running live.py: {result.stderr.decode()}")
        return None
    if os.path.exists('cropped_image.jpg'):
        image = cv2.imread('cropped_image.jpg')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        return image
    else:
        st.error("Image not captured!")
        return None

# Function to set local background image
def set_bg_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image
set_bg_image('samsung/b2.png')

# Styled title
st.markdown(
    """
    <style>
    .title {
        font-size: 60px;
        text-align: center;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="title">Conjunctivitis Prediction</h1>', unsafe_allow_html=True)

# Select input method
input_method = st.radio("Choose Input Method:", ["Upload Image", "Live Camera Capture"])

if input_method == "Upload Image":
    selected_image_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    if selected_image_file is not None:
        image = load_image_from_file_uploader(selected_image_file)

elif input_method == "Live Camera Capture":
    if st.button("Start Live Camera"):
        st.write("Capturing Image...")
        image = run_live_capture()

# Process image if available
if 'image' in locals() and image is not None:
    st.image(image, caption='Processed Image', use_column_width=True)
    resized_image = resize_image(image)
    img_array = np.expand_dims(resized_image, axis=0) / 255.0

    # Human eye detection
    eye_prediction = i_model.predict(img_array)
    is_human_eye = eye_prediction[0][0] <= 0.5

    if is_human_eye:
        st.success(" The image is identified as a human eye.")
        conjunctivitis_prediction = model.predict(img_array)
        label = "Healthy Eye" if conjunctivitis_prediction[0][0] > 0.5 else "Infected Eye"
        st.markdown(f"<h2 style='text-align: center;'>Prediction: <span style='font-size: 36px;'>{label}</span></h2>", unsafe_allow_html=True)
    else:
        st.warning("L The image is not identified as a human eye. Try again with a clearer image.")
