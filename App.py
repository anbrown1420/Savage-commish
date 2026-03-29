import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Page Config
st.set_page_config(page_title="Savage Commish", page_icon="🏈", layout="centered")
st.title("🔥 Savage Commish")
st.markdown("*Where league dreams come to die.*")

# 2. Secret Key Setup
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("Missing API Key! Add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

# --- SECTION 1: MODEL SCOUT (DIAGNOSTIC) ---
with st.expander("🛠️ Tech Support & Model Scout"):
    st.write("If you get a 404 error, check supported models below.")
    if st.button("List My Available Models"):
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.success("Models found!")
            for m_name in models:
                st.code(m_name)
        except Exception as e:
            st.error(f"Could not list models: {e}")

st.divider()

# --- SECTION 2: THE ROAST MACHINE ---
st.subheader("2. The Roast Machine")

# Manual Model Input
model_choice = st.text_input("Model ID:", value="models/gemini-2.5-flash")

# Personality Picker
personality = st.selectbox(
    "Choose Your Executioner:",
    ["Toxic Commish", "Drunk Uncle", "Stat Nerd", "Angry Gambling Addict", "Patronizing Mom"]
)

# Personality Logic - REFINED FOR CREATIVITY
prompts = {
    "Toxic Commish": (
        "Role: A ruthless, power-tripping league commissioner. "
        "Lingo: Use Gen-Z/Alpha slang mixed with corporate hate. Terms: 'fraud watch', 'cooked', 'absolute burger', 'zero aura', 'relegation material'. "
        "Goal: Publicly humiliate the owner. Call them a 'poverty franchise'. Mention how you're considering kicking them out of the league for this performance."
    ),
    "Drunk Uncle": (
        "Role: A bitter 50-year-old with a beer in hand. "
        "Lingo: 'Back in my day', 'soft', 'participation trophy', 'fancy-pants analytics'. "
        "Goal: Compare these modern players to 90s legends who 'played through broken legs.' Insult the user's haircut or life choices based on the team name."
    ),
    "Stat Nerd": (
        "Role: An insufferable MIT dropout who sees the world in spreadsheets. "
        "Lingo: 'Regression to the mean', 'standard deviation of failure', 'statistically insignificant roster'. "
        "Goal: Use pseudo-intellectual math to prove the user's team is a mathematical impossibility. Mention that their 'Expected Wins' is currently 0.0004."
    ),
    "Angry Gambling Addict": (
        "Role: A man who just lost his mortgage on a 12-leg parlay because of one player in this screenshot. "
        "Lingo: ALL CAPS INTERMITTENTLY. 'YOU OWE ME MONEY', 'BUM', 'VANCE JOSEPH RUINED MY LIFE'. "
        "Goal: Be unhinged. Blame the user for 'personally' conspiring with the head coach to ruin your financial future."
    ),
    "Patronizing Mom": (
        "Role: A world-class data scientist talking to her 'sweet, slow' adult son. "
        "Lingo: Diminutives like 'roster-woster', 'pointy-wointies', 'big strong players', 'precious attempt'. "
        "Goal: Use devastating condescension. Tell the user you're going to put their score on the fridge next to their 2nd-grade drawing. "
        "End with: 'Do you want a crustless PB&J while you cry about your little hobby?'"
    )
}

# 3. Intake Multiple Screenshots
uploaded_files = st.file_uploader("Upload Scoreboard Screenshot(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = []
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        images.append(img)
    
    st.image(images, caption=[f"Evidence {i+1}" for i in range(len(images))], width=300)
    
    if st.button(f"EXECUTE ROAST: {personality.upper()}"):
        with st.spinner('Calculating the disrespect...'):
            try:
                # Setup Model with high temperature for more creativity
                generation_config = {
                    "temperature": 1.0, # Increased for more creative/varied responses
                    "top_p": 0.95,
                    "max_output_tokens": 1024,
                }
                
                model = genai.GenerativeModel(
                    model_name=model_choice,
                    generation_config=generation_config
                )
                
                # Construct the prompt
                full_instructions = (
                    f"{prompts[personality]} \n\n"
                    "TASK: Look at the attached screenshot(s). Identify the team names, player names, and scores. "
                    "Write 3 savage, creative, and distinct paragraphs. Do not repeat yourself. "
                    "Be specific about the players/scores you see."
                )
                
                # Pass all images in the list
                content_payload = [full_instructions] + images
                response = model.generate_content(content_payload)
                
                st.subheader("The Verdict:")
                st.write(response.text)
                
                # Copy Box
                st.divider()
                st.subheader("📱 Share to Group Chat")
                st.text_area("Copy/Paste this:", value=response.text, height=250)
                
            except Exception as e:
                st.error(f"Error: {e}")

st.caption("Savage Commish v3.0 | 2026 'Maximum Toxicity' Edition")
