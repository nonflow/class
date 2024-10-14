# Use an official Python runtime as a parent image
ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip and install required python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
ARG APP_PORT
EXPOSE ${APP_PORT}

# Set environment variable for Tesseract OCR path
ARG TESSERACT_PATH
ENV TESSERACT_CMD=${TESSERACT_PATH}

# Run app.py when the container launches
CMD ["python", "app.py"]