import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image, ImageSequence
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify, current_app, session, send_file
from flask_socketio import SocketIO
from PIL import Image
import os
import threading
import matplotlib.pyplot as plt
import concurrent.futures
import pandas as pd
import datetime
import time
import pyautogui
import tkinter as tk
import webbrowser
import plotly.graph_objs as go


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


def get_emoji(emotion):
    """
    Get the path to the emoji image corresponding to the given emotion.

    Args:
        emotion (str): The emotion for which to retrieve the emoji path.

    Returns:
        str: The path to the emoji image.
    """
    return emoji_dict.get(emotion, "emojis/neutral.png")

def draw_cursor(img, x, y, region):
    """
    Draw a cursor on the image and check if it's near the target position.

    Args:
        img (numpy.ndarray): The image on which to draw the cursor.
        x (int): The x-coordinate of the target position.
        y (int): The y-coordinate of the target position.
        region (numpy.ndarray): The region of interest for overlaying the exit icon.

    Returns:
        bool: True if the cursor is not near the target position, False otherwise.
    """
    xs, ys = pyautogui.position()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (255, 255, 255)

    if x <= xs <= x + region.shape[1] and y <= ys <= y + region.shape[0]:
        cv2.putText(img, "Done", (1580, 260), font, font_scale, text_color, font_thickness)
        cv2.putText(img, "Done", (1580, 260), font, font_scale, (0, 0, 0), font_thickness)
        return False


