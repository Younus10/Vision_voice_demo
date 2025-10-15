
# YOLO Video Analysis with Voice Summary 🎥🗣️

## Concept / Motivation
This project demonstrates a **prototype of smart spectacles** that help visually impaired users understand their surroundings.  
By analyzing a short video (simulating what the spectacles capture), the system:

- Detects objects in the scene.
- Provides a **friendly text description** of what’s around.
- Converts the description to **speech** so a user can hear it.

Think of it as a **vision-to-voice system** that translates visual information into audible, meaningful feedback.

---

## Overview
The system automatically generates:

1. **Annotated frames** showing detected objects.
2. **Text summary** of the objects detected in a natural, friendly sentence.
3. **Audio narration** of the summary using text-to-speech.

It uses **YOLOv8 (medium)** for object detection, OpenCV for video processing, and **Gradio** for a web interface.

---

## Features
- Extracts key frames from the video for faster processing.
- Enhances brightness & contrast of frames for better detection.
- Detects multiple objects and aggregates them into a human-readable summary.
- Generates **friendly text summaries**, e.g.:  
  *"It looks like you're near a bottle, a mouse, and a cell phone."*
- Converts the summary to audio using `gTTS`.
- Displays **annotated frames** with bounding boxes and labels.

---

## Working Examples / Use Cases

### Example 1: High-Quality Video
**Input:**  
![High-Quality Input]

**Output:**  
<img width="1710" height="1031" alt="Screenshot 2025-10-14 at 8 43 06 PM" src="https://github.com/user-attachments/assets/902a61cc-68a6-44c0-8b58-fa3da6b9edd3" />


**Text Summary:**  
```

It looks like you're near a bottle, a mouse, and a cell phone.

```

**Observation:**  
- High-resolution and clear videos result in **accurate detection** of multiple objects.  
- Bounding boxes align well with objects, and the summary is precise.

---

### Example 2: Blurry / Low-Quality Video
**Input:**  
![Blurry Input](assets/blurry_video.jpg)

**Output Annotated Frame:**  
![Annotated Output](assets/blurry_output.jpg)

**Text Summary:**  
```

I couldn't detect any familiar objects in the video.

```

**Observation:**  
- Blurry or low-resolution videos reduce detection accuracy.  
- Some objects may be missed or misclassified, showing the importance of video quality.

---

### Example 3: Mixed Scenario Video
**Input:**  
![Mixed Input](assets/mixed_video.jpg)

**Output Annotated Frame:**  
![Annotated Output](assets/mixed_output.jpg)

**Text Summary:**  
```

It appears there’s a bottle, a laptop, and a mouse.

````

**Observation:**  
- Partial clarity in the video still allows detection of major objects.  
- Some smaller or obscured objects may not be recognized.

---

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/yolo_video_analysis.git
cd yolo_video_analysis
````

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Download the YOLOv8 medium model (`yolov8m.pt`) from [Ultralytics YOLOv8 release page](https://github.com/ultralytics/ultralytics/releases) and place it in the project root.

---

## Usage

Run the app:

```bash
python app.py
```

* Open `http://127.0.0.1:7860` in your browser.
* Upload a short video (mp4 recommended).
* Click **Process Video**.
* View the annotated frame, read the text summary, and listen to the audio narration.

---

## Customization

* **YOLO model**: Change `YOLO("yolov8m.pt")` to `yolov8n.pt` for faster but less accurate detection.
* **Frame sampling**: Adjust `step` and `max_frames` in `extract_sampled_frames()` for faster/slower analysis.
* **Friendly summary**: Toggle `friendly=True/False` in `aggregate_detections()` to control tone.

---

## Notes

* Works best with videos where objects are clearly visible.
* Supports multiple objects per frame.
* Ensure your environment can play audio for `gTTS` output.
* You can add sample videos in the `assets/` folder for testing.

---

## Dependencies

* Python 3.10+
* [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
* OpenCV
* NumPy
* gTTS
* Gradio

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## License

MIT License

