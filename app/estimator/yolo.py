from pathlib import Path
from typing import Any, Tuple

import numpy as np
from numpy.typing import NDArray
from ultralytics import YOLO

from app.estimator.constants import MODEL_VERSION


def detect_food_items(input: Path) -> Tuple[NDArray, NDArray]:
    """
    Generate food class prediction and item coordinates
    using YOLO model.
    Args:
        input (Path): Path to image for classification.
    Returns:
        dims (NDArray): (N, 2) array containing normalised
            height and width values.
        labels (NDArray): (1, N) array containing food items.
    """
    # load pre-trained model
    model = YOLO(MODEL_VERSION)

    # generate prediction based on input image
    # classes: classes included in search (0 = bowl, 1 = omelette, 2 = plate)
    results = model.predict(source=input, classes=[1])

    # get normalized width and height
    pos_tensor = results[0].boxes.xywhn

    # get identified classes
    cls_tensor = results[0].boxes.cls

    # convert to numpy array and delete coordinates of box
    pos_np = pos_tensor.detach().numpy()
    dims = np.delete(pos_np, [0, 1], axis=1)

    # create numpy label array
    cls_np = np.expand_dims(cls_tensor.detach().numpy(), axis=0)
    names_dict = model.names
    to_np = np.vectorize(lambda i: names_dict[i])
    labels = to_np(cls_np)

    return dims, labels


def parse_output(dims: NDArray, labels: NDArray) -> Tuple[Any, Any, Any]:
    """
    Parse output from YOLO model.
    Args:
        dims (NDArray): (N, 2) array containing two columns:
            [Normalised Width, Normalised Height].
        labels (NDArray): (1, N) array detailing class labels.
    Returns:
        label (str | NDArray): Label string or array (multiple elements).
        width (float | NDArray): Width value or array (multiple elements).
        height (float | NDArray): Height value or array (multiple elements).
    """
    # extract relevant fields
    label = labels[:, 0]
    width = dims[:, 0]
    height = dims[:, 1]

    # TODO: currently assumes 1 record
    if len(label) == 1:
        label = label[0]
    if len(width) == 1:
        width = width[0]
    if len(height) == 1:
        height = height[0]

    return label, width, height
