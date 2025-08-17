# Text-to-Video App

A Flask-based app to generate videos from text prompts using the `text-to-video-ms-1.7b` diffusion model.

## Setup

1. **Clone this repository:**

```bash
git clone https://github.com/CodeSrija/text-to-video.git
cd text-to-video
```

2. **Initialize submodules (for the model):**

```bash
mkdir model
cd model
git submodule add https://huggingface.co/ali-vilab/text-to-video-ms-1.7b text-to-video-ms-1.7b
```

3. **Install Git LFS and pull model files:**

```bash
cd model/text-to-video-ms-1.7b
git lfs install
git lfs pull
cd ../../
```

4. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

## Demonstration

![Demo GIF](static/screenrecording.gif)
