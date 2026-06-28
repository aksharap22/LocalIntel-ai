import cv2
import numpy as np
from app.services.ocr import preprocess_image


def test_preprocess_image(tmp_path):
    image = np.full((64, 128, 3), 255, dtype=np.uint8)
    cv2.putText(image, "AI", (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    path = tmp_path / "scan.png"
    cv2.imwrite(str(path), image)
    processed = preprocess_image(path)
    assert processed.shape == (64, 128)
