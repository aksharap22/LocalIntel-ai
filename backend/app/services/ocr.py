from pathlib import Path

import cv2
import numpy as np

from app.services.parser import clean_text


def preprocess_image(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError("Unable to read image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    return cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def extract_image_text(path: Path) -> str:
    _ = preprocess_image(path)
    try:
        from paddleocr import PaddleOCR  # type: ignore[import-untyped]

        ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False, show_log=False)
        result = ocr.ocr(str(path), cls=True)
        lines = [line[1][0] for page in result for line in page]
        return clean_text("\n".join(lines))
    except Exception as exc:
        return clean_text(
            f"OCR unavailable locally for {path.name}. " f"Install PaddleOCR models. {exc}"
        )
