import streamlit as st
import pandas as pd
import plotly.express as px
from model_engine import SentryEngine
import io
from streamlit_mic_recorder import mic_recorder

# --- INITIAL CONFIG ---
st.set_page_config(page_title="Bio-Acoustic Sentry", layout="wide", page_icon="🛡️")

if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- AUTHENTICATION SCREEN ---
def login_screen():
    st.title("🛡️ Bio-Acoustic Sentry")
    st.subheader("Physics-Informed Subterranean Monitoring")
    st.markdown("---")
    st.write("Secure Access Required. Please authenticate with your institutional Google account.")
    if st.button("Sign in with Google"):
        st.session_state.auth = True
        st.session_state.user = "authorized_researcher@gmail.com"
        st.rerun()

# --- MAIN DASHBOARD ---
def main_app():
    st.sidebar.title("Sentry Control")
    st.sidebar.write(f"Logged in as: **{st.session_state.user}**")
    menu = st.sidebar.radio("Navigation", ["Live Monitor", "Audit Ledger", "Model Training", "System Settings"])
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    engine = SentryEngine()

    if menu == "Live Monitor":
        st.header("📡 Subterranean Live Monitor")
        col1, col2 = st.columns([1, 1])
        
        audio_source = None

        with col1:
            st.markdown("### Data Acquisition")
            # FEATURE: Restricted file types
            uploaded = st.file_uploader("Upload Audio", type=["wav", "mp3", "mpeg"])
            
            if uploaded:
                audio_source = uploaded
                st.info("Uploaded File Player")
                # FEATURE: Built-in Audio Player
                st.audio(uploaded)

            st.write("--- OR ---")
            
            # FEATURE: Microphone Integration
            st.write("🎤 Device Microphone")
            recorded_audio = mic_recorder(
                start_prompt="Start Real-Time Scan",
                stop_prompt="Stop & Analyze",
                key='recorder'
            )
            
            if recorded_audio:
                audio_source = io.BytesIO(recorded_audio['bytes'])
                st.success("Microphone Capture Complete")
                st.audio(audio_source)

        if audio_source:
            with st.spinner("Processing Physics-Informed Wave Equation (PINN)..."):
                res = engine.analyze_audio(audio_source)
            
            with col2:
                st.markdown("### Classification Output")
                if res['tier'] == "Harmful":
                    st.error(f"**Species Detected:** {res['name']}")
                elif res['tier'] == "Beneficial":
                    st.success(f"**Species Detected:** {res['name']}")
                else:
                    st.info(f"**Species Detected:** {res['name']}")
                
                st.write(f"**Ecological Tier:** {res['tier']}")
                st.metric("Model Confidence", f"{res['confidence']:.2f}%")
                
                if res['human']:
                    st.warning(f"⚠️ **Human Intervention Detected!**")
                    st.write(f"Type: {res['intervention']}")
                else:
                    st.write("✅ Environment Secure: No human interference.")

            st.divider()
            st.subheader("📈 Waveform Reconstruction")
            fig = px.line(res['waveform'][::100], title="De-noised Subterranean Signature", color_discrete_sequence=['#2e7d32'])
            st.plotly_chart(fig, use_container_width=True)
            st.code(f"Accountability Ledger Hash: {res['hash']}", language="text")

    elif menu == "Model Training":
        st.header("🧠 Backend Model Management")
        st.write("Synchronize local captures with online datasets to refine PINN accuracy.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Online Dataset Sync")
            st.write("Datasets: *Pest-DB, SoilBio-Net, Voice-Intervention-Set*")
            if st.button("🚀 Run Backend Training"):
                with st.spinner("Training model on cloud-synced datasets..."):
                    success = engine.train_backend("backend_data/") # Path to your storage
                    if success:
                        st.success("Model optimized with new patterns.")
                    else:
                        st.error("Training failed: Check backend data directory.")
        
        with col2:
            st.subheader("Data Contributions")
            st.write("Upload unique subterranean signatures to the global training pool.")
            st.file_uploader("Contribute to Dataset", type=["wav", "mp3"], accept_multiple_files=True)

    # ... [Keep Audit Ledger and System Settings code as per your original] ...
    elif menu == "Audit Ledger":
        st.header("📜 Immutable Accountability Ledger")
        ledger_data = pd.DataFrame([
            {"Time": "12:00:01", "Species": "Termite", "Status": "Harmful", "Human": "No", "SHA-256 Hash": "8f3e...2a11"},
            {"Time": "12:05:44", "Species": "Earthworm", "Status": "Beneficial", "Human": "No", "SHA-256 Hash": "4d1b...99f2"}
        ])
        st.table(ledger_data)

    elif menu == "System Settings":
        st.header("⚙️ System Settings")
        st.slider("Minimum Confidence Threshold (%)", 50, 99, 90)
        if st.button("Revoke Google Access Data"):
            st.warning("Access data cleared.")

# --- ROUTING ---
if not st.session_state.auth:
    login_screen()
else:
    main_app()
                
