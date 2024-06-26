import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
import kagglehub

# IF YOU DO NOT HAVE MODEL ON LOCAL, UNCOMMENT BELOW
# # Download latest version
# path = kagglehub.model_download("tensorflow/ssd-mobilenet-v2/tensorFlow2/fpnlite-320x320")
# # Load the pre-trained SSD MobileNet V2 model from TensorFlow Hub
# model = tf.saved_model.load(path)
# tf.saved_model.save(model, "ssd_mobilenet_v2_fpnlite_320x320")
# Function to preprocess the image

model = tf.saved_model.load("ssd_mobilenet_v2_fpnlite_320x320") # Use this if you already downloaded the model on your local

def preprocess_image(image):
    image = image.resize((320, 320))
    image_array = np.array(image)
    return np.expand_dims(image_array, axis=0).astype(np.uint8)

# Function to detect if the image contains a human
def detect_human(image):
    processed_image = preprocess_image(image)
    input_tensor = tf.convert_to_tensor(processed_image, dtype=tf.uint8)
    detections = model(input_tensor)
    detection_classes = detections['detection_classes'][0].numpy()
    detection_scores = detections['detection_scores'][0].numpy()
    for i, score in enumerate(detection_scores):
        if score > 0.5:  # Confidence threshold
            class_id = int(detection_classes[i])
            if class_id == 1:  # Class ID for person in COCO dataset
                return True
    return False

# Streamlit UI
st.title("Human Detection App")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    # Check if the image contains a human
    if detect_human(image):
        st.success("This image contains a human.")
    else:
        st.error("No human detected in this image.")
