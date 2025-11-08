import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
import os

# Dataset path
base_dir = "datasets"

train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")

# In case you only have /fire images for now, we’ll reuse them
# and later you can add /nofire for better classification
if not os.path.exists(val_dir):
    os.makedirs(val_dir, exist_ok=True)
    os.system(f"cp -r {train_dir}/fire {val_dir}/fire")

# Parameters
IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10

# Preprocessing and augmentation
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,   # Split training data internally if needed
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    base_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    base_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)

# Model definition (simple CNN)
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(224, 224, 3)),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(128, activation="relu"),
    layers.Dropout(0.5),
    layers.Dense(1, activation="sigmoid")  # Binary output
])

model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])

# Train
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator
)

# Save model
os.makedirs("model", exist_ok=True)
model.save("model/fire_model.h5")

print("✅ Model training complete! Saved as model/fire_model.h5")
