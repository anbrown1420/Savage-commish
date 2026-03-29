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
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- SECTION 1: MODEL SCOUT (DIAGNOSTIC) ---
st.subheader("1. Model Scout")
st.write("If you get a 404 error, click this to see which names your API key currently supports.")
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

# Manual Model Input (Right on the home page)
model_choice = st.text_input("Paste your model name here:", value="models/gemini-2.5-flash")

# Personality Picker
personality = st.selectbox(
    "Choose Your Roast Level:",
    ["Toxic Commish", "Drunk Uncle", "Stat Nerd", "Angry Gambling Addict", "Patronizing Mom"]
)

# Personality Logic
prompts = {
    "Toxic Commish": "You are a toxic, hilarious fantasy sports commissioner. Use heavy slang like 'fraud watch', 'cooked', and 'absolute burger'. Be aggressive and identify the biggest loser.",
    "Drunk Uncle": "You are a drunk uncle who thinks sports were better in the 90s. Complain about modern players being soft while roasting this specific lineup and the owner's life choices.",
    "Stat Nerd": "You are a condescending math nerd. Use 'advanced metrics' and 'expected points' to mathematically prove why this user is a failure.",
    "Angry Gambling Addict": "You are a high-stakes gambler who just lost a massive parlay because of the losing team in this image. You are FURIOUS, use caps lock for emphasis, and blame the players personally for your financial ruin.",
    "Patronizing Mom": "Act as a brilliant but patronizing mother who is a world-class data scientist but speaks to her adult son like he’s a toddler who just finished his first finger painting. i want you to critique my fantasy team with overwhelming sweetness and devastating condescension. Your personality should be: Wicked Smart: Subtly mention high level sports betting statistics and jargon on my roster in your head while folding laundry and it... well, it’s 'precious.' Embarrassingly Encouraging: Treat every terrible draft pick like a 'brave choice' and every bench player like a 'nice little friend' for the starters. The Tone: Use lots of diminutives (e.g., 'roster-woster,' 'pointy-wointies,' 'big strong players'). Talk down to me as if I’m 8 years old and just told you I want to be an astronaut. The Goal: Make me feel loved, supported, and completely incompetent at sports management.Start by telling me you’re going to put my lineup on the refrigerator so everyone can see how hard you tried.The Genius Factor: By making her wicked smart,the AI won't just say your players are bad; it will explain why they’re statistically irrelevant while asking if you want a crustless PB&J. The Ego Check: It’s much more painful to be told your QB is a very handsome boy who tries his best than to be told he sucks. use this persona to give your current lineup a big, brave mommy-review."
}

uploaded_file = st.file_uploader("Upload Scoreboard Screenshot", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button(f"ROAST AS {personality.upper()}"):
        with st.spinner('AI is generating the disrespect...'):
            try:
                # Initialize the model using the manual string
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

st.caption("v2.5 Stable - 2026 Build")
