from pathlib import Path
from typing import Any, Tuple

import numpy as np
from numpy.typing import NDArray
from ultralytics import YOLO

from app.estimator.constants import MODEL_VERSION


def detect_food_items(input: Path) -> Tuple[NDArray, NDArray, NDArray]:
    """
    Generate food class prediction and item area
    using YOLO model.
    Args:
        input (Path): Path to image for classification.
    Returns:
        labels (NDArray): (N) 1D array containing food items.
        area (NDArray): (N) 1D array containing the area of the
            image containing the class in labels[i]
        dims (NDArray): (N, 2) array containing normalised
            height and width values.
    """
    # load pre-trained model
    model = YOLO(MODEL_VERSION)

    # generate prediction based on input image
    results = model.predict(source=input, save=False)

    # get identified classes
    cls_tensor = results[0].boxes.cls

    # create numpy label array
    cls_np = np.expand_dims(cls_tensor.detach().numpy(), axis=0)
    names_dict = model.names
    to_np = np.vectorize(lambda i: names_dict[i])
    labels = (np.asarray(to_np(cls_np))).flatten()

    # extract mask element
    mask_data = results[0].masks.data  # raw masks tensor (N, H, W)

    # create empty np array for object areas
    areas = np.empty(shape=labels.size, dtype=float)

    # iterate through elements in tensor and extract mask size
    for i in range(mask_data.shape[0]):
        mask_zero = (mask_data[i] == 0).sum()
        mask_one = (mask_data[i] == 1).sum()
        area_tensor = mask_one / (mask_zero + mask_one)
        areas[i] = area_tensor.detach().numpy()

    # get normalized width and height
    pos_tensor = results[0].boxes.xywhn

    # convert to numpy array and delete coordinates of box
    pos_np = pos_tensor.detach().numpy()
    dims = np.delete(pos_np, [0, 1], axis=1)

    return labels, areas, dims


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
