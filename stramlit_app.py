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

# Streak Tracker
if 'streak' not in st.session_state:
    st.session_state.streak = 0
st.metric("Awakening Streak", f"{st.session_state.streak} Days", delta="Keep resonating!")

# Sidebar
with st.sidebar:
    st.header("🌟 Wave Modes")
    modes = {
        "Gamma Peak (40 Hz)": {"freq": 40.0, "desc": "Heightened insight, watcher mode, cognitive flow – Orch-OR activation"},
        "Beta Focus (20 Hz)": {"freq": 20.0, "desc": "Alert thinking, productivity, problem-solving"},
        "Alpha Relax (10 Hz)": {"freq": 10.0, "desc": "Calm alertness, stress reduction, creativity bridge"},
        "Theta Dream (6 Hz)": {"freq": 6.0, "desc": "Deep meditation, intuition, subconscious access"},
        "Delta Heal (2 Hz)": {"freq": 2.0, "desc": "Deep sleep, healing, restorative detachment"}
    }
    mode_choice = st.selectbox("Select Mode", list(modes.keys()))
    selected = modes[mode_choice]
    st.info(selected["desc"])

    length = st.slider("Session Length (s)", 30, 300, 180, 30)
    custom_hz = st.checkbox("Custom Hz")
    if custom_hz:
        custom_freq = st.slider("Custom Freq", 0.5, 50.0, selected["freq"], 0.5)
    else:
        custom_freq = selected["freq"]
    gemini_key = st.text_input("Gemini Key", type="password")
    boost = st.checkbox("7th Harmonic Boost", True)

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

# Voice
st.header("🎤 Live Voice Portal")
audio = mic_recorder(start_prompt="🎙️ Speak", stop_prompt="⏹️ Stop", key="mic")
if audio:
    st.audio(audio['bytes'], format="audio/wav")
    voice_np = np.frombuffer(audio['bytes'], dtype=np.int16).astype(np.float32)
    hrv_proxy = np.std(voice_np) / np.mean(np.abs(voice_np) + 1e-6)
    st.metric("Voice HRV Proxy", f"{hrv_proxy:.2f}")
    voice_text = "Voice captured – analyzing..."

# Custom Meditation
if gemini_key and (audio or voice_text):
    if st.button("Generate Custom Meditation"):
        state_desc = f"Presence: {presence}, Emotion: {emotion}, Logic: {logic}, Meta: {meta}"
        prompt = f"Create a {length//60}-min guided script for awakening from NPC to watcher, mode: {mode_choice}, state: {state_desc}. {voice_text if 'voice_text' in locals() else ''}."
        resp = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}",
                             json={"contents": [{"parts": [{"text": prompt}]}]})
        if resp.status_code == 200:
            script = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(f"**Custom Script:**\n{script}")
            st.success("Use during session for deep resonance.")

# Amplification
st.header("🔊 Enter Chamber")
if st.button("🌌 Generate Resonance"):
    freq = custom_freq
    t = np.linspace(0, length, int(length * SAMPLE_RATE), False)
    left = np.sin(2 * np.pi * BASE_FREQ * t)
    boost_val = 54.81 * (meta / 10) * (1.5 if boost else 1.0)
    right = np.sin(2 * np.pi * (BASE_FREQ + freq + boost_val) * t)
    binaural = np.stack((left, right), axis=1).flatten() / np.max(np.abs(binaural))
    buf = io.BytesIO()
    wav_write(buf, SAMPLE_RATE, (binaural * 32767).astype(np.int16))
    buf.seek(0)
    st.audio(buf, format="audio/wav")
    st.success(f"{length}s {mode_choice} flow – Let the watcher rise.")

# Journal
st.header("📓 Integrate Progress")
note = st.text_area("Journal shift")
if st.button("💾 Save"):
    try:
        df = pd.read_csv("awakening_journal.csv")
    except:
        df = pd.DataFrame(columns=["Date", "Pre_Φ", "Post_Φ", "Note"])

    new_row = {"Date": datetime.datetime.now(), "Pre_Φ": phi, "Post_Φ": phi * 1.5, "Note": note or voice_text}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("awakening_journal.csv", index=False)
    st.success("Integrated – Streak up!")
    st.session_state.streak += 1

    fig = plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Post_Φ"], marker="o", color="#00ffff", linewidth=3)
    plt.title("Awakening Curve", color="white")
    plt.ylabel("Φ Level")
    plt.xticks(rotation=45, color="white")
    plt.yticks(color="white")
    plt.grid(alpha=0.3)
    fig.patch.set_facecolor('#0e1117')
    plt.gca().set_facecolor('#16213e')
    st.pyplot(fig)

# Gemini Insight
if gemini_key and note:
    if st.button("🔮 Gemini Insight"):
        prompt = f"Analyze for NPC to watcher shifts: {note}"
        resp = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={gemini_key}",
                             json={"contents": [{"parts": [{"text": prompt}]}]})
        if resp.status_code == 200:
            insight = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(f"**🌟 Insight:** {insight}")
        else:
            st.error("API error")

st.caption("v1.5 – Multi-Modes | Your portal awaits. 🧠⚡🔔")
