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


def test_deepface_frame():
    frame = "picture/temp_frame.jpg"
    result = deepface_frame(frame)
    assert isinstance(result, dict)

def test_get_emoji():
    emotion = "happy"
    emoji_path = get_emoji(emotion)
    assert isinstance(emoji_path, str)
