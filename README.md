# YOLO Video Analysis with Voice Summary

## Overview
This project allows you to upload a short video and automatically generates:

1. **Annotated frames** showing detected objects.
2. **Text summary** of the objects detected in a natural, friendly sentence.
3. **Audio narration** of the summary using text-to-speech.

It uses **YOLOv8 (medium)** for object detection, OpenCV for video processing, and **Gradio** for a web interface.

---

## Features
- Extracts key frames from the video for faster processing.
- Enhances brightness & contrast of frames for better detection.
- Detects multiple objects and aggregates them into a human-readable summary.
- Generates **friendly text summaries** like:  
  *"It looks like you're near a bottle, a mouse, and a cell phone."*
- Converts the summary to audio using `gTTS`.
- Displays **annotated frames** with bounding boxes and labels.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/yolo_video_analysis.git
cd yolo_video_analysis
Install Python dependencies:

bash
Copy code
pip install -r requirements.txt
Download the YOLOv8 medium model (yolov8m.pt) from Ultralytics YOLOv8 release page and place it in the project root.

Usage
Run the app:

bash
Copy code
python app.py
Open http://127.0.0.1:7860 in your browser.

Upload a short video (mp4 recommended).

Click Process Video.

View the annotated frame, text summary, and listen to the audio narration.

Customization
YOLO model: Change YOLO("yolov8m.pt") to yolov8n.pt (nano) for faster but less accurate detection.

Frame sampling: Adjust step and max_frames in extract_sampled_frames() for faster/slower analysis.

Friendly summary: Toggle friendly=True/False in aggregate_detections() to control tone.

Notes
Works best with videos where objects are clearly visible.

Supports multiple objects per frame.

Ensure your environment can play audio for gTTS output.

You can add sample videos in the assets/ folder for testing.

Dependencies
Python 3.10+

Ultralytics YOLOv8

OpenCV

NumPy

gTTS

Gradio

Install all dependencies with:

bash
Copy code
pip install -r requirements.txt
License
MIT License
