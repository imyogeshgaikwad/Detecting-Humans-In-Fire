import cv2
import joblib
import numpy as np
from skimage.feature import hog

MODEL_PATH = "models/fire_model.pkl"

HOG_PARAMS = dict(
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    block_norm='L2-Hys'
)
IMG_SIZE = (128, 128)

model = joblib.load(MODEL_PATH)

def detect_fire(img):
    img = cv2.resize(img, IMG_SIZE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = hog(gray, **HOG_PARAMS).reshape(1, -1)
    prediction = model.predict(features)[0]
    return {
        "has_fire": prediction == "fire",
        "label": prediction,
        "confidence": 1.0  
    }
