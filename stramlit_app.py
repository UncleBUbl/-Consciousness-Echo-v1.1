import streamlit as st
from streamlit_mic_recorder import mic_recorder
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
import io
from scipy.io.wavfile import write as wav_write

# Theme
st.set_page_config(page_title="Consciousness Echo", page_icon="🧠", layout="wide")
st.markdown("""
<style>
    .main {background: linear-gradient(#0e1117, #16213e); color: #faebd7;}
    h1, h2 {color: #00ffff;}
    .stButton>button {background: linear-gradient(#00b7eb, #00ffff); border: none; color: black;}
    .stSelectbox, .stSlider {color: #00ffff;}
</style>
""", unsafe_allow_html=True)

st.title("🧠⚡ Consciousness Echo v1.5 – Multi-Mode Portal")
st.markdown("**Choose Your Wave** | Full Brainwave Entrainment | Awakening Amplified 🔔🌌")

# Brainwave Charts Inspo
st.image("https://www.diygenius.com/wp-content/uploads/2022/12/brainwave-frequencies-chart.jpg", caption="Brainwave Frequencies Overview")
st.image("https://images.squarespace-cdn.com/content/v1/5bee2e5d2714e52916f4d54c/1620812751228-38Z8PRVAH17ZE48SMLNW/brainwaves+what+are+types+of+brain+wave+chart.png", caption="States & Effects")
st.image("https://storage.googleapis.com/mv-prod-blog-en-assets/2019/01/52d9017f-brainwaves_bloggraphic_1200x800.webp", caption="Entrainment Guide")

# Sidebar Modes
with st.sidebar:
    st.header("🌟 Wave Modes")
    modes = {
        "Gamma Peak (40 Hz)": {"freq": 40.0, "desc": "Heightened insight, watcher mode, cognitive flow – Orch-OR activation"},
        "Beta Focus (20 Hz)": {"freq": 20.0, "desc": "Alert thinking, productivity, problem-solving"},
        "Alpha Relax (10 Hz)": {"freq": 10.0, "desc": "Calm alertness, stress reduction, creativity bridge"},
        "Theta Dream (6 Hz)": {"freq": 6.0, "desc": "Deep meditation, intuition, subconscious access"},
        "Delta Heal (2 Hz)": {"freq": 2.0, "desc": "Deep sleep, healing, restorative detachment"}
    }
    mode_choice = st.selectbox("Select Entrainment Mode", list(modes.keys()))
    selected = modes[mode_choice]
    st.info(selected["desc"])

    length = st.slider("Session Length (s)", 30, 300, 180, 30)
    custom_hz = st.checkbox("Custom Hz Fine-Tune")
    if custom_hz:
        custom_freq = st.slider("Custom Beat Freq", 0.5, 50.0, selected["freq"], 0.5)
    else:
        custom_freq = selected["freq"]

    boost = st.checkbox("7th Harmonic Boost", True)

# Detection (same as before)
# ... (keep sliders, phi calc)

# Amplification with Selected Mode
if st.button("🌌 Activate Wave"):
    freq = custom_freq
    # Generate with selected freq
    # ... (same gen code, use freq instead of GAMMA_FREQ)

# Rest same – mic, journal, Gemini, etc.

st.caption("v1.5 – Full Modes | Choose your wave, awaken your state. 🧠⚡🔔")
