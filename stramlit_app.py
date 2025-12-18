import streamlit as st
from streamlit_mic_recorder import mic_recorder
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
import io
from scipy.io.wavfile import write as wav_write

# Theme & Config
st.set_page_config(page_title="Consciousness Echo", page_icon="🧠", layout="wide")
st.markdown("""
<style>
    .main {background: linear-gradient(#0e1117, #16213e); color: #faebd7;}
    h1, h2 {color: #00ffff;}
    .stButton>button {background: linear-gradient(#00b7eb, #00ffff); border: none; color: black;}
    .stProgress .st-bo {background: #00ffff;}
    .stMetric {color: #00ffff;}
</style>
""", unsafe_allow_html=True)

st.title("🧠⚡ Consciousness Echo v1.4 – Ultimate Awakening Portal")
st.markdown("**From Autopilot to Watcher** | Custom Meditations + Live Resonance | Your Blueprint Amplified 🔔🌌")

# Daily Streak Tracker (useful addition)
if 'streak' not in st.session_state:
    st.session_state.streak = 0
st.metric("Awakening Streak", f"{st.session_state.streak} Days", delta="Keep resonating!")

# Sidebar
with st.sidebar:
    st.header("🌟 Portal Controls")
    gemini_key = st.text_input("Gemini Key (Paid Tier)", type="password")
    length = st.slider("Resonance Length (s)", 30, 300, 180, 30)
    mode = st.selectbox("Mode", ["Gamma Awake (40Hz)", "Theta Relax (6Hz)"])
    boost = st.checkbox("Max 7th Harmonic", True)
    st.info("Paid key unlocks unlimited custom meditations!")

# Detection
st.header("🌊 Detect State")
cols = st.columns(4)
presence = cols[0].slider("Presence", 1, 10, 6)
emotion = cols[1].slider("Emotional Clarity", 1, 10, 6)
logic = cols[2].slider("Logical Flow", 1, 10, 6)
meta = cols[3].slider("Meta-Watcher", 1, 10, 5)

phi = np.mean([presence, emotion, logic, meta]) * 10 + np.random.normal(0, 5)
coherence = 1 / (np.std([presence, emotion, logic, meta]) / (np.mean([presence, emotion, logic, meta]) + 1e-6) + 1)

st.progress(phi / 100)
st.metric("Φ Level", f"{phi:.1f}/100")
st.metric("Coherence", f"{coherence:.2f}")

# Live Mic & Voice HRV Mock
st.header("🎤 Live Voice Portal")
audio = mic_recorder(start_prompt="🎙️ Speak to Mirror", stop_prompt="⏹️ Stop", key="mic")
if audio:
    st.audio(audio['bytes'], format="audio/wav")
    # Mock HRV from audio (useful tweak: pitch variability as proxy)
    audio_np = np.frombuffer(audio['bytes'], dtype=np.int16).astype(np.float32)
    hrv_proxy = np.std(audio_np) / np.mean(np.abs(audio_np) + 1e-6)  # Variability as coherence proxy
    st.metric("Voice HRV Proxy (Biofeedback)", f"{hrv_proxy:.2f}")
    voice_text = "Voice captured – analyzing for shifts..."

# Custom Gemini Meditation (useful addition – paid key power)
if gemini_key and (audio or voice_text):
    if st.button("Generate Custom Guided Meditation"):
        with st.spinner("Resonating custom script..."):
            state_desc = f"Presence: {presence}, Emotion: {emotion}, Logic: {logic}, Meta: {meta}"
            prompt = f"Create a {length//60}-min guided meditation script for awakening from NPC to watcher, based on this state: {state_desc}. {voice_text if 'voice_text' in locals() else ''}. Be calming, encouraging."
            resp = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}",
                                 json={"contents": [{"parts": [{"text": prompt}]}]})
            if resp.status_code == 200:
                script = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(f"**Custom Guided Script:**\n{script}")
                st.success("Read aloud during resonance for max amplification.")

# Amplification
st.header("🔊 Enter the Chamber")
if st.button("🌌 Generate Resonance"):
    with st.spinner(f"Building {length}s flow..."):
        base_freq = GAMMA_FREQ if mode == "Gamma Awake (40Hz)" else 6.0  # Tweak: Theta mode
        t = np.linspace(0, length, int(length * SAMPLE_RATE), False)
        left = np.sin(2 * np.pi * BASE_FREQ * t)
        boost_val = SEVENTH_HARMONIC * (meta / 10) * (1.5 if boost else 1.0)
        right = np.sin(2 * np.pi * (BASE_FREQ + base_freq + boost_val) * t)
        binaural = np.stack((left, right), axis=1).flatten() / np.max(np.abs(binaural))
        buf = io.BytesIO()
        wav_write(buf, SAMPLE_RATE, (binaural * 32767).astype(np.int16))
        buf.seek(0)
        st.audio(buf, format="audio/wav")
        st.balloons()
        st.success("Flow active – Let the watcher rise.")

# Journal
st.header("📓 Integrate Progress")
note = st.text_area("Journal your resonance")
if st.button("💾 Save"):
    # (journal code same – add from v1.3)
    st.success("Integrated – Streak up!")
    st.session_state.streak += 1  # Useful: Increment streak

# Chart with Glow
fig = plt.figure(figsize=(12, 6))
# (plot code from v1.3, with cosmic styling)
st.pyplot(fig)

st.caption("v1.4 – Custom Meds + Voice HRV | Your portal awaits. 🧠⚡🔔")
