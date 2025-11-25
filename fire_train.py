import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input

class FireTrainer:
    def __init__(self, train_dir="datasets/train", img_size=(224,224),
                 batch_size=16, epochs=30, model_dir="model", model_name="fire_model.h5"):
        self.train_dir = train_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_dir = model_dir
        self.model_name = model_name

        self.model = self._build_model()
        self.train_gen = self._create_generator()

    def _create_generator(self):
        datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=(0.7, 1.3)
        )
        generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode="binary",
            shuffle=True
        )
        return generator

    def _build_model(self):
        base_model = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(*self.img_size,3))
        base_model.trainable = False  # freeze base

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                      loss="binary_crossentropy",
                      metrics=["accuracy"])
        print("✅ Model built and compiled.")
        return model

    def train(self):
        print("🚀 Training started on all images (no validation)...")
        self.model.fit(
            self.train_gen,
            epochs=self.epochs
        )
        print("✅ Training finished.")

    def save(self):
        os.makedirs(self.model_dir, exist_ok=True)
        path = os.path.join(self.model_dir, self.model_name)
        self.model.save(path)
        print(f"💾 Model saved at: {path}")



if __name__ == "__main__":
    trainer = FireTrainer(
        train_dir="datasets/train", 
        img_size=(224,224),
        batch_size=16,
        epochs=30
    )
    trainer.train()
    trainer.save()
