import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


class FireModelTrainer:
    def __init__(self, base_dir="datasets", img_size=(224, 224),
                 batch_size=16, epochs=30, model_dir="model"):
        self.base_dir = base_dir
        self.train_dir = os.path.join(base_dir, "train")
        self.val_dir = os.path.join(base_dir, "train")
        self.img_size = img_size
        self.batch_size = batch_size
        self.epochs = epochs
        self.model_dir = model_dir

        # Ensure directories exist and have images
        self._validate_dataset()

        # Data generators
        self.train_generator, self.val_generator = self._create_generators()

        # Build model
        self.model = self._build_model()

        # Callbacks
        self.callbacks = [
            EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
            ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6)
        ]

    def _validate_dataset(self):
        for folder in [self.train_dir, self.val_dir]:
            for cls in ["fire", "nofire"]:
                path = os.path.join(folder, cls)
                if not os.path.exists(path) or len(os.listdir(path)) == 0:
                    raise ValueError(f"Dataset folder '{path}' is missing or empty!")

    def _create_generators(self):
        train_datagen = ImageDataGenerator(
            preprocessing_function=preprocess_input,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            brightness_range=(0.7, 1.3)
        )

        val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

        train_gen = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode="binary"
        )

        val_gen = val_datagen.flow_from_directory(
            self.val_dir,
            target_size=self.img_size,
            batch_size=self.batch_size,
            class_mode="binary"
        )

        return train_gen, val_gen

    def _build_model(self):
        base_model = EfficientNetB0(weights="imagenet", include_top=False,
                                    input_shape=(*self.img_size, 3))
        base_model.trainable = False

        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.5),
            layers.Dense(1, activation="sigmoid")
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(1e-4),
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )
        return model

    def train(self, fine_tune=False):
        print("🚀 Starting training...")
        history = self.model.fit(
            self.train_generator,
            epochs=self.epochs,
            validation_data=self.val_generator,
            callbacks=self.callbacks
        )

        if fine_tune:
            print("🔧 Starting fine-tuning...")
            # Unfreeze last 20 layers
            self.model.layers[0].trainable = True
            for layer in self.model.layers[0].layers[:-20]:
                layer.trainable = False

            self.model.compile(
                optimizer=tf.keras.optimizers.Adam(1e-5),
                loss="binary_crossentropy",
                metrics=["accuracy"]
            )

            history_ft = self.model.fit(
                self.train_generator,
                epochs=10,
                validation_data=self.val_generator,
                callbacks=self.callbacks
            )
            return history, history_ft

        return history, None

    def save_model(self, filename="fire_model.h5"):
        os.makedirs(self.model_dir, exist_ok=True)
        path = os.path.join(self.model_dir, filename)
        self.model.save(path)
        print(f"✅ Model saved at {path}")

    @staticmethod
    def preprocess_image_file(file, img_size=(224, 224)):
        """Preprocess a single image file for prediction."""
        img = Image.open(file).convert("RGB")
        img = img.resize(img_size)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array


if __name__ == "__main__":
    trainer = FireModelTrainer(
        base_dir="datasets",
        img_size=(224, 224),
        batch_size=16,
        epochs=30,
        model_dir="model"
    )
    trainer.train(fine_tune=True)
    trainer.save_model()
