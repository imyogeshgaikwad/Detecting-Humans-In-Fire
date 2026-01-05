from ultralytics import YOLO
from pathlib import Path


class HumanTrainer:

    def __init__(self, model_path: str = "yolov8n.pt", conf_threshold: float = 0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect_human(self, image_path: str) -> bool:
  
        results = self.model.predict(
            image_path,
            classes=[0],              
            conf=self.conf_threshold,
            verbose=False
        )[0]

        return len(results.boxes) > 0

    def evaluate_dataset(self, dataset_path: str, expected_label: bool):

        dataset_path = Path(dataset_path)
        correct = 0
        total = 0

        for image in dataset_path.glob("*.png"):
            prediction = self.detect_human(str(image))
            is_correct = prediction == expected_label

            status = " CORRECT" if is_correct else "WRONG"
            detected = "HUMAN" if prediction else "NO HUMAN"

            print(f"{image.name:25} -> {detected:10} | {status}")

            correct += int(is_correct)
            total += 1

        accuracy = (correct / total) * 100 if total > 0 else 0
        print(f"\nDataset: {dataset_path.name}")
        print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})\n")


if __name__ == "__main__":
    detector = HumanTrainer(conf_threshold=0.5)

    detector.evaluate_dataset(
        dataset_path="datasets/train/humans",
        expected_label=True
    )

    detector.evaluate_dataset(
        dataset_path="datasets/train/nohumans",
        expected_label=False
    )
