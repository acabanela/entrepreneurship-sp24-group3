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

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    imgData = data['imgData'].split(',')[1]  # Remove the "data:image/jpeg;base64," prefix
    imgBytes = base64.b64decode(imgData)
    img = Image.open(BytesIO(imgBytes))

    img_np = np.array(img)  # Convert PIL Image to numpy array

    result = DeepFace.analyze(img_np, actions=['emotion'])
    # Check if result is a list
    # if isinstance(result, list):
    #     for r in result:
    #         dominant_emotion = r['dominant_emotion'][:]
    #         print('Dominant Emotion:', dominant_emotion)
    # else:
    #     dominant_emotion = result['dominant_emotion'][:]
    #     print('Dominant Emotion:', dominant_emotion)

    return jsonify(result)

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     imgFile = request.files['image']  # Retrieve the uploaded file
#     img = Image.open(imgFile)  # Open the image file using PIL
#     img = np.array(img)  # Convert the image to a numpy array

#     # Convert numpy array back to PIL Image object
#     img_pil = Image.fromarray(img)

#     # Convert PIL Image object to base64 string
#     img_base64 = image_to_base64(img_pil)

#     # Analyze the base64-encoded image data
#     result = DeepFace.analyze(img_path=img_base64, actions=['emotion'])

#     return jsonify(result)


# @app.route('/analyze', methods=['POST'])
# def analyze():
#     imgFile = request.files['image']  # Retrieve the uploaded file
#     img = Image.open(imgFile)  # Open the image file using PIL
#     img = np.array(img)  # Convert the image to a numpy array

#     # Convert numpy array back to PIL Image object
#     img_pil = Image.fromarray(img)

#     # Convert PIL Image object to base64 string
#     img_base64 = image_to_base64(img_pil)

#     # print("Base64 Image:", img_base64)  # Print the base64 image data

#     # Decode the base64 string
#     img_data = base64.b64decode(img_base64.split(",")[1])

#     # Save the decoded data as an image file
#     with open('decoded_image.png', 'wb') as f:
#         f.write(img_data)

#     # Analyze the image data
#     result = DeepFace.analyze(img_path=img_base64, actions=['emotion'])

#     return jsonify(result)

def image_to_base64(pil_image):
    # Convert PIL Image to base64 string (JPEG format)
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"


# def image_to_base64(pil_image):
#     # Convert PIL Image to base64 string
#     buffered = BytesIO()
#     pil_image.save(buffered, format="PNG")
#     img_str = base64.b64encode(buffered.getvalue()).decode()
#     return f"data:image/png;base64,{img_str}"

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     imgData = request.json['imgData']
#     # result = DeepFace.analyze(img_path=imgData, actions=['emotion'])
#     # result = DeepFace.analyze(img_path=imgData, actions=['emotion'], enforce_detection=False)
#     result = DeepFace.analyze(img_path=imgData, actions=['emotion'],
#                               enforce_detection=False,
#                               detector_backend="opencv",
#                               align=True,
#                               silent=False)
#     return jsonify(result)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=4999, debug=True)
    app.run(debug=True)
