"""Usage of Google Vision API for food classification."""

import logging
from typing import Optional

from google.cloud import vision

from app.constants import VALID_ITEMS

log = logging.getLogger("vision")


def get_food_classification(input: bytes) -> Optional[str]:
    """
    Classify input image using Google Vision API.
    Args:
        input (bytes): Input image for classification.
    Returns:
        Optional[str]: Filtered food classification.
    """

    # call Google Vision API with input image
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=input)
    response = client.label_detection(image=image, max_results=20)

    # get the labels from response
    labels = response.label_annotations

    # return first valid label from possible labels based on items in scope
    for label in labels:
        if label.description in VALID_ITEMS:
            log.info(
                f"[Vision API] Item: {label.description} - Score: {round(label.score, 2)}"
            )
            return label.description

    return None
