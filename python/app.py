import os
import cv2
import numpy as np
from collections import Counter
import pytesseract
from PIL import Image
import torch
from flask import Flask, render_template, Response
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("Environment variables loaded")

class VideoCamera(object):
    def __init__(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.video = cv2.VideoCapture(self.rtsp_url)
        self.fgbg = cv2.createBackgroundSubtractorMOG2()  # Background subtractor
        self.descriptor = VideoDescriptionGenerator()  # Background subtractor

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        if success:
            description = self.generate_description(frame)
            print(description)
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes(), description
        else:
            return None, None

    def generate_description3(self, frame):
        description = self.descriptor.generate_description(frame)
        return description

    def generate_description(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = self.fgbg.apply(gray)

        # Tune these parameters for better detection
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_areas = [cv2.contourArea(contour) for contour in contours]

        if contour_areas and max(contour_areas) > 500:
            # Estimate object size based on contour area
            max_area = max(contour_areas)
            object_size = "small"
            if max_area > 5000:
                object_size = "medium"
            if max_area > 10000:
                object_size = "large"

            description = self.descriptor.generate_description(frame)
            return f"A {object_size} object is moving. {description}"

        return "."

    def generate_description2(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = self.fgbg.apply(gray)

        # Tune these parameters for better detection
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if cv2.contourArea(contour) < 500:  # Ignore small movements
                continue
            return "Video showing movement detected."

        # return "Video showing no significant movement."
        return "."


class RTSPStream:
    def __init__(self, rtsp_url, host='0.0.0.0', port=5000):
        self.rtsp_url = rtsp_url
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.camera = VideoCamera(self.rtsp_url)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        def gen(camera):
            while True:
                frame, description = camera.get_frame()
                if len(description):
                    print(description)  # Print description for debugging

                if frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        @self.app.route('/video_feed')
        def video_feed():
            return Response(gen(self.camera),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    def start(self):
        print(f"Starting Flask app on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=True)



class VideoDescriptionGenerator:
    def __init__(self):
        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        # Load YOLOv7 model
        try:
            print("Loading YOLOv7 model...")
            self.model = torch.hub.load('WongKinYiu/yolov7', 'yolov7', pretrained=True)
            print("YOLOv7 model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
        if self.model:
            self.model.conf = 0.25  # Confidence threshold
        # Set up OCR
        pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Update this path as needed

    def generate_description(self, frame):
        description = []

        if self.model:
            # Object detection
            results = self.model(frame)
            detections = results.pred[0]

            for *box, conf, cls in detections:
                x1, y1, x2, y2 = map(int, box)
                obj_name = self.model.names[int(cls)]
                description.append(f"{obj_name} detected with confidence {conf:.2f}")

                # Draw bounding box on frame (optional)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"{obj_name} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return ". ".join(description) + "."

    def detect_objects(self, frame):
        if self.model:
            results = self.model(frame)  # Perform inference
            detections = results.pred[0]  # Get predictions

            for *box, conf, cls in detections:
                # Draw bounding boxes or take other actions based on detections
                x1, y1, x2, y2 = map(int, box)
                label = f"{self.model.names[int(cls)]} {conf:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return frame

    def detect_text(self, frame):
        # Convert the frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform OCR
        text = pytesseract.image_to_string(pil_image)

        # Clean up the text
        text = ' '.join(text.split())
        return text if text else None

    def get_dominant_color(self, frame):
        pixels = frame.reshape(-1, 3)
        counts = Counter(map(tuple, pixels))
        most_common = counts.most_common(1)[0][0]
        return self.color_name(most_common)

    def color_name(self, rgb):
        r, g, b = rgb
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > max(g, b):
            return "red"
        elif g > max(r, b):
            return "green"
        elif b > max(r, g):
            return "blue"
        else:
            return "mixed"

    def get_brightness(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv)
        avg_brightness = np.mean(v)
        if avg_brightness < 50:
            return "dark"
        elif avg_brightness > 200:
            return "bright"
        else:
            return "moderately lit"


if __name__ == "__main__":
    try:
        # Accessing variables with default values
        rtsp_url = os.getenv("RTSP_URL", "rtsp://example.com/stream")
        app_port = int(os.getenv("APP_PORT", "5000"))

        print(f"RTSP URL: {rtsp_url}")
        print(f"App Port: {app_port}")

        stream = RTSPStream(rtsp_url, port=app_port)
        stream.start()
    except Exception as e:
        print(f"An error occurred: {e}")
