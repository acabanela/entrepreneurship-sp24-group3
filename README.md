# Emotion Explorers: Webcam Emotion Detection and Analysis

This project aims to detect and analyze emotions in real-time using webcam feed, with the objective of assisting individuals with Neurodevelopmental Disorders (NDDs) such as Autism and ADHD in understanding facial expressions and corresponding emotions. The system leverages the DeepFace library for facial analysis with computer vision AI.

## Startup 3: Emotion Explorers
MSDS 603: Entrepreneurship in AI, Spring 2024

Professor Uri Schonfeld

Amadeo Cabanela, Ronel Solomon, Krit Poshakrishna, David Ramirez, Yi-Fang Tsai

## About this Github Repository
We used this Github Repository for centralized development of our webapp. Please refer to the code in the `main` branch which contains the latest state of our MVP deployed to google cloud run.
* `app.py` - Main Flask app logic; code follows PEP8 standards
* `Dockerfile` - configuration file for building image
* `requirements.txt` - dependencies to be installed as part of the image
* `static` folder - contains image assets and javascript files for accessing webcam
* `templates` folder - html files for web pages
* `unit_test.py` - python test file

The other branches contain work for other experimental features developed locally.

## Webapp Features

- Real-time Video Analysis/ Face Explorer: Utilize your webcam for live-streaming video analysis and immediate feedback on detected emotions/facial expressions.
- Learning Center: A description of all the emotions.
- Scenario Explorer: Train facial expressions in different social contexts by answering questions and making facial expressions based on emotion for each scenario.

## Technology

### Application Flow
<img width="458" alt="image" src="https://github.com/acabanela/entrepreneurship-sp24-group3/assets/138199384/d30a0203-21d3-4c96-ba28-f90ca146bbe4">

The flow of the application is as follows:
* Once a user visits the demo webpage, the webcam becomes accessible via the client-side browser using javascript. This reduces network latency as the user is viewing their facial expressions.
* The webcam feed is sent to the flask app which is running on google cloud run.
* The webcam frames are captured using OpenCV and are sent to a VGG-Face model to detect the face.
* The face data is then sent to a CNN for emotion classification.
* The weights for both models are stored on the server side (it was included as part of the image when building it in the google cloud image registry).
* Finally, the emotion prediction is sent back to the user’s browser.

### About the Models
Our application leverages the DeepFace library for facial analysis with computer vision.

**Face Detection Model:** The default trained model for face detection in the Deep Face library is based on the VGG-Face model. This was trained on the VGG-Face dataset, which consists of millions of facial images across thousands of identities. The VGG-Face model is known for its high accuracy in facial recognition and attribute detection tasks. This model is based on the *Deep Face Recognition* Paper from Parkhi et al. here: https://www.robots.ox.ac.uk/~vgg/publications/2015/Parkhi15/parkhi15.pdf

**Facial Expression Emotion Classification Model:** A CNN model is used for facial expression emotion classification. It was trained on the FER2013 dataset consisting of over 30K facial images labeled with seven different emotions: anger, disgust, fear, happiness, sadness, surprise, and neutral.

Link to Deepface Documentation: https://github.com/serengil/deepface

### Model Deployment
We leverage the benefits of containerization with docker which allows portability, speed, flexibility, and scalability. Our MVP is a Flask application that is built as an image using the specifications in a Dockerfile. The image was built in the Google Cloud Registry and deployed to the compute service Google Cloud Run. The model weights and Flask app are stored in the server. The webcam functionality is made available on the client-side web browser with Javascript.

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

### Running the live webapp
Here is the link to the live webapp:
https://emotion-explorers-web-service-bg44mx37ca-wn.a.run.app/

1. Recommended browswer: Google Chrome

1. **Note on cold start:** Google Cloud Run containers will be deleted after 10 minutes of idle time. Therefore, when you first visit the link, please give it 1 minute for GCP to allocate compute resources. There may be some network latency for the first minute after startup when detecting facial expression emotions.

1. Have fun with the app's features including the Face Explorer, Emotion Explorer, and Learning Center. Remember to visit the About page for more information about our mission and the team.

### Running the app locally
1. Run the Flask application:

```bash
python app.py
```

2. Access the web interface at `http://127.0.0.1:5000` in your browser.

3. Follow the on-screen instructions to start practicing facial expressions using the webcam to analyze emotions.

## Webapp links: 
Here are live links to the most recent versions of our application:

* Final MVP: https://emotion-explorers-web-service-bg44mx37ca-wn.a.run.app/

* App with Scenario-Based Training Added: https://face-app-scenario-web-service-bg44mx37ca-wn.a.run.app/
