# SafeVision AI

Real-Time Indoor Fall Detection using Edge AI on NVIDIA Jetson Orin Nano.

![Python](https://img.shields.io/badge/Python-3.8-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-red)
![Platform](https://img.shields.io/badge/Platform-Jetson%20Orin%20Nano-green)

---

## Overview

SafeVision AI is a privacy-preserving, edge-based fall detection system. All processing happens 100% on-device. Falls are detected using YOLOv8n-Pose skeleton keypoint analysis and confirmed using a 5-frame majority vote algorithm.

---

## Features

- Real-time fall detection using human pose estimation
- Live web dashboard with skeleton overlay and event log
- Instant email and SMS alerts with snapshot on fall detection
- 100% on-device processing — zero cloud dependency
- Runs on NVIDIA Jetson Orin Nano (JetPack 5.1.4)
- Threaded camera capture for maximum throughput
- SQLite event logging with timestamps and angles

---

## Hardware Requirements

- NVIDIA Jetson Orin Nano
- USB Camera 640x480 at 30 FPS
- Local Wi-Fi network

---

## Software Stack

| Layer | Technology |
|-------|------------|
| Pose estimation | YOLOv8n-Pose (Ultralytics) |
| Deep learning | PyTorch (Jetson-specific build) |
| Computer vision | OpenCV |
| Web server | Flask + Flask-SocketIO |
| Database | SQLite |
| Email alerts | SendGrid API |
| SMS alerts | Twilio API |
| Operating system | Ubuntu 20.04 / JetPack 5.1.4 |

---
## Project Architecture

<img width="696" height="394" alt="Screenshot 2026-05-19 at 21 22 42" src="https://github.com/user-attachments/assets/d1cd68cc-1201-40ab-9900-17e0b8626729" />


## Project Structure

```
safevision/
├── main.py               Entry point, runs full pipeline
├── config.py             All settings and thresholds
├── camera.py             Threaded USB camera capture
├── pose_estimator.py     YOLOv8n-Pose keypoint extraction
├── fall_detector.py      Torso angle and majority vote logic
├── alerts.py             Email, SMS, and snapshot on fall
├── logger.py             SQLite event logging
├── display.py            OpenCV skeleton overlay
└── dashboard/
    ├── app.py            Flask and SocketIO server
    ├── templates/
    │   └── index.html    Dashboard UI
    └── static/
        ├── style.css     Dark theme styling
        └── app.js        Live feed and event log logic
```

---

## How It Works

```
USB Camera (640x480 at 30 FPS)
        |
        v
camera.py
Threaded background frame capture
        |
        v
pose_estimator.py
YOLOv8n-Pose detects 17 body keypoints
Inference at 256x256 for speed
        |
        v
fall_detector.py
Computes torso angle using arctan2
Majority vote: 3 out of 5 frames above 45 degrees
        |
        v
    FALL CONFIRMED
        |
        |-- alerts.py      Email + SMS + snapshot saved locally
        |-- display.py     Skeleton overlay drawn on frame
        |-- dashboard/     Live stream to browser via WebSocket
        |-- logger.py      Event written to SQLite database
```

---

## Fall Detection Algorithm

```
torso_vec = shoulder_midpoint - hip_midpoint
angle     = arctan2(|torso_vec_x|, |torso_vec_y|)

Upright person   =  0 to 30 degrees
Bending/sitting  =  30 to 44 degrees
FALL confirmed   =  45+ degrees in 3 out of 5 frames
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Chandravadan30/SafeVision-AI.git
cd SafeVision-AI
```

### 2. Create virtual environment

```bash
python3 -m venv venv --system-site-packages
source venv/bin/activate
```

### 3. Install Jetson-specific PyTorch for JetPack 5.1

```bash
wget https://developer.download.nvidia.com/compute/redist/jp/v512/pytorch/torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
pip install torch-2.1.0a0+41361538.nv23.06-cp38-cp38-linux_aarch64.whl
```

### 4. Install dependencies

```bash
pip install ultralytics --no-deps
pip install flask flask-socketio opencv-python-headless
pip install sendgrid twilio pillow scipy tqdm
```

### 5. Configure credentials

```bash
nano config.py
```

Fill in your SendGrid API key and Twilio credentials in config.py.

### 6. Run the system

```bash
python main.py
```

Open http://jetson-ip:5000 in your browser.

---

## Performance

| Metric | Target | Achieved |
|--------|--------|----------|
| Fall confirmation speed | 15 frames | 3 to 5 frames |
| Alert latency | 2 seconds | 1.5 seconds |
| Inference resolution | 640x640 | 256x256 optimized |
| Privacy | 100% on-device | Zero data leaves device |
| System uptime | 99% | Stable via systemd |

---

## Dashboard

The web dashboard provides:

- **Live video feed** — real-time skeleton overlay streamed via WebSocket
- **Live metrics** — FPS, torso angle, detection status, persons in frame
- **Event log** — every fall with timestamp and exact angle recorded
- **Angle history chart** — torso angle over time with threshold line
- **Fall badge** — blinking red alert when fall is confirmed

---

## Future Work

- YOLOv8n object detection for hazard detection
- Behavioral fusion to classify events as Safe, Hazard, or Fall
- Multi-camera support across larger spaces
- TensorRT engine export for additional 2x GPU speedup
- Fine-tune on custom indoor fall dataset

---

## Author

**Venkata Sai Chandravadan Sobila** (HL12732)

DATA 690 — Final Project

NVIDIA Jetson Orin Nano, Edge AI, Computer Vision

## DEMO

**Dashboard**



<img width="588" height="475" alt="Screenshot 2026-05-19 at 17 17 46" src="https://github.com/user-attachments/assets/75698c98-e04d-468c-9ca9-3335e6f18dd1" />

https://github.com/user-attachments/assets/fe0badb4-a33e-4866-8451-ba7daa2e65f8


https://github.com/user-attachments/assets/c91d49cd-57c8-48a6-8ea7-9b2df73d3b35



**Email Alerts**

<img width="1512" height="982" alt="Screenshot 2026-05-19 at 20 07 34" src="https://github.com/user-attachments/assets/b869c970-3736-4f4b-81c5-a8e4e12688d4" />


<img width="1512" height="982" alt="Screenshot 2026-05-19 at 20 09 04" src="https://github.com/user-attachments/assets/78a387f9-7cca-4d6f-bae0-532871fde100" />


