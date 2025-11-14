import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

class HumanTrainer:
    def __init__(self, train_dir="datasets/train",
                 img_size=(224,224),
                 batch_size=32,
                 epochs=50,
                 model_dir="model",
                 model_name="human_model.h5"):
        """
        Trainer for binary classification: humans vs nohumans
        """
        self.train_dir = train_dir
        self.img_size = img_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_dir = model_dir
        self.model_name = model_name

        self.model = self._build_model()
        self.train_gen = self._create_generator()

    def _create_generator(self):
        # Less aggressive augmentation for human detection
        datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=15,
            width_shift_range=0.15,
            height_shift_range=0.15,
            shear_range=0.1,
            zoom_range=0.15,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode="binary",
            shuffle=True
        )
        print(f"🧍 Dataset loaded from: {self.train_dir}")
        print(f"Classes found: {generator.class_indices}")
        print(f"Total samples: {generator.samples}")
        return generator

    def _build_model(self):
        # MobileNetV2 is often better for human detection
        base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(*self.img_size,3))
        
        # Unfreeze last 30 layers for fine-tuning
        for layer in base_model.layers[:-30]:
            layer.trainable = False
        for layer in base_model.layers[-30:]:
            layer.trainable = True

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.BatchNormalization(),
            layers.Dense(512, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.3),
            layers.Dense(1, activation="sigmoid")
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss="binary_crossentropy",
            metrics=["accuracy", tf.keras.metrics.Precision(), tf.keras.metrics.Recall()]
        )
        print("✅ Model built and compiled (MobileNetV2 backbone with fine-tuning).")
        return model

    def train(self):
        print("🚀 Training started (humans vs nohumans)...")
        
        # Callbacks for better training
        callbacks = [
            ReduceLROnPlateau(monitor='loss', factor=0.5, patience=3, min_lr=1e-7, verbose=1),
            EarlyStopping(monitor='loss', patience=8, restore_best_weights=True, verbose=1)
        ]
        
        self.model.fit(
            self.train_gen,
            epochs=self.epochs,
            callbacks=callbacks
        )
        print("✅ Training finished successfully.")

    def save(self):
        os.makedirs(self.model_dir, exist_ok=True)
        path = os.path.join(self.model_dir, self.model_name)
        self.model.save(path)
        print(f"💾 Model saved at: {path}")


# -----------------------------
# Usage Example
# -----------------------------
if __name__ == "__main__":
    trainer = HumanTrainer(
        train_dir="datasets/train",
        img_size=(224,224),
        batch_size=32,
        epochs=50
    )
    trainer.train()
    trainer.save()