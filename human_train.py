from ultralytics import YOLO

class SimpleHumanDetector:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
    
    def has_human(self, image_path):
        """Returns True if human detected, False otherwise"""
        results = self.model.predict(image_path, classes=[0], conf=0.5, verbose=False)[0]
        return len(results.boxes) > 0


# Usage
if __name__ == "__main__":
    detector = SimpleHumanDetector()
    
    # Single image check
    result = detector.has_human("datasets/train/humans/image1.jpg")
    print(f"Has human: {result}")  # True or False
    
    # Check multiple images
    import os
    from pathlib import Path
    
    test_folder = "datasets/train/humans"
    if os.path.exists(test_folder):
        for img in Path(test_folder).glob("*.jpg"):
            has_human = detector.has_human(str(img))
            print(f"{img.name}: {'✅ HUMAN' if has_human else '❌ NO HUMAN'}")