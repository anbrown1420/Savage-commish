import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. Page Config
st.set_page_config(page_title="Savage Commish", page_icon="🏈")
st.title("🔥 Savage Commish")

# 2. Secret Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- SECTION 1: MODEL SCOUT ---
st.subheader("1. Model Scout")
if st.button("List My Available Models"):
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.success("Models found! Copy one of these exactly:")
        for m_name in models:
            st.code(m_name)
    except Exception as e:
        st.error(f"Could not list models: {e}")

st.divider()

# --- SECTION 2: THE ROAST MACHINE ---
st.subheader("2. The Roast Machine")

model_choice = st.text_input("Paste your model name here:", value="models/gemini-2.5-flash-lite")
personality = st.selectbox(
    "Choose Your Roast Level:",
    ["Toxic Commish", "Drunk Uncle", "Stat Nerd", "Angry Gambling Addict", "Patronizing Mom"]
)

prompts = {
    "Toxic Commish": "You are a toxic fantasy commissioner. Use slang like 'fraud watch' and 'cooked'.",
    "Drunk Uncle": "You are a drunk uncle who thinks modern sports are soft. Roast this lineup.",
    "Stat Nerd": "You are a condescending math nerd. Prove they are a failure with fake math.",
    "Angry Gambling Addict": "You are FURIOUS. You lost your parlay and your mortgage. Use CAPS LOCK.",
    "Patronizing Mom": "Be incredibly nice but deeply embarrassing. Bring up orange slices."
}

uploaded_file = st.file_uploader("Upload Scoreboard Screenshot", type=["jpg", "jpeg", "png"])

# Use Session State to "remember" the roast so we can make a meme from it
if 'current_roast' not in st.session_state:
    st.session_state.current_roast = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button(f"ROAST AS {personality.upper()}"):
        with st.spinner('Generating disrespect...'):
            try:
                model = genai.GenerativeModel(model_choice)
                base_prompt = f"{prompts[personality]} Look at this screenshot and write 3 savage paragraphs."
                response = model.generate_content([base_prompt, image])
                st.session_state.current_roast = response.text
            except Exception as e:
                st.error(f"Error: {e}")