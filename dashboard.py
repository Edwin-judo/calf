import streamlit as st
import os
from pipeline import analyze_video
from risk_engine import calculate_risk

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CalfWatch AI",
    page_icon="🐄",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🐄 CalfWatch AI")
st.subheader("Newborn Calf Health & Survival Risk Prediction")

st.info(
    "⚠️ Early-warning decision-support prototype. "
    "Not a clinically validated veterinary diagnostic system."
)

st.divider()

# --------------------------------------------------
# FILE PATH
# --------------------------------------------------

VIDEO_PATH = "data/test_videos/calf_test.mp4"

# --------------------------------------------------
# INPUT CONTROLS & VIDEO SECTION
# --------------------------------------------------

st.header("🎥 Calf Video Analysis")

video_col, control_col = st.columns([1.5, 1])

with video_col:
    if os.path.exists(VIDEO_PATH):
        st.video(VIDEO_PATH)
    else:
        st.error(f"Test video not found at: {VIDEO_PATH}")

with control_col:
    st.subheader("🤖 AI Analysis Controls")
    
    time_to_stand = st.number_input(
        "Time to Stand (seconds)",
        min_value=0,
        value=40
    )
    
    time_to_suckle = st.number_input(
        "Time to First Suckle (seconds)",
        min_value=0,
        value=90
    )

    if st.button("▶ Run AI Analysis", type="primary"):
        with st.spinner("Analyzing calf video..."):
            result = analyze_video(VIDEO_PATH)
            if result is None:
                st.error("Could not process the video.")
            else:
                st.session_state["result"] = result
                st.success("Analysis completed successfully.")

    if st.button("Calculate Risk"):
        risk, score = calculate_risk(time_to_stand, time_to_suckle)
        st.session_state["manual_risk"] = risk
        st.session_state["manual_score"] = score
        st.success(f"Risk calculated: {risk} (Score: {score})")

st.divider()

# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "result" not in st.session_state:
    st.info("Click 'Run AI Analysis' to analyze the calf video.")
else:
    status = st.session_state["result"]

    # --------------------------------------------------
    # CALF MONITORING METRICS
    # --------------------------------------------------
    st.header("🐄 Calf Monitoring")
    col1, col2, col3 = st.columns(3)

    with col1:
        detection_text = "Detected" if status.get("calf_detected", False) else "Not Detected"
        st.metric("Calf Detection", detection_text)

    with col2:
        st.metric("Current Behaviour", status.get("current_behavior", "Unknown"))

    with col3:
        st.metric("Monitoring Status", status.get("monitoring_status", "Unknown"))

    st.divider()

    # --------------------------------------------------
    # BEHAVIOUR TIMING
    # --------------------------------------------------
    st.header("⏱️ Behaviour Timing")
    time_col1, time_col2 = st.columns(2)

    with time_col1:
        t_stand = status.get("time_to_stand")
        if t_stand is not None:
            st.metric("Time to Stand", f"{t_stand:.2f} sec")
        else:
            st.metric("Time to Stand", "Not detected")

    with time_col2:
        t_suckle = status.get("time_to_suckle")
        if t_suckle is not None:
            st.metric("Time to First Suckle", f"{t_suckle:.2f} sec")
        else:
            st.metric("Time to First Suckle", "Not detected")

    st.divider()

    # --------------------------------------------------
    # HEALTH RISK ANALYSIS
    # --------------------------------------------------
    st.header("⚠️ Health Risk Analysis")
    risk_col1, risk_col2 = st.columns(2)

    risk_score = status.get("risk_score", 0)
    risk_level = status.get("risk_level", "UNKNOWN")

    with risk_col1:
        st.metric("Risk Score", risk_score)

    with risk_col2:
        st.metric("Risk Level", risk_level)

    if risk_level == "LOW":
        st.success("🟢 LOW RISK — Calf behaviour indicators are currently within the prototype's expected range.")
    elif risk_level == "MEDIUM":
        st.warning("🟡 MEDIUM RISK — Monitor the calf closely for delayed behaviour indicators.")
    else:
        st.error("🔴 HIGH RISK — Immediate attention recommended. Early-warning alert: delayed behaviour indicators detected.")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.caption("CalfWatch AI | Prototype for early-warning decision support.")