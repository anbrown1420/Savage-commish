# import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup
st.set_page_config(page_title="Savage Commish", page_icon="🏈")
st.title("🔥 Savage Commish: AI Vision Roast")

# Get API Key from Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Using the 'flash' model which supports image input
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Please add GEMINI_API_KEY to your Streamlit Secrets!")
    st.stop()

# 2. UI
st.write("Upload a screenshot of your league scoreboard or roster.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button("Generate Savage Roast"):
        with st.spinner('AI is judging your life choices...'):
            try:
                # The prompt is combined with the image directly
                prompt = """
                You are a toxic, hilarious Fantasy Sports Commissioner. 
                Look at this screenshot and write a 3-paragraph savage roast. 
                - Identify the 'Clown of the Week' (the biggest loser).
                - Mock specific players who failed or points left on the bench.
                - Use aggressive sports slang like 'fraud watch', 'cooked', and 'absolute burger'.
                - Be specific to the numbers you see in the image.
                """
                
                response = model.generate_content([prompt, image])
                
                st.subheader("The Verdict:")
                st.write(response.text)
                
                # Copy-paste helper
                st.text_area("Copy for Group Chat", value=response.text, height=150)
                
            except Exception as e:
                st.error(f"Something went wrong: {e}")
