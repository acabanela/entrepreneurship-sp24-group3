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
    result = DeepFace.analyze(img_path=frame, actions=['emotion'],
                              enforce_detection=False,
                              detector_backend="opencv",
                              align=True,
                              silent=False)
    return result

emoji_dict = {
    "angry": "emojis/angry.png",
    "fear": "emojis/fear.png",
    "neutral": "emojis/nuetral.png",
    "sad": "emojis/sad.png",
    "disgust": "emojis/disgust.png",
    "happy": "emojis/happy.png",
    "surprise": "emojis/suprised.png"
}

def get_emoji(emotion):
    return emoji_dict.get(emotion, "emojis/nuetral.png")
    
def generate_frames():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        
        
        # Save frame as temporary image
        cv2.imwrite("temp_frame.jpg", frame)

        # Analyze the frame using DeepFace
        with concurrent.futures.ThreadPoolExecutor() as executor:
            face_analysis = deepface_frame("temp_frame.jpg")
            emotion = face_analysis[0]['dominant_emotion']
            print(get_emoji(emotion))
            #cv2.putText(frame, f"Emotion: {get_emoji(emotion)}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 2)
            emoji_path = get_emoji(emotion)
            emoji = cv2.imread(emoji_path, -1)
            
            # Resize emoji to fit the frame
            #emoji = cv2.resize(emoji, (100, 100))
            
            # Overlay emoji onto the frame
            #if emoji_path:
            # Load the emoji image
            emoji = cv2.imread(emoji_path, -1)

            # Resize emoji to fit the frame
            #emoji = cv2.resize(emoji, (100, 100))

            # Define the position to overlay the emoji
            if emoji is not None:
                x_offset = 20
                y_offset = 20

            # Extract the alpha channel from the emoji
                y1, y2 = y_offset, y_offset + 160
                x1, x2 = x_offset, x_offset + 160
                alpha_s = emoji[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                for c in range(0, 3):
                    frame[y1:y2, x1:x2, c] = (alpha_s * emoji[:, :, c] +
                                           alpha_l * frame[y1:y2, x1:x2, c])

            cv2.putText(frame, f"Emotion: {emotion}", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 245, 238), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (42, 202), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        
            
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        
        
        

    # Release the webcam
    cap.release()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('webcam.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    image = Image.open(file)
    image.save("temp_image.jpg")

    if not os.path.exists("temp_image.jpg"):
        return "File not Exist"

    face_analysis = DeepFace.analyze(img_path="temp_image.jpg")
    emotion = face_analysis[0]['dominant_emotion']
    return render_template('result.html', image="temp_image.jpg", emotion=emotion)

if __name__ == '__main__':
    app.run(debug=True)


