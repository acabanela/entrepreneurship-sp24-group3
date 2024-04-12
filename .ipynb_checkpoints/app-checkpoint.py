import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_socketio import SocketIO
from PIL import Image
import os
import threading
import matplotlib.pyplot as plt
import concurrent.futures

app = Flask(__name__)

# Function to analyze facial attributes using DeepFace
def deepface_frame(frame):
    """
    Analyzes facial attributes in an image using DeepFace.

    This function analyzes the emotion in the provided image using the DeepFace library.
    It detects facial attributes such as emotion, using the OpenCV backend, and returns
    the analysis result.

    Args:
        frame (str): The path to the image file to be analyzed.

    Returns:
        dict: A dictionary containing the analysis result, including the detected emotions.
    """
    result = DeepFace.analyze(img_path=frame, actions=['emotion'],
                              enforce_detection=False,
                              detector_backend="opencv",
                              align=True,
                              silent=False)
    return result
    
# Dictionary mapping emotions to emoji images
emoji_dict = {
    "angry": "emojis/angry.png",
    "fear": "emojis/fear.png",
    "neutral": "emojis/nuetral.png",
    "sad": "emojis/sad.png",
    "disgust": "emojis/disgust.png",
    "happy": "emojis/happy.png",
    "surprise": "emojis/suprised.png"
}

# Function to generate frames from webcam feed
def get_emoji(emotion):
    return emoji_dict.get(emotion, "emojis/nuetral.png")
    
