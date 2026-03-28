import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Savage Commish", page_icon="🏈")
st.title("🔥 Savage Commish")

# 2. Secret Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Using the universal stable alias with the 'models/' prefix
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# 3. UI logic
st.write("Upload a screenshot of your league scoreboard.")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button("Generate Savage Roast"):
        with st.spinner('AI is analyzing your failure...'):
            try:
                prompt = """
                You are a toxic, hilarious Fantasy Sports Commissioner. 
                Look at this screenshot and write a 3-paragraph savage roast. 
                Identify the biggest loser, mock specific players/points, 
                and use aggressive sports slang. Check the benched players and missed points. Be mean.
                """
                # Send image and prompt to Gemini
                response = model.generate_content([prompt, image])
                
                st.subheader("The Verdict:")
                st.write(response.text)
                st.text_area("Copy for Group Chat", value=response.text, height=150)
                
            except Exception as e:
                st.error(f"Error: {e}")
