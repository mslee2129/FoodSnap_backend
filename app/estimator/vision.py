"""Usage of Google Vision API for food classification."""

import logging
from pathlib import Path
from typing import Optional

from google.cloud import vision

from app.estimator.constants import VALID_ITEMS
from app.util import load_image

log = logging.getLogger("vision")


def get_food_classification(path: Path) -> Optional[str]:
    """
    Classify input image using Google Vision API.
    Args:
        path (Path): Path to input image for classification.
    Returns:
        Optional[str]: Filtered food classification.
    """

    # call Google Vision API with input image
    client = vision.ImageAnnotatorClient()

    # read image from file
    content = load_image(path)
    image = vision.Image(content=content)

    # call API to detect classes
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
