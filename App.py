import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Savage Commish Diagnostic", page_icon="🕵️")
st.title("🕵️ Savage Commish: Model Scout")

# 2. Secret Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- DIAGNOSTIC SECTION ---
st.subheader("1. Run Diagnostic")
if st.button("List My Available Models"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.success("Models found! Copy one of these exactly:")
        for m_name in models:
            st.code(m_name)
    except Exception as e:
        st.error(f"Could not list models: {e}")

st.divider()

# --- MAIN APP SECTION ---
st.subheader("2. Test a Model Name")
model_name = st.text_input("Paste the model name from above here:", value="models/gemini-1.5-flash")

uploaded_file = st.file_uploader("Upload screenshot", type=["jpg", "jpeg", "png"])

if uploaded_file and st.button("Generate Roast"):
    image = Image.open(uploaded_file)
    try:
        # Use the name typed in the box
        test_model = genai.GenerativeModel(model_name)
        response = test_model.generate_content(["Roast this fantasy sports screenshot.", image])
        st.write(response.text)
    except Exception as e:
        st.error(f"Failed with {model_name}: {e}")
