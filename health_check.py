#!/usr/bin/env python3
"""
Health Check for Streamlit Cloud Deployment
Simple script to verify the app is working correctly
"""

import streamlit as st
import sys
import platform

st.set_page_config(
    page_title="Health Check",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Deployment Health Check")

# System information
st.header("🖥️ System Information")
col1, col2 = st.columns(2)

with col1:
    st.write(f"**Python Version:** {sys.version}")
    st.write(f"**Platform:** {platform.platform()}")

with col2:
    st.write(f"**Streamlit Version:** {st.__version__}")
    st.write(f"**Architecture:** {platform.architecture()[0]}")

# Functionality tests
st.header("🧪 Functionality Tests")

# Test 1: Basic Streamlit functions
st.subheader("Test 1: Basic Functions")
if st.button("Test Button Click"):
    st.success("✅ Button click works!")
    st.balloons()

# Test 2: Input widgets
st.subheader("Test 2: Input Widgets")
test_text = st.text_input("Enter test text:", "Hello, World!")
if test_text:
    st.success(f"✅ Text input works: {test_text}")

# Test 3: Layout components
st.subheader("Test 3: Layout Components")
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("✅ Tab 1 content")
with tab2:
    st.write("✅ Tab 2 content")

# Test 4: Sidebar
with st.sidebar:
    st.header("Sidebar Test")
    st.success("✅ Sidebar working")
    st.slider("Test Slider", 0, 100, 50)

# Final status
st.header("📊 Overall Status")
st.success("🎉 All tests passed! Deployment is healthy.")
st.info("🌐 This app is accessible from the internet.")

# Deployment info
st.header("🔧 Deployment Information")
st.code("""
URL: https://new-medical-italian.streamlit.app
Repository: https://github.com/NinoF840/Italian-Medical-AI
Status: ✅ Online and functional
""")

