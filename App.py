import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Custom Styling (Dark Mode & Professional Polish)
st.set_page_config(page_title="Savage Commish", page_icon="🏈", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ff4b4b; color: white; border: none; font-weight: bold; }
    .stSelectbox label { color: #ff4b4b !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Setup API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Using the stable alias we found works for you
    model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. Sidebar for Settings
with st.sidebar:
    st.title("🛠️ Commish Settings")
    personality = st.selectbox(
        "Choose Your Roast Level:",
        ["Toxic Commish", "Drunk Uncle", "Stat Nerd", "Angry Gambling Addict", "Patronizing Mom"]
    )
    st.info("Upload a screenshot and hit the button to generate the carnage.")

# 4. Main UI
st.title("🔥 Savage Commish")
st.write(f"Current Persona: **{personality}**")

uploaded_file = st.file_uploader("Upload Scoreboard/Roster", type=["jpg", "jpeg", "png"])

# Define Persona Prompts
prompts = {
    "Toxic Commish": "You are a toxic fantasy commissioner. Use heavy slang like 'fraud watch', 'cooked', and 'absolute burger'. Be aggressive and identify the biggest loser.",
    "Drunk Uncle": "You are a drunk uncle who thinks sports were better in the 90s. Complain about modern players being soft while roasting this specific lineup.",
    "Stat Nerd": "You are a condescending math nerd. Use 'advanced metrics' and 'expected points' to mathematically prove why this user is a failure.",
    "Angry Gambling Addict": "You are a high-stakes gambler who just lost your mortgage because of the losing team in this image. You are FURIOUS, loud (caps lock occasionally), and blaming the players personally.",
    "Patronizing Mom": "You are a 'helpful' mom who knows nothing about sports. Be incredibly nice but deeply embarrassing. Talk about how 'proud' you are of them for trying their best even though they lost so badly."
}

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)
    
    if st.button(f"ROAST THEM AS {personality.upper()}"):
        with st.spinner('Calculating the disrespect...'):
            try:
                base_prompt = f"{prompts[personality]} Look at this image, identify the players and scores, and write 3 savage paragraphs."
                response = model.generate_content([base_prompt, image])
                
                st.subheader("📝 The Verdict")
                st.write(response.text)
                
                # Copy/Paste Box for Group Chat
                st.divider()
                st.subheader("📱 Share to Group Chat")
                st.text_area("Copy this:", value=response.text, height=200)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.caption("Powered by Savage AI | v2.0 - 2026 Stable Build")