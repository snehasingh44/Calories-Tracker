from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the Gemini API
def get_gemini_response(image, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to process image and prepare for the API
def input_image_setup(uploaded_file):
    try:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": "image/jpeg", "data": bytes_data}]
        return image_parts
    except Exception as e:
        raise ValueError(f"Error processing image: {str(e)}")

# Initialize Streamlit app configuration
st.set_page_config(page_title="Calorie Tracker", page_icon="🍎", layout="centered")

# Apply custom styling for minimalistic design
st.markdown("""
    <style>
        .stApp { background-color: black; font-family: 'Arial', sans-serif; }
        .main-header { font-size: 2.5em; font-weight: bold; text-align: center; color: #333; margin-bottom: 20px; }
        .response-text { font-size: 1.1em; line-height: 1.5; color: #444; text-align: justify; }
        img { border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# Display the app's header
st.markdown('<div class="main-header">Calorie Tracker: AI-Powered Food Insights</div>', unsafe_allow_html=True)

# Persistent state to manage image source
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# Tabs for selecting input method
tab1, tab2 = st.tabs(["📷 Capture Image", "📁 Upload Image"])

# Camera input (real-time capture)
with tab1:
    st.markdown("#### Use your camera to take a picture")
    camera_image = st.camera_input("Take a picture of your food")
    if camera_image:
        st.session_state.selected_image = camera_image  # Store the captured image

# File uploader (browse and upload)
with tab2:
    st.markdown("#### Browse and upload an image from your device")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.session_state.selected_image = uploaded_file  # Store the uploaded file

# Display and process the selected image
if st.session_state.selected_image:
    try:
        # Display the selected image
        image = Image.open(st.session_state.selected_image)
        st.image(image, caption="Selected Image", use_column_width=True)

        # Prepare the image data for API request
        image_data = input_image_setup(st.session_state.selected_image)

        # Input prompt for the API
        input_prompt = """
        You are an expert nutritionist. Please analyze the food items in the image
        and calculate the total calories, also provide the details of each food item with calorie intake
        in the following format:

        1. Item 1 - number of calories
        2. Item 2 - number of calories
        ----
        ----
        Finally, mention whether the food is healthy or not.
        If the food is unhealthy, give suggestions to add or remove food items to make it an overall healthy meal.
        """

        # Get the response from the Gemini API
        response = get_gemini_response(image_data, input_prompt)

        # Display the response text
        st.markdown("### Nutritional Analysis", unsafe_allow_html=True)
        st.markdown(f'<div class="response-text">{response}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.info("Please select an image by either capturing one or uploading it.")