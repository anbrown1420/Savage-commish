import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import google.generativeai as genai

# 1. Setup & Page Config
st.set_page_config(page_title="Savage Commish", page_icon="🏈")
st.title("🔥 Savage Commish: 100% Free Roast")

# SECRETS: Get a free key at https://aistudio.google.com/
# In Streamlit Cloud, add 'GEMINI_API_KEY' to your Secrets.
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# 2. Main UI
uploaded_file = st.file_uploader("Upload Scoreboard Screenshot", type=["jpg", "png", "jpeg"])

if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button("Generate Savage Roast"):
        with st.spinner('Reading the stats...'):
            img_np = np.array(image)
            results = reader.readtext(img_np)
            raw_text = " ".join([res[1] for res in results])
            
            prompt = f"""
            You are a toxic, hilarious Fantasy Football Commissioner. 
            Based on this messy OCR text from a screenshot, write a 3-paragraph league recap.
            - Identify the biggest loser/clown.
            - Roast someone for leaving points on the bench.
            - Use heavy sports slang (e.g., 'absolute burger', 'fraud watch', 'cooked').
            
            Text: {raw_text}
            """
            
            try:
                response = model.generate_content(prompt)
                st.subheader("The Verdict:")
                st.write(response.text)
                st.text_area("Copy for Group Chat", value=response.text, height=150)
            except Exception as e:
                st.error(f"API Error: {e}")
else:
    st.info("Step 1: Get a free key at Google AI Studio. Step 2: Upload a screenshot.")
