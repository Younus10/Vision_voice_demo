# app.py
import os
import tempfile
import shutil
import cv2
import numpy as np
from ultralytics import YOLO
from gtts import gTTS
import gradio as gr
from collections import Counter
import random

# --- Load YOLOv8 model (medium version for higher accuracy) ---
model = YOLO("yolov8m.pt")  # 'm' = medium, more accurate than 'n'


# --- Extract frames from the video ---
def extract_sampled_frames(video_path, step=10, max_frames=15):
    """
    Extract frames every `step` frames (≈3 fps @30fps) up to max_frames.
    Returns a list of (frame_index, frame_bgr_numpy).
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    idx = 0
    saved = 0
    while cap.isOpened() and saved < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % step == 0:
            frames.append((idx, frame.copy()))
            saved += 1
        idx += 1
    cap.release()
    return frames


# --- Draw boxes and labels on frame ---
def annotate_frame(frame, boxes):
    """Draw bounding boxes and labels on a frame (BGR)."""
    annotated = frame.copy()
    for box in boxes:
        x1, y1, x2, y2 = map(int, box["xyxy"])
        cls_name = box["label"]
        conf = box["conf"]
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        text = f"{cls_name} {conf:.2f}"
        cv2.putText(annotated, text, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return annotated


# --- Generate summary sentence (friendly or concise) ---
def aggregate_detections(all_detections, top_k=5, friendly=False):
    """
    Summarize detected objects into a natural, human-like sentence.
    - all_detections: list of detected object labels
    - top_k: number of top objects to include
    - friendly: if True, generates a conversational summary
    """
    counts = Counter(all_detections)
    if not counts:
        return "I couldn't detect any familiar objects in the video."

    common = [obj for obj, cnt in counts.most_common(top_k)]

    if len(common) == 1:
        core_sentence = f"a {common[0]}"
    elif len(common) == 2:
        core_sentence = f"a {common[0]} and a {common[1]}"
    else:
        last = common.pop()
        core_sentence = f"a {', a '.join(common)}, and a {last}"

    if friendly:
        prefixes = [
            "It looks like you're near",
            "Seems like there’s",
            "I can spot",
            "You might be around",
            "It appears there’s"
        ]
        prefix = random.choice(prefixes)
        return f"{prefix} {core_sentence}."
    else:
        return f"I see {core_sentence}."


# --- Process uploaded video ---
def process_video(video_file):
    tmp_dir = tempfile.mkdtemp()
    video_path = os.path.join(tmp_dir, "input.mp4")

    # Handle Gradio file input variations
    if isinstance(video_file, dict) and "name" in video_file:
        src_path = video_file["name"]
        shutil.copy(src_path, video_path)
    elif hasattr(video_file, "name"):
        src_path = video_file.name
        shutil.copy(src_path, video_path)
    else:
        with open(video_path, "wb") as f:
            f.write(video_file.read())

    # Extract more frames for richer detection
    frames = extract_sampled_frames(video_path, step=10, max_frames=15)
    all_labels = []
    annotated_img_path = None

    # --- Object Detection with YOLO ---
    for i, (frame_idx, frame_bgr) in enumerate(frames):
        # Improve brightness & contrast slightly
        frame_bgr = cv2.convertScaleAbs(frame_bgr, alpha=1.2, beta=20)

        # Run YOLO detection with lower confidence threshold
        results = model(frame_bgr, conf=0.15, iou=0.5)
        r = results[0]
        boxes = []

        for det in r.boxes:
            cls_id = int(det.cls.cpu().numpy())
            label = model.names.get(cls_id, str(cls_id))
            conf = float(det.conf.cpu().numpy())
            xyxy = det.xyxy.cpu().numpy().flatten().tolist()
            boxes.append({"label": label, "conf": conf, "xyxy": xyxy})
            all_labels.append(label)

        # Print detections for debugging
        if boxes:
            print(f"Frame {i}: Detected {', '.join([b['label'] for b in boxes])}")

        # Save the first annotated frame for display
        if boxes and annotated_img_path is None:
            annotated = annotate_frame(frame_bgr, boxes)
            annotated_img_path = os.path.join(tmp_dir, f"annotated_{i}.jpg")
            cv2.imwrite(annotated_img_path, annotated)

    # Fallback frame if nothing detected visually
    if annotated_img_path is None and frames:
        _, frame_bgr = frames[0]
        annotated_img_path = os.path.join(tmp_dir, "fallback.jpg")
        cv2.imwrite(annotated_img_path, frame_bgr)

    # Summarize detected objects (friendlier tone)
    summary = aggregate_detections(all_labels, top_k=5, friendly=True)

    # Text-to-Speech output (slower, clearer)
    tts = gTTS(summary, lang="en", slow=True)
    audio_path = os.path.join(tmp_dir, "summary.mp3")
    tts.save(audio_path)

    return summary, audio_path, annotated_img_path


# --- Gradio Web UI ---
with gr.Blocks() as demo:
    gr.Markdown("## 🎥 Vision→Voice Prototype (Enhanced Smart Spectacles Demo)\nUpload a short video and let the system describe what it sees with improved precision and natural narration.")

    with gr.Row():
        video_in = gr.File(label="Upload video (mp4 recommended)", file_types=["video"])
        run_btn = gr.Button("🔍 Process Video")

    output_summary = gr.Textbox(label="Summary (text)", interactive=False)
    output_audio = gr.Audio(label="Narration (audio)", interactive=False)
    output_image = gr.Image(label="Annotated Frame")

    def on_process(video_obj):
        if video_obj is None:
            return "No video uploaded.", None, None
        return process_video(video_obj)

    run_btn.click(on_process, inputs=[video_in], outputs=[output_summary, output_audio, output_image])


# --- Run the Gradio App ---
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
