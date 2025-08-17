import os
import torch
import numpy as np
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

# Path to pretrained model
MODEL_PATH = "./model/text-to-video-ms-1.7b"
# Output video path inside static folder so Flask can serve it
VIDEO_FILE = "static/output_video.mp4"

# Global pipeline object
pipe = None

# Shared progress state
progress = {"stage": "Idle", "pct": 0}


def update_progress(stage: str, pct: int):
    """
    Update the global progress state for UI feedback.
    
    Args:
        stage (str): Current stage description
        pct (int): Completion percentage (0-100)
    """
    global progress
    progress["stage"] = stage
    progress["pct"] = pct


def load_model():
    """
    Load the text-to-video diffusion pipeline if not already loaded.
    
    Returns:
        DiffusionPipeline: The loaded pipeline object
    """
    global pipe
    if pipe is None:
        update_progress("📦 Loading model pipeline...", 0)
        pipe = DiffusionPipeline.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
            torch_dtype=torch.float16
        )
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
        pipe.to("cuda")
        update_progress("✅ Model loaded successfully!", 100)
    return pipe


def predict(prompt: str, num_frames: int = 16, num_inference_steps: int = 25) -> str:
    """
    Generate a video from a text prompt.
    
    Args:
        prompt (str): The text prompt describing the video
        num_frames (int): Number of frames to generate
        num_inference_steps (int): Diffusion steps for each frame

    Returns:
        str: Path to the generated video file
    """
    pipe = load_model()
    update_progress("🎬 Generating frames... This might take a few minutes", 0)

    frames = pipe(prompt, num_inference_steps=num_inference_steps, num_frames=num_frames).frames
    processed_frames = []

    total_batches = len(frames)
    for i, batch in enumerate(frames):
        for frame in batch:
            # Remove alpha channel if present
            if frame.shape[-1] == 4:
                frame = frame[..., :3]
            processed_frames.append((frame * 255).astype(np.uint8))
        update_progress(f"🖼 Processing frames {i+1}/{total_batches}", int((i+1) / total_batches * 100))

    update_progress("💾 Exporting video...", 0)
    export_to_video(processed_frames, output_video_path=VIDEO_FILE)
    update_progress(f"✅ Video saved at {VIDEO_FILE}", 100)

    return VIDEO_FILE
