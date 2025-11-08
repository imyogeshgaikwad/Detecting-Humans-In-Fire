# from flask import Flask
from flask import Flask, request, jsonify, render_template
from PIL import Image
import numpy as np

from tensorflow.keras.models import load_model
# Create the Flask app
app = Flask(__name__)
# Pages: signup login dashboard upload-picture
# Define a route
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

# Define a route
@app.route('/login')
def login():
    return "LOGGIN IN"


@app.route('/analyze', methods=['POST'])
def analyze_frame():
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    fire_result = detect_fire(img)
    human_result = detect_humans(img)

    alert = fire_result["has_fire"] and len(human_result.get("persons", [])) > 0

    return jsonify({
        "alert": alert,
        "fire_label": fire_result["label"],
        "human_detected": len(human_result.get("persons", [])) > 0
    })

# Load the trained fire model once at startup
model = load_model("model/fire_model.h5")

IMG_SIZE = (224, 224)

def preprocess_image(file):
    # Open uploaded file
    img = Image.open(file).convert("RGB")
    img = img.resize(IMG_SIZE)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route("/fire-model", methods=["POST"])
def model_test():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    img_array = preprocess_image(file)

    pred = model.predict(img_array)[0][0]
    result = {
        "fire_detected": bool(pred > 0.5),
        "confidence": float(pred*100)
    }

    return jsonify(result)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
