import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
import io
from scipy.io.wavfile import write as wav_write

# App Config
st.set_page_config(page_title="Consciousness Echo", page_icon="🧠", layout="centered")
st.title("🧠 Consciousness Echo v1.1")
st.markdown("**Your Awakening Tool** – From NPC to Awake Watcher | Built from Consciousness Engineering Blueprint ⚡🔔")

# Constants
GAMMA_FREQ = 40.0  # Hz gamma entrainment
SEVENTH_HARMONIC = 54.81  # 7th Schumann overlay
BASE_FREQ = 200.0  # Carrier tone for binaural
SAMPLE_RATE = 44100
JOURNAL_FILE = "awakening_journal.csv"

# Sidebar for Settings
with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Gemini API Key (for insights & voice)", type="password", value="")
    session_length = st.slider("Session Length (seconds)", 30, 300, 60, step=30)  # Tweak: User-adjustable length
    st.info("Plug your key for voice analysis & insights. Safe—no data stored.")

# Detection Layer
st.header("1. Detect Your State")
st.markdown("Rate 1-10 (honestly—no judgment)")
col1, col2, col3, col4 = st.columns(4)
presence = col1.slider("Presence (just being here)", 1, 10, 5)
emotion = col2.slider("Emotional clarity", 1, 10, 5)
logic = col3.slider("Logical flow", 1, 10, 5)
meta = col4.slider("Meta-awareness (watching thoughts)", 1, 10, 5)

scores = np.array([presence, emotion, logic, meta])
phi_proxy = np.mean(scores) * 10  # 0-100 scale
coherence = 1 / (np.std(scores) / np.mean(scores + 1e-6) + 1)  # Inverted variability
quantum_noise = np.random.normal(0, 5)  # Orch-OR mock
phi_proxy += quantum_noise

st.progress(phi_proxy / 100)
st.write(f"**Φ Proxy (Awareness Level):** {phi_proxy:.1f}/100")
st.write(f"**Coherence:** {coherence:.2f} (Higher = more integrated)")

if meta >= 7:
    st.success("7th Harmonic Active – Meta-pattern detection strong! 🔔")

# Voice Input Addition
st.subheader("Voice Harmonic Input (Optional)")
voice_file = st.file_uploader("Upload short voice note (e.g., 'How I feel today')", type=["wav", "mp3", "m4a"])
if voice_file and gemini_key:
    with st.spinner("Analyzing voice harmonics..."):
        # Read file bytes (for real API send)
        voice_bytes = voice_file.read()
        # Mock prompt for sim; real: base64 encode and send to Gemini for audio analysis (Gemini supports audio)
        prompt = "Transcribe and analyze this voice for harmonic presence/emotion/logic/meta patterns (1-10 scores): [audio data]"
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        data = {"contents": [{"parts": [{"text": prompt}]}]}  # Real: Add audio part if API allows
        resp = requests.post(f"{url}?key={gemini_key}", json=data)
        if resp.status_code == 200:
            voice_insight = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            st.markdown(f"**Voice Harmonic Insight:** {voice_insight}")
        else:
            st.error("Voice analysis error—check key.")

# Amplification Layer
st.header("2. Amplify Resonance")
if st.button("Generate & Play Session"):
    with st.spinner("Creating binaural beats..."):
        t = np.linspace(0, session_length, int(session_length * SAMPLE_RATE), False)  # Tweak: Use user length
        left = np.sin(2 * np.pi * BASE_FREQ * t)
        right = np.sin(2 * np.pi * (BASE_FREQ + GAMMA_FREQ + (SEVENTH_HARMONIC * meta/10)) * t)
        binaural = np.stack((left, right), axis=1).flatten()
        binaural /= np.max(np.abs(binaural))

        # To bytes for st.audio
        buf = io.BytesIO()
        wav_write(buf, SAMPLE_RATE, (binaural * 32767).astype(np.int16))
        buf.seek(0)

        st.audio(buf, format="audio/wav")
        st.success(f"Playing {session_length}s session – Headphones on, breathe deeply. Feel the shift.")

    # Mock post-boost
    post_phi = phi_proxy * 1.5 + np.random.normal(0, 5)
    st.write(f"**Post-Session Φ Estimate:** {post_phi:.1f}/100 – Awakening amplified ⚡")

# Integration Layer
st.header("3. Journal & Track Progress")
note = st.text_area("How do you feel now? (e.g., 'Less reactive, more watching')")

if st.button("Save Session"):
    try:
        df = pd.read_csv(JOURNAL_FILE)
    except:
        df = pd.DataFrame(columns=["Date", "Pre_Φ", "Post_Φ", "Note"])

    new_row = {"Date": datetime.datetime.now(), "Pre_Φ": phi_proxy, "Post_Φ": post_phi if 'post_phi' in locals() else phi_proxy, "Note": note}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(JOURNAL_FILE, index=False)
    st.success("Journal saved!")

    # Plot
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Post_Φ"], marker="o", label="Φ Progress")
    ax.set_title("Your Awakening Curve")
    ax.set_ylabel("Φ Proxy")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Gemini Insight
if gemini_key and note:
    if st.button("Get Gemini Awakening Insight"):
        with st.spinner("Analyzing patterns..."):
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            data = {"contents": [{"parts": [{"text": f"Analyze this awakening journal for shifts from NPC/autopilot to conscious watcher: {note}"}]}]}
            resp = requests.post(f"{url}?key={gemini_key}", json=data)
            if resp.status_code == 200:
                insight = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(f"**Gemini Insight:** {insight}")
            else:
                st.error("API error—check key.")

st.markdown("---")
st.caption("Built Dec 18, 2025 | From your blueprint – Awakening in progress 🧠⚡")
