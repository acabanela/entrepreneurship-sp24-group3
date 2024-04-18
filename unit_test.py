import unittest
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image, ImageSequence
from flask import Flask, render_template, request, redirect, url_for, Response, jsonify, current_app, session
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



def test_deepface_frame():
    frame = "picture/temp_frame.jpg"
    result = deepface_frame(frame)
    assert isinstance(result, dict)

def test_get_emoji():
    emotion = "happy"
    emoji_path = get_emoji(emotion)
    assert isinstance(emoji_path, str)

def test_draw_cursor():
    img = cv2.imread("picture/temp_frame.jpg")  # Provide a valid image path for testing
    x, y = 100, 100  # Provide valid coordinates for testing
    region = img  # Provide a valid region for testing (should match the shape of img)
    result = draw_cursor(img, x, y, region)
    assert isinstance(result, bool)