def generate_frames(name="asset"):
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
    exit = cv2.imread("emojis/exit.png", -1)

    cap = cv2.VideoCapture(0)

    time_list = []
    emotion_list = []
    while True:
        # Capture frame-by-frame
        try:
            ret, frame = cap.read()
            time_list.append(datetime.datetime.now())
            if not ret:
                break

            # Save frame as temporary image
            cv2.imwrite("static/picture/temp_frame.jpg", frame)

            # Analyze the frame using DeepFace for emotion detection
            with concurrent.futures.ThreadPoolExecutor() as executor:
                face_analysis = deepface_frame("static/picture/temp_frame.jpg")
                if face_analysis is not None:
                    emotion = face_analysis[0]['dominant_emotion']
                    emotion_list.append(emotion)
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

                        x_offset_exit = frame.shape[1] - exit.shape[1] - 20  # 20 pixels from the right edge
                        y_offset_exit = 20  # 20 pixels from the top edge
                        print(exit.shape[1], exit.shape[0]),

                        # Define the region of interest for overlaying the exit icon
                        exit_roi = frame[y_offset_exit:y_offset_exit + exit.shape[0], x_offset_exit:x_offset_exit + exit.shape[1]]

                        leave = draw_cursor(frame, x_offset_exit, y_offset_exit, exit_roi)

                        cv2.putText(frame, "Exit", (x_offset_exit + 200, y_offset_exit + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                        if leave == False:
                            with app.app_context():
                                df = pd.DataFrame({'Time': time_list, 'Emotion': emotion_list})
                                df.to_csv(f'{name}_emotion_data.csv', index=False)
                                print("Done", app.redirect("/"))
                                cap.release()
                                return webbrowser.open("http://127.0.0.1:5000")

            # Add text indicating emotion to the frame
            cv2.putText(frame, f"Emotion: {emotion}", (40, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 245, 238), 2)
            cv2.putText(frame, f"Emotion: {emotion}", (42, 202), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

            # Encode the frame as JPEG and yield it
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        except Exception as e:
            # If an error occurs, release the webcam and return to index page
            print(f"An error occurred: {e}")

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
    with app.app_context():
        return render_template('index.html')


@app.route('/take-screenshot', methods=['POST'])
def take_screenshot():
    # Capture a screenshot and save it as a JPEG file
    camera = cv2.VideoCapture(0)
    
    time.sleep(3)
    # Capture a picture
    ret, frame = camera.read()
    
    # Release the camera
    camera.release()
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    cv2.imwrite('sreenshot_pict.jpg', frame)
    
    # Return the captured picture as a response
    return send_file('sreenshot_pict.jpg', mimetype='image/jpeg')


@app.route('/about', methods=['GET', 'POST'])
def about():
    """
    About Section.
    """
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('about.html')


@app.route('/video', methods=['GET', 'POST'])
def video():
    """
    Streams video feed from webcam.
    
    This function generates frames from the webcam feed using the
    generate_frames() generator function and streams them as a multipart
    response with the 'multipart/x-mixed-replace' content type.
    
    Returns:
        Response: Multipart response containing video frames.
    """
    name = request.form['username']
    print(name)
    # Call generate_frames function with name parameter
    return Response(generate_frames(name), mimetype='multipart/x-mixed-replace; boundary=frame')
    
@app.route('/video_feed')       
def video_feed():
    """
    Return a login template for video_feed.
    
    Returns:
        Response: template for login.
    """
    return render_template('login.html')


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

emotion_descriptions = {
    "happy": "Feeling joyous and content. Happiness is a positive emotion that arises from experiencing pleasure, satisfaction, or success. It can be expressed through smiling, laughter, and a generally upbeat demeanor. Happiness contributes to overall well-being and can be contagious, spreading positivity to those around us.",
    "sad": "Feeling sorrowful or unhappy. Sadness is a natural human emotion often triggered by loss, disappointment, or failure. It's characterized by feelings of grief, loneliness, or despair. While sadness can be uncomfortable, it's important to acknowledge and express these emotions, as doing so can lead to healing and emotional growth.",
    "angry": "Feeling intense displeasure or hostility. Anger is a powerful emotion that arises in response to perceived threats, injustices, or frustrations. It's often accompanied by physical sensations like increased heart rate and muscle tension. While anger itself is not inherently negative, it's important to manage it constructively to avoid harmful behaviors and maintain healthy relationships.",
    "fear": "Feeling scared or anxious. Fear is an adaptive response to perceived danger or threat. It triggers a fight, flight, or freeze reaction in the body, preparing us to respond to potential harm. While fear can be protective, excessive or irrational fear can interfere with daily life. Overcoming fear often involves facing it gradually and developing coping strategies to manage anxiety.",
    "surprise": "Feeling astonished or amazed. Surprise is a brief, intense emotion that occurs in response to unexpected events or stimuli. It's characterized by a sudden shift in attention and physiological arousal. Surprise can be positive or negative depending on the context, but it adds excitement and novelty to our experiences.",
    "neutral": "Showing no particular emotion. Neutrality is a state of emotional calmness and balance where no strong feelings or reactions are present. It can be a temporary state or a habitual response to certain situations. While neutrality may seem unremarkable, it can serve as a valuable buffer against stress and overwhelm.",
    "disgust": "Feeling revulsion or strong disapproval. Disgust is an aversive emotion triggered by offensive or repulsive stimuli, such as foul odors, unsanitary conditions, or morally objectionable behavior. It serves as a protective mechanism to avoid potentially harmful substances or situations. While disgust may be unpleasant, it plays an important role in maintaining hygiene and social norms."
    }


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
    if (request.files['file']):
        file = request.files['file']
    # Ensure "picture" directory exists
        if not os.path.exists("picture"):
            os.makedirs("picture")
        image = Image.open(file)
        # image = image.resize((800, 600))
        image.save("static/picture/temp_image.jpg")

        if not os.path.exists("static/picture/temp_image.jpg"):
            return "File not Exist"
    
        face_analysis = DeepFace.analyze(img_path="static/picture/temp_image.jpg")
        img = "static/picture/temp_image.jpg"
    else:
        image = Image.open("sreenshot_pict.jpg")
        image.save("static/picture/temp_image.jpg")
        face_analysis = DeepFace.analyze(img_path="sreenshot_pict.jpg")
        img = "static/picture/temp_image.jpg"
    emotion = face_analysis[0]['dominant_emotion']

    expected_emotion = request.form.get('expected_emotion')
        
    emoji_urls = {
        "happy": "https://giphy.com/embed/chzz1FQgqhytWRWbp3",
        "sad": "https://giphy.com/embed/QJY9tY29IQGMU",
        "angry": "https://giphy.com/embed/11tTNkNy1SdXGg",
        "fear": "https://giphy.com/embed/PaG51G9OKKdKU",
        "disgust": "https://giphy.com/embed/rP6BL1bifRBBK",
        "neutral": "https://giphy.com/embed/1gQwMNJ9z1mqABgQd3",
        # Add URLs for other emotions here
    }
    emoji_url = emoji_urls.get(emotion, "https://example.com/default_emoji.gif")
    emotion_description = emotion_descriptions.get(emotion, "No description available.")
    return render_template('result.html',
                           image=img,
                           emotion=emotion,
                           description=emotion_description,
                           emoji_url=emoji_url)


@app.route('/username') 
def username():
    """
    Return a login template for username.
    
    Returns:
        Response: template for login.
    """
    return render_template('username.html')


@app.route('/emotion', methods=['GET', 'POST'])    
def emotion():
    """
    This function processes emotion data obtained from a CSV file and generates visualizations.
    It reads the CSV file based on the username provided in the form, groups the data by emotion,
    and creates bar charts and time series graphs to visualize the occurrence of each emotion over time.
    
    Returns:
        str: Rendered HTML template containing the visualizations and emotion descriptions.
    """
    # Read the CSV file
    name = request.form['username']
    print(name)
    df = pd.read_csv(f"{name}_emotion_data.csv")
    
    # Group by the 'emotion' column and get the size of each group
    groupby = df.groupby("Emotion")
    size = groupby.size()
    
    bar_data = [
        go.Bar(
            x=size.index,
            y=size.values,
            marker=dict(color='rgb(158,202,225)', line=dict(color='rgb(8,48,107)', width=1.5))
        )
    ]
    

    bar_layout = go.Layout(
        title='The most occurrence of each Emotion',
        xaxis=dict(title='Emotion'),
        yaxis=dict(title='Counts')
    )

    bar_fig = go.Figure(data=bar_data, layout=bar_layout)
    bar_plot_div = bar_fig.to_html(full_html=False)
    
    # Second Plot: Time Series Graph for Emotion Over Time
    df['Time'] = pd.to_datetime(df['Time'])

    grouped_df = df.groupby(['Emotion', pd.Grouper(key='Time', freq='S')]).size().reset_index(name='Count')

    # Create traces for each emotion
    time_series_traces = []
    for emotion in grouped_df['Emotion'].unique():
        emotion_data = grouped_df[grouped_df['Emotion'] == emotion]
        trace = go.Scatter(
        x=emotion_data['Time'],
        y=emotion_data['Count'],
        mode='lines+markers',
        name=emotion
        )
        time_series_traces.append(trace)

    # Create layout
    time_series_layout = go.Layout(
    title='Emotion Over Time',
    xaxis=dict(title='Time'),
    yaxis=dict(title='Count')
    )

    # Create the time series graph figure
    time_series_fig = go.Figure(data=time_series_traces, layout=time_series_layout)
    time_series_plot_div = time_series_fig.to_html(full_html=False)
    
    
    
    # Get the top 2 emotions
    top_2_emotions = size.nlargest(2)
    
    # Get the names of the top 2 emotions
    top_2_emotion_names = top_2_emotions.index.tolist()
    
    # Define descriptions for each emotion
    emotion_descriptions = {
        "happy": "Patient is is feeling joy satisfication. Keep on going. \n Celebrate with them by sharing in their excitement.",
        "sad": "Patient is feeling sorrowful or unhappy. \n Listen to them attentively and empathize with their feelings.",
        "fear": "Patient feeling stressed out. Need to take a break! \n Reassure them that it's okay to feel afraid and that they are not alone.",
        "disgust": "Feeling a strong aversion or repugnance.  \n Listen to their concerns without judgment.",
        "neutral": "Feeling Normal. Keep on going going. You got it! Be \n attentive and observant, as they may be concealing their true feelings.",
        "angry": "Very upset. Need some cooldown. Give them so tea or ice cream!"
    }

    
    # Assign descriptions based on the top 2 emotions
    descriptions = {}
    for emotion in top_2_emotion_names:
        if emotion in emotion_descriptions:
            descriptions[emotion] = emotion_descriptions[emotion]
        else:
            descriptions[emotion] = "No description available."
    
    return render_template('emotion.html', bar_plot_div=bar_plot_div, time_series_plot_div=time_series_plot_div, descriptions=descriptions)


if __name__ == '__main__':
    app.run(debug=True, threaded=False)