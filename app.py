from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input

# -----------------------------
# Initialize Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Load model at startup
# -----------------------------
MODEL_PATH = "model/fire_model.h5"
IMG_SIZE = (224, 224)  # must match training
model = load_model(MODEL_PATH)

# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return "LOGGING IN"


@app.route('/fire-model', methods=["POST"])
def fire_model():
    """
    Endpoint for fire detection.
    Returns JSON: fire_detected (bool), confidence (%)
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_array = preprocess_image(file)

    # Predict
    pred = float(model.predict(img_array)[0][0])

    # Flip probability to match correct class (fire vs no-fire)
    fire_prob = 1 - pred

    result = {
        "fire_detected": fire_prob > 0.5,
        "confidence": round(fire_prob * 100, 2)
    }

    return jsonify(result)


# -----------------------------
# Helper function
# -----------------------------
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


# -----------------------------
# Run server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)
