import streamlit as st
from PIL import Image
import requests

# Define the endpoint for breed recognition
RECOGNITION_URL = "http://server:8000/recognize_dog_breed"

st.title('Dog Breed Recognition')

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("Classifying...")

    # Convert the file to an image that can be sent via HTTP
    files = {"file": uploaded_file.getvalue()}

    # Post the image to the endpoint
    response = requests.post(RECOGNITION_URL, files=files)

    if response.status_code == 200:
        # On a successful response, display the predicted breed
        prediction = response.json()
        highest_matching_breed = prediction[0]['label']
        st.write(f"Predicted breed: {highest_matching_breed}")
    else:
        # If the response wasn't successful, display an error message
        st.write(f"Failed to classify image. Status code: {response.status_code}")
