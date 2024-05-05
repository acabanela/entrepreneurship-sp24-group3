# Use the official Python image as the base image
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        pkg-config \
        libhdf5-dev \
        gcc \
        libgl1 \
        python3-opencv \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container at /app
COPY . /app

# Set DEEPFACE_HOME environment variable to the current working directory
# to avoid downloading the weights on image boot per feedback from Professor Schonfeld
ENV DEEPFACE_HOME=/app

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available .
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle inst
CMD exec gunicorn --bind :$PORT --workers 4 --threads 8 --timeout 0 app:app