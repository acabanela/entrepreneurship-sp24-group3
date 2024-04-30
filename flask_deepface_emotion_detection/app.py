from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import base64
from io import BytesIO
from deepface import DeepFace

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    """
    About Section.
    """
    return render_template('about.html')

@app.route('/learning_center')
def learning_center():
    """
    Learning Center Page
    """
    return render_template('learning_center.html')

@app.route('/webcam')
def webcam():
    """
    Webcam page for real-time emotion detection from facial epxressions.
    """
    return render_template('webcam.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    imgData = data['imgData'].split(',')[1]  # Remove the "data:image/jpeg;base64," prefix
    imgBytes = base64.b64decode(imgData)
    img = Image.open(BytesIO(imgBytes))

    img_np = np.array(img)  # Convert PIL Image to numpy array

    result = DeepFace.analyze(img_np, actions=['emotion'])

    return jsonify(result)


def image_to_base64(pil_image):
    # Convert PIL Image to base64 string (JPEG format)
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"


if __name__ == '__main__':
    app.run(debug=True)
