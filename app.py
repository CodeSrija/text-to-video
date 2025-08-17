from flask import Flask, render_template, request
from inference import predict, progress

app = Flask(__name__)

@app.route("/progress")
def get_progress():
    from inference import progress
    return progress

@app.route("/", methods=["GET", "POST"])
def home():
    video_path = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        num_inference_steps = int(request.form.get("num_inference_steps", 25))
        video_time = int(request.form.get("video_time", 5))

        # Determine frames based on video time
        fps = 8
        num_frames = max(8, video_time * fps)

        if prompt:
            video_path = predict(
                prompt, 
                num_frames=num_frames, 
                num_inference_steps=num_inference_steps
            )

    return render_template("index.html", output=video_path)

if __name__ == "__main__":
    app.run(debug=True)
