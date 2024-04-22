# Entrepreneurship Spring 2024 Group3

# Webcam Emotion Detection and Analysis

This project aims to detect and analyze emotions in real-time using a static photo or webcam feed, with the objective of assisting children with Autism Spectrum Disorders in understanding facial expressions and corresponding emotions. Leveraging the DeepFace library for facial analysis, the system provides visualizations of detected emotions over time.

## Main Functions

- Static Photo Analysis: Upload a static photo to receive detected emotion/facial expression feedback.
- Real-time Video Analysis: Utilize your webcam for live streaming video analysis and immediate feedback on detected emotions/facial expressions.

## Features

- Real-time emotion detection using a webcam feed
- Overlay of emoji corresponding to detected emotions on video frames
- Analysis of detected emotions over time with visualizations
- Web interface for interacting with the application

## Dependencies

- Python 3.8
- OpenCV
- DeepFace
- Flask
- Flask-SocketIO
- PIL (Python Imaging Library)
- NumPy
- Pandas
- Matplotlib
- Plotly

## Installation

1. Clone the repository:

```bash
git clone git@github.com:acabanela/entrepreneurship-sp24-group3.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```bash
python app.py
```

2. Access the web interface at `http://127.0.0.1:5000` in your browser.

3. Follow the on-screen instructions to start uploading photos or the webcam feed and analyze emotions.

---
