import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
 
# Load the saved model
model = load_model('shelf_life_prediction_model_vgg.keras')
 
# Constants
IMG_SIZE = (224, 224)  # Image size used for training
 
# Function to preprocess the image
def preprocess_image(image):
    image = image.resize(IMG_SIZE)  # Resize image to match model input
    image = img_to_array(image)  # Convert to array
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    image = image / 255.0  # Rescale image
    return image
 
# Streamlit app
st.title('Fruit & Vegetable Shelf Life Predictor')
 
st.write("Upload an image of a fruit or vegetable, and this app will predict its shelf life.")
 
# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
 
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
   
    # Add a button for predicting
    if st.button('Predict Shelf Life'):
        # Preprocess the image
        processed_image = preprocess_image(image)
 
        # Predict the shelf life
        prediction = model.predict(processed_image)
       
        # Assuming you have 14 categories for shelf life
        categories = ['1 day', '2 days', '3 days', '4 days', '5 days', '6 days', '7 days', '8 days', '9 days', '10 days', '11 days', '12 days', '13 days', '14+ days']
        predicted_class = np.argmax(prediction, axis=1)[0]
       
        # Display the prediction result
        st.write(f"Predicted Shelf Life: {categories[predicted_class]}")