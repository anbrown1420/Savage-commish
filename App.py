import streamlit as st
import google.generativeai as genai
from PIL import Image

# THIS MUST BE THE FIRST ST COMMAND
st.set_page_config(page_title="Savage Commish", page_icon="🏈")

st.title("🔥 Savage Commish: AI Vision Roast")

# Logic to check for the API Key
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-flash')
else:
    st.error("Missing API Key! Go to Settings -> Secrets and add GEMINI_API_KEY.")
    st.stop()

st.write("Upload your league screenshot below.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button("Generate Savage Roast"):
        with st.spinner('AI is judging you...'):
            try:
                prompt = "You are a toxic Fantasy Sports Commissioner. Write a 3-paragraph savage roast based on this screenshot. Be mean."
                response = model.generate_content([prompt, image])
                st.subheader("The Verdict:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
