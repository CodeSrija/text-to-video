// Grab DOM elements
const form = document.getElementById('video-form');
const resetBtn = document.getElementById('reset-btn');

const framesSlider = document.getElementById('num_frames');
const stepsSlider = document.getElementById('num_inference_steps');
const timeSlider = document.getElementById('video_time');

// Update slider values in real-time
framesSlider.oninput = () => document.getElementById('frames-val').innerText = framesSlider.value;
stepsSlider.oninput = () => document.getElementById('steps-val').innerText = stepsSlider.value;
timeSlider.oninput = () => document.getElementById('time-val').innerText = timeSlider.value;

// Poll server for progress updates
function pollProgress() {
    fetch("/progress")
        .then(res => res.json())
        .then(data => {
            const progressContainer = document.getElementById('progress-container');
            const progressText = document.getElementById('progress-text');

            // Show only progress text
            progressContainer.style.display = 'block';
            progressText.innerText = data.stage;

            // Continue polling until complete
            if (data.pct < 100) {
                setTimeout(pollProgress, 500);
            }
        })
        .catch(() => setTimeout(pollProgress, 1000));
}

// Handle form submission
form.addEventListener('submit', function() {
    // Hide placeholder while generating video
    const placeholder = document.querySelector('.video-container .placeholder');
    if (placeholder) placeholder.style.display = 'none';

    // Start polling for progress
    pollProgress();
});
