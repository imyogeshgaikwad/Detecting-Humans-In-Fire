from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
import io

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load models at startup
# -----------------------------
FIRE_MODEL_PATH = "model/fire_model.h5"
HUMAN_MODEL_PATH = "model/human_model.h5"
IMG_SIZE = (224, 224)  # must match training
FIRE_THRESHOLD = 0.90  # 90% confidence threshold for fire

fire_model = load_model(FIRE_MODEL_PATH)
human_model = load_model(HUMAN_MODEL_PATH)

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return "LOGGING IN"


@app.route('/detect', methods=["POST"])
def detect():
    """
    Combined endpoint for fire and human detection.
    Returns JSON with both detections.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    
    # Read file once into memory
    image_bytes = file.read()
    
    # Fire prediction
    fire_img_array = preprocess_image_from_bytes(image_bytes)
    fire_pred = float(fire_model.predict(fire_img_array, verbose=0)[0][0])
    fire_prob = 1 - fire_pred  # Fire model needs flipping

    # Human prediction - use same bytes
    human_img_array = preprocess_image_from_bytes(image_bytes)
    human_pred = float(human_model.predict(human_img_array, verbose=0)[0][0])
    human_prob = human_pred  # Human model does NOT need flipping

    result = {
        "fire_detected": fire_prob >= FIRE_THRESHOLD,  # Changed to 90% threshold
        "fire_confidence": round(fire_prob * 100, 2),
        "human_detected": human_prob > 0.5,
        "human_confidence": round(human_prob * 100, 2)
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
    image_bytes = file.read()
    img_array = preprocess_image_from_bytes(image_bytes)

    # Predict
    pred = float(fire_model.predict(img_array, verbose=0)[0][0])

    # Flip probability to match correct class (fire vs no-fire)
    fire_prob = 1 - pred

    result = {
        "fire_detected": fire_prob >= FIRE_THRESHOLD,  # 90% threshold
        "confidence": round(fire_prob * 100, 2)
    }

    return jsonify(result)


@app.route('/human-model', methods=["POST"])
def human_model_route():
    """
    Endpoint for Human detection.
    Returns JSON: human_detected (bool), confidence (%)
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    image_bytes = file.read()
    img_array = preprocess_image_from_bytes(image_bytes)

    # Predict
    pred = float(human_model.predict(img_array, verbose=0)[0][0])

    # DON'T flip - raw prediction is already the human probability
    human_prob = pred

    result = {
        "human_detected": human_prob > 0.5,
        "confidence": round(human_prob * 100, 2)
    }

    return jsonify(result)


# -----------------------------
# Helper function
# -----------------------------
def preprocess_image_from_bytes(image_bytes, img_size=IMG_SIZE):
    """
    Process image from bytes instead of file object.
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(img_size)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array


# -----------------------------
# Run server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)