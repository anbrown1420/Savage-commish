import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config (Standard Look)
st.set_page_config(page_title="Savage Commish", page_icon="🏈")
st.title("🔥 Savage Commish")

# 2. Secret Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# 3. Sidebar Configuration
with st.sidebar:
    st.title("⚙️ App Settings")
    
    # Re-adding the manual model selection box
    model_choice = st.text_input(
        "AI Model Name:", 
        value="models/gemini-1.5-flash",
        help="Use 'models/gemini-1.5-flash' or 'models/gemini-3-flash' based on what worked in your diagnostic."
    )
    
    personality = st.selectbox(
        "Choose Your Roast Level:",
        ["Toxic Commish", "Drunk Uncle", "Stat Nerd", "Angry Gambling Addict", "Patronizing Mom"]
    )
    
    st.divider()
    st.info("Upload a screenshot and let the AI do the rest.")

# 4. Personality Logic
prompts = {
    "Toxic Commish": "You are a toxic, hilarious fantasy sports commissioner. Use heavy slang like 'fraud watch', 'cooked', and 'absolute burger'. Be aggressive and identify the biggest loser.",
    "Drunk Uncle": "You are a drunk uncle who thinks sports were better in the 90s. Complain about modern players being soft while roasting this specific lineup/score.",
    "Stat Nerd": "You are a condescending math nerd. Use 'advanced metrics' and 'expected points' to mathematically prove why this user is a failure.",
    "Angry Gambling Addict": "You are a high-stakes gambler who just lost a massive parlay because of the losing team in this image. You are FURIOUS, use caps lock for emphasis, and blame the players personally.",
    "Patronizing Mom": "You are a 'helpful' mom who knows nothing about sports. Be incredibly nice but deeply embarrassing. Talk about how 'proud' you are of them for trying their best even though they lost so badly."
}

# 5. Main UI
st.write(f"Current Persona: **{personality}**")

uploaded_file = st.file_uploader("Upload Scoreboard Screenshot", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button(f"ROAST AS {personality.upper()}"):
        with st.spinner('AI is generating the disrespect...'):
            try:
                # Initialize the model using the manual string from the sidebar
                model = genai.GenerativeModel(model_choice)
                
                base_prompt = f"{prompts[personality]} Look at this screenshot, identify the teams/players and scores, and write 3 savage paragraphs."
                
                response = model.generate_content([base_prompt, image])
                
                st.subheader("The Verdict:")
                st.write(response.text)
                
                # Copy Box
                st.divider()
                st.subheader("📱 Share to Group Chat")
                st.text_area("Copy/Paste this:", value=response.text, height=200)
                
            except Exception as e:
                st.error(f"Error with model '{model_choice}': {e}")