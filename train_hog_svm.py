import os
import cv2
import joblib
import numpy as np
from skimage.feature import hog
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# ---- CONFIG ----
DATASET_DIR = "datasets/fire"   # change to datasets/humans for human model
MODEL_PATH = "models/fire_model.pkl"

# HOG parameters
HOG_PARAMS = dict(
    orientations=9,
    pixels_per_cell=(8, 8),
    cells_per_block=(2, 2),
    block_norm='L2-Hys'
)

IMG_SIZE = (128, 128)

def load_images(root_dir):
    data, labels = [], []
    for label_name in os.listdir(root_dir):
        folder = os.path.join(root_dir, label_name)
        if not os.path.isdir(folder):
            continue
        for img_name in tqdm(os.listdir(folder), desc=f"Loading {label_name}"):
            path = os.path.join(folder, img_name)
            try:
                img = cv2.imread(path)
                if img is None: continue
                img = cv2.resize(img, IMG_SIZE)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                feat = hog(gray, **HOG_PARAMS)
                data.append(feat)
                labels.append(label_name)
            except Exception as e:
                print("Error:", e)
    return np.array(data), np.array(labels)

def main():
    print("[INFO] Loading data...")
    X, y = load_images(DATASET_DIR)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"[INFO] Training samples: {len(X_train)}, Testing: {len(X_test)}")

    print("[INFO] Training SVM...")
    model = LinearSVC(max_iter=5000)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"[RESULT] Test Accuracy: {acc*100:.2f}%")
    print("Confusion Matrix:\n", confusion_matrix(y_test, preds))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"[SAVED] Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    main()
