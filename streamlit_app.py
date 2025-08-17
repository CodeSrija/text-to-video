# app_streamlit.py
import streamlit as st
from inference import predict, progress
import time
import os

# Page setup
st.set_page_config(page_title="Text-to-Video Generator", layout="wide")

# Title & description
st.title("🎬 Text-to-Video Generator")
st.markdown("Generate short videos from text prompts using the 1.7B model.")

# Sidebar controls
st.sidebar.header("Video Settings")
num_frames = st.sidebar.slider("Number of Frames", min_value=8, max_value=64, value=16, step=1)
num_inference_steps = st.sidebar.slider("Inference Steps", min_value=5, max_value=50, value=25, step=1)
video_time = st.sidebar.slider("Video Duration (seconds)", min_value=1, max_value=15, value=5, step=1)

# Prompt input
prompt = st.text_input("Enter your text prompt:")

# Placeholder for video & progress
video_placeholder = st.empty()
progress_text = st.empty()

# Generate button
if st.button("Generate Video"):
    if not prompt.strip():
        st.warning("Please enter a prompt!")
    else:
        # Start video generation
        st.info("Starting video generation...")
        
        # Determine frames based on video time
        fps = 8
        num_frames = max(8, video_time * fps)
        
        # Run prediction
        video_path = predict(prompt, num_frames=num_frames, num_inference_steps=num_inference_steps)

        # Display video
        if os.path.exists(video_path):
            video_placeholder.video(video_path)
            st.success(f"Video saved at `{video_path}`")
        else:
            st.error("Video generation failed.")

# Progress updater
def update_progress():
    while progress["pct"] < 100:
        progress_text.text(f"{progress['stage']} ({progress['pct']}%)")
        time.sleep(0.5)
    progress_text.text(f"{progress['stage']} ({progress['pct']}%)")

# Start a background progress updater
if st.button("Show Progress"):
    update_progress()