def generate_frames():
    """
    Generates frames from webcam feed with emotion analysis and overlay of emoji.

    This function continuously captures frames from the webcam feed, analyzes
    each frame for emotion using the DeepFace library, overlays an emoji image
    corresponding to the detected emotion onto the frame, and adds text indicating
    the detected emotion to the frame. The frames are encoded as JPEG images
    and yielded as a multipart response for streaming.

    Returns:
        generator: A generator yielding multipart JPEG frames.
    """
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        
        
        # Save frame as temporary image
        cv2.imwrite("picture/temp_frame.jpg", frame)

        # Analyze the frame using DeepFace for emotion detection
        with concurrent.futures.ThreadPoolExecutor() as executor:
            face_analysis = deepface_frame("picture/temp_frame.jpg")
            if face_analysis is not None:
                emotion = face_analysis[0]['dominant_emotion']
                # print(get_emoji(emotion))
                emoji_path = get_emoji(emotion)
                emoji = cv2.imread(emoji_path, -1)
            

                emoji = cv2.imread(emoji_path, -1)


            # Define the position to overlay the emoji
                if emoji is not None:
                    x_offset = 20
                    y_offset = 20

            # Position the emoji in the video?
                    y1, y2 = y_offset, y_offset + 160
                    x1, x2 = x_offset, x_offset + 160
                    alpha_s = emoji[:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s
                    for c in range(0, 3):
                        frame[y1:y2, x1:x2, c] = (alpha_s * emoji[:, :, c] +
                                           alpha_l * frame[y1:y2, x1:x2, c])
    
             # Add text indicating emotion to the frame
            cv2.putText(frame, f"Emotion: {emotion}", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 245, 238), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (42, 202), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
         # Encode the frame as JPEG and yield it   
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        
        
        

    # Release the webcam
    cap.release()



@app.route('/')
def index():
    """
    Renders the index.html template.
    
    This function is responsible for rendering the index.html template
    when the root URL is accessed.
    
    Returns:
        str: Rendered HTML template.
    """
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    """
    Streams video feed from webcam.
    
    This function generates frames from the webcam feed using the
    generate_frames() generator function and streams them as a multipart
    response with the 'multipart/x-mixed-replace' content type.
    
    Returns:
        Response: Multipart response containing video frames.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/picture', methods=['GET', 'POST'])
def picture():
    """
    Renders the webcam.html template or redirects to index page.
    
    This function renders the webcam.html template when accessed via
    GET request. If accessed via POST request, it redirects to the
    index page.
    
    Returns:
        str: Rendered HTML template or redirection to index page.
    """
    print("hello")
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('webcam.html')
# Route for analyzing uploaded images
@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes the emotion in an uploaded image.
    
    This function receives an image file uploaded via a POST request,
    saves it as 'temp_image.jpg', analyzes the emotion in the image using DeepFace,
    and renders the 'result.html' template with the image and the dominant emotion.
    
    Returns:
        str: Rendered HTML template with image and dominant emotion.
    """
    file = request.files['file']
    # Ensure "picture" directory exists
    if not os.path.exists("picture"):
        os.makedirs("picture")
    image = Image.open(file)
    image.save("picture/temp_image.jpg")

    if not os.path.exists("picture/temp_image.jpg"):
        return "File not Exist"

    face_analysis = DeepFace.analyze(img_path="picture/temp_image.jpg")
    emotion = face_analysis[0]['dominant_emotion']
    return render_template('result.html', image="temp_image.jpg", emotion=emotion)

if __name__ == '__main__':
    app.run(debug=True)

import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
from flask import Flask, render_template, request, redirect, url_for, Response
from flask_socketio import SocketIO
from PIL import Image
import os
import threading
import matplotlib.pyplot as plt
import concurrent.futures

app = Flask(__name__)

# Function to analyze facial attributes using DeepFace
def deepface_frame(frame):
    """
    Analyzes facial attributes in an image using DeepFace.

    This function analyzes the emotion in the provided image using the DeepFace library.
    It detects facial attributes such as emotion, using the OpenCV backend, and returns
    the analysis result.

    Args:
        frame (str): The path to the image file to be analyzed.

    Returns:
        dict: A dictionary containing the analysis result, including the detected emotions.
    """
    result = DeepFace.analyze(img_path=frame, actions=['emotion'],
                              enforce_detection=False,
                              detector_backend="opencv",
                              align=True,
                              silent=False)
    return result
    
# Dictionary mapping emotions to emoji images
emoji_dict = {
    "angry": "emojis/angry.png",
    "fear": "emojis/fear.png",
    "neutral": "emojis/nuetral.png",
    "sad": "emojis/sad.png",
    "disgust": "emojis/disgust.png",
    "happy": "emojis/happy.png",
    "surprise": "emojis/suprised.png"
}

# Function to generate frames from webcam feed
def get_emoji(emotion):
    return emoji_dict.get(emotion, "emojis/nuetral.png")
    
def generate_frames():
    """
    Generates frames from webcam feed with emotion analysis and overlay of emoji.

    This function continuously captures frames from the webcam feed, analyzes
    each frame for emotion using the DeepFace library, overlays an emoji image
    corresponding to the detected emotion onto the frame, and adds text indicating
    the detected emotion to the frame. The frames are encoded as JPEG images
    and yielded as a multipart response for streaming.

    Returns:
        generator: A generator yielding multipart JPEG frames.
    """
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        
        
        # Save frame as temporary image
        cv2.imwrite("picture/temp_frame.jpg", frame)

        # Analyze the frame using DeepFace for emotion detection
        with concurrent.futures.ThreadPoolExecutor() as executor:
            face_analysis = deepface_frame("picture/temp_frame.jpg")
            if face_analysis is not None:
                emotion = face_analysis[0]['dominant_emotion']
                # print(get_emoji(emotion))
                emoji_path = get_emoji(emotion)
                emoji = cv2.imread(emoji_path, -1)
            

                emoji = cv2.imread(emoji_path, -1)


            # Define the position to overlay the emoji
                if emoji is not None:
                    x_offset = 20
                    y_offset = 20

            # Position the emoji in the video?
                    y1, y2 = y_offset, y_offset + 160
                    x1, x2 = x_offset, x_offset + 160
                    alpha_s = emoji[:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s
                    for c in range(0, 3):
                        frame[y1:y2, x1:x2, c] = (alpha_s * emoji[:, :, c] +
                                           alpha_l * frame[y1:y2, x1:x2, c])
    
             # Add text indicating emotion to the frame
            cv2.putText(frame, f"Emotion: {emotion}", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 245, 238), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (42, 202), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
         # Encode the frame as JPEG and yield it   
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        
        
        

    # Release the webcam
    cap.release()



@app.route('/')
def index():
    """
    Renders the index.html template.
    
    This function is responsible for rendering the index.html template
    when the root URL is accessed.
    
    Returns:
        str: Rendered HTML template.
    """
    return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    """
    About Section
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about.html')

@app.route('/video_feed')
def video_feed():
    """
    Streams video feed from webcam.
    
    This function generates frames from the webcam feed using the
    generate_frames() generator function and streams them as a multipart
    response with the 'multipart/x-mixed-replace' content type.
    
    Returns:
        Response: Multipart response containing video frames.
    """
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/picture', methods=['GET', 'POST'])
def picture():
    """
    Renders the webcam.html template or redirects to index page.
    
    This function renders the webcam.html template when accessed via
    GET request. If accessed via POST request, it redirects to the
    index page.
    
    Returns:
        str: Rendered HTML template or redirection to index page.
    """
    print("hello")
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('webcam.html')
# Route for analyzing uploaded images
@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes the emotion in an uploaded image.
    
    This function receives an image file uploaded via a POST request,
    saves it as 'temp_image.jpg', analyzes the emotion in the image using DeepFace,
    and renders the 'result.html' template with the image and the dominant emotion.
    
    Returns:
        str: Rendered HTML template with image and dominant emotion.
    """
    file = request.files['file']
    # Ensure "picture" directory exists
    if not os.path.exists("picture"):
        os.makedirs("picture")
    image = Image.open(file)
    image.save("picture/temp_image.jpg")

    if not os.path.exists("picture/temp_image.jpg"):
        return "File not Exist"

    face_analysis = DeepFace.analyze(img_path="picture/temp_image.jpg")
    emotion = face_analysis[0]['dominant_emotion']
    return render_template('result.html', image="temp_image.jpg", emotion=emotion)

if __name__ == '__main__':
    app.run(debug=True)