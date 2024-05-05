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
    """
    Render the index.html template.

    Returns:
        HTML: The rendered index page.
    """
    return render_template('index.html')


@app.route('/about')
def about():
    """
    Render the about.html template.

    Returns:
        HTML: The rendered about page.
    """
    return render_template('about.html')


@app.route('/learning_center')
def learning_center():
    """
    Render the learning_center.html template.

    Returns:
        HTML: The rendered learning center page.
    """
    return render_template('learning_center.html')


@app.route('/webcam')
def webcam():
    """
    Render the webcam.html template.

    Returns:
        HTML: The rendered webcam page.
    """
    return render_template('webcam.html')


@app.route('/webcam_scenario')
def webcam_scenario():
    """
    Render the webcam_scenario.html template.

    Returns:
        HTML: The rendered webcam scenario page.
    """
    return render_template('webcam_scenario.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze the facial expression from the provided image data by running
    inference on the face detection and emotion classification models.

    Returns:
        JSON: The result of the facial expression analysis.
    """
    data = request.get_json()

    # Remove the "data:image/jpeg;base64," prefix
    imgData = data['imgData'].split(',')[1]
    imgBytes = base64.b64decode(imgData)
    img = Image.open(BytesIO(imgBytes))

    # Convert PIL Image to numpy array
    img_np = np.array(img)

    # Call the DeepFace analyze() method. This will run model inference on
    # the VGG-Face model for face detection, then it will run model inference
    # on a CNN model for facial expression emotion classification.
    result = DeepFace.analyze(img_np,
                              actions=['emotion'],
                              enforce_detection=False)

    return jsonify(result)


def image_to_base64(pil_image):
    """
    Convert a PIL Image to a base64-encoded string in JPEG format.

    Args:
        pil_image (PIL.Image): The PIL Image to be converted.

    Returns:
        str: The base64-encoded image string.
    """
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"


if __name__ == '__main__':
    app.run(debug=True)
