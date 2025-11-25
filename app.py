from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from ultralytics import YOLO
import os


app = Flask(__name__)


FIRE_MODEL_PATH = "model/fire_model.h5"
IMG_SIZE = (224, 224)
FIRE_THRESHOLD = 0.90

fire_model = load_model(FIRE_MODEL_PATH)
human_model = YOLO('yolov8n.pt')  


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/detect', methods=["POST"])
def detect():
    """
    Combined endpoint for fire and human detection.
    Returns JSON with both detections.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    
    # Fire prediction
    img_array = preprocess_image(file)
    fire_pred = float(fire_model.predict(img_array)[0][0])
    fire_prob = 1 - fire_pred

    # Human prediction with YOLO
    file.seek(0)
    temp_path = "temp_upload.jpg"
    file.save(temp_path)
    
    results = human_model.predict(temp_path, classes=[0], conf=0.5, verbose=False)[0]
    has_human = len(results.boxes) > 0
    human_confidence = float(results.boxes[0].conf[0]) * 100 if has_human else 0.0
    
    os.remove(temp_path)

    result = {
        "fire_detected": fire_prob >= FIRE_THRESHOLD,
        "fire_confidence": round(fire_prob * 100, 2),
        "human_detected": has_human,
        "human_confidence": round(human_confidence, 2)
    }

    return jsonify(result)


@app.route('/fire-model', methods=["POST"])
def fire_model_route():
    """
    Endpoint for fire detection.
    Returns JSON: fire_detected (bool), confidence (%)
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_array = preprocess_image(file)

    pred = float(fire_model.predict(img_array)[0][0])
    fire_prob = 1 - pred

    result = {
        "fire_detected": fire_prob >= FIRE_THRESHOLD,
        "confidence": round(fire_prob * 100, 2)
    }

    return jsonify(result)


@app.route('/human-model', methods=["POST"])
def human_model_route():
    """
    Endpoint for Human detection using YOLO.
    Returns JSON: human_detected (bool), confidence (%)
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    
    # Save temporarily for YOLO
    temp_path = "temp_upload.jpg"
    file.save(temp_path)
    
    # Predict with YOLO
    results = human_model.predict(temp_path, classes=[0], conf=0.5, verbose=False)[0]
    has_human = len(results.boxes) > 0
    confidence = float(results.boxes[0].conf[0]) * 100 if has_human else 0.0
    
    # Cleanup
    os.remove(temp_path)

    result = {
        "human_detected": has_human,
        "confidence": round(confidence, 2)
    }

    return jsonify(result)



def preprocess_image(file, img_size=IMG_SIZE):
    """
    Open uploaded file, resize to model input size,
    preprocess with EfficientNet preprocessing, add batch dimension.
    """
    img = Image.open(file).convert("RGB")
    img = img.resize(img_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array



if __name__ == '__main__':
    app.run(debug=True)