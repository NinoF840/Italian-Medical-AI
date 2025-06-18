import streamlit as st

# Minimal app for deployment testing
st.set_page_config(page_title="Medico-Italiano-IA", page_icon="🏥")

st.title("🏥 Medico-Italiano-IA")
st.success("✅ Deployment successful!")
st.write("This is a minimal version to test cloud deployment.")

# Basic demo functionality
text = st.text_area("Enter Italian medical text:", "Il paziente presenta febbre alta.")
if st.button("Analyze"):
    st.success(f"✅ Analyzed {len(text)} characters")
    st.write("**Demo entities found:** febbre (SYMPTOM), paziente (PERSON)")

st.sidebar.success("App is online!")
st.sidebar.write("Full version coming soon...")

