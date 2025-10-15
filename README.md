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
