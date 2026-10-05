import cv2
import numpy as np
import pytesseract


def extract_text(image_bytes):

    # Convert bytes into NumPy array
    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    # Read image
    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return ""

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Reduce noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Thresholding
    processed = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # OCR
    text = pytesseract.image_to_string(
        processed
    )

    return text.strip()