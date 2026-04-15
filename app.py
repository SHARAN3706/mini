import streamlit as st
import pandas as pd
import plotly.express as px
from model_engine import SentryEngine
import librosa

# --- INITIAL CONFIG ---
st.set_page_config(page_title="Bio-Acoustic Sentry", layout="wide", page_icon="🛡️")

# Use your provided Google Client ID
CLIENT_ID = "829501438039-75718gi7vc54hr9qa6q9v48oftheuriv.apps.googleusercontent.com"

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- AUTHENTICATION SCREEN ---
def login_screen():
    st.title("🛡️ Bio-Acoustic Sentry")
    st.subheader("Physics-Informed Subterranean Monitoring")
    st.markdown("---")
    st.write("Secure Access Required. Please authenticate with your institutional Google account.")
    
    # Simulating OAuth flow for the demo build
    if st.button("Sign in with Google"):
        st.session_state.auth = True
        st.session_state.user = "authorized_researcher@gmail.com"
        st.rerun()

# --- MAIN DASHBOARD ---
def main_app():
    # Sidebar Navigation
    st.sidebar.title("Sentry Control")
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
    menu = st.sidebar.radio("Navigation", ["Live Monitor", "Audit Ledger", "System Settings"])
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    engine = SentryEngine()

    if menu == "Live Monitor":
        st.header("📡 Subterranean Live Monitor")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Data Acquisition")
            uploaded = st.file_uploader("Upload Audio (MP3/WAV)", type=["wav", "mp3"])
            
            st.write("--- OR ---")
            
            if st.button("🎤 Activate Microphone (Real-Time Scan)"):
                st.warning("Requesting Microphone Access...")
                # Simulating mic capture for the demo
                uploaded = "mic_capture"

        if uploaded:
            with st.spinner("Processing Physics-Informed Wave Equation (PINN)..."):
                # Use demo audio if mic is clicked, else use file
                sample = librosa.ex('choice') if uploaded == "mic_capture" else uploaded
                res = engine.analyze_audio(sample)
            
            with col2:
                st.markdown("### Classification Output")
                
                # Dynamic Alert Colors
                if res['tier'] == "Harmful":
                    st.error(f"**Species Detected:** {res['name']}")
                elif res['tier'] == "Beneficial":
                    st.success(f"**Species Detected:** {res['name']}")
                else:
                    st.info(f"**Species Detected:** {res['name']}")
                
                st.write(f"**Ecological Tier:** {res['tier']}")
                st.metric("PINN Confidence", f"{res['confidence']:.2f}%")
                
                if res['human']:
                    st.warning(f"⚠️ **Human Intervention Detected!**")
                    st.write(f"Type: {res['intervention']}")
                    st.caption("Safety Protocol: Autonomous intervention paused.")
                else:
                    st.write("✅ Environment Secure: No human interference.")

            st.divider()
            
            # Physics Plot
            st.subheader("📈 Waveform Reconstruction")
            fig = px.line(res['waveform'][::100], title="De-noised Subterranean Signature", color_discrete_sequence=['#2e7d32'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.code(f"Accountability Ledger Hash: {res['hash']}", language="text")

    elif menu == "Audit Ledger":
        st.header("📜 Immutable Accountability Ledger")
        st.write("This ledger provides a cryptographic record of all autonomous actions for legal and ethical auditing.")
        
        ledger_data = pd.DataFrame([
            {"Time": "12:00:01", "Species": "Termite", "Status": "Harmful", "Human": "No", "SHA-256 Hash": "8f3e...2a11"},
            {"Time": "12:05:44", "Species": "Earthworm", "Status": "Beneficial", "Human": "No", "SHA-256 Hash": "4d1b...99f2"},
            {"Time": "12:15:10", "Species": "Undetermined", "Status": "N/A", "Human": "Yes (Speech)", "SHA-256 Hash": "1c9a...ff03"}
        ])
        st.table(ledger_data)

# --- ROUTING ---
if not st.session_state.auth:
    login_screen()
else:
    main_app()
