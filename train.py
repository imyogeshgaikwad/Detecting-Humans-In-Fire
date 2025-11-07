import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

# Load training dataset
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "dataset/train",
    image_size=(180, 180),
    batch_size=32
)

# Load test dataset
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "dataset/test",
    image_size=(180, 180),
    batch_size=32
)

# Normalize images (0–1)
normalization_layer = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Build model
model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(180, 180, 3)),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(train_ds.class_names), activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Train model
history = model.fit(train_ds, validation_data=val_ds, epochs=10)

# Evaluate on test data
model.evaluate(val_ds)

# Save model
model.save("image_classifier_model.h5")

print("Training complete! Classes:", train_ds.class_names)
