
import os
import streamlit as st

# Groq API Key
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Hugging Face API Key
try:
    HF_API_KEY = st.secrets["HF_API_KEY"]
except (KeyError, FileNotFoundError):
    HF_API_KEY = os.getenv("HF_API_KEY", "")

# Check API keys
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing in config.py")

if not HF_API_KEY:
    raise ValueError("HF_API_KEY missing in config.py")

