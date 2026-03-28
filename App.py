# Replace the OCR and AI part with this:
if uploaded_file and api_key:
    image = Image.open(uploaded_file)
    st.image(image, caption='The Evidence', use_column_width=True)
    
    if st.button("Generate Savage Roast"):
        with st.spinner('Analyzing the carnage...'):
            try:
                # We send the image DIRECTLY to Gemini
                response = model.generate_content([
                    "You are a toxic Fantasy Football Commissioner. Look at this screenshot and write a 3-paragraph savage roast. Identify the biggest loser and mock their bench/points.", 
                    image
                ])
                st.subheader("The Verdict:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
