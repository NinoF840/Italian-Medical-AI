import streamlit as st
import datetime

# Simple test version for deployment verification
st.set_page_config(
    page_title="Medico-Italiano-IA - Test",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Medico-Italiano-IA - Deployment Test")
st.success("✅ App is running successfully!")

st.write("If you can see this message, the deployment is working.")
st.write(f"**Last updated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Basic functionality test
if st.button("Test Button"):
    st.balloons()
    st.write("✅ Interactive elements working!")
    st.write("🌐 Internet deployment successful!")

st.sidebar.success("✅ Sidebar working!")
st.sidebar.write("Demo is online and functional.")
st.sidebar.write(f"Streamlit version: {st.__version__}")

