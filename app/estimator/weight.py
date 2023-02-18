"""Functions to estimate the weight of a food item."""

import numpy as np
from numpy.typing import NDArray

from app.estimator.constants import (
    AREA_FILL,
    DENSITY_DICT,
    DEPTH_DICT,
    IMAGE_HEIGHT,
    IMAGE_WIDTH,
)


def calculate_food_weight_plate(
    label: str, pixel_plate: float, pixel_food: float, plate_area: int = 25
) -> float:
    """
    Estimates weight of food item in grams given a plate of fixed size as reference
    Args:
        label (str): Food item for estimation.
        pixel_plate (float): number of pixel of the plate relative to image.
        pixel_food (float): number of pixel of the food relative to image.
        plate area (int): size of plate in scm.
    Returns:
        weight (float): weight of food item in grams.
    """

    # calculate the are of the food
    area_rel = pixel_food / pixel_plate
    area = area_rel * plate_area

    # convert label to lowercase for dict values
    label = label.lower()

    # calculate weight assuming depth and density and converting into g
    weight = area * DEPTH_DICT[label] * DENSITY_DICT[label]

    return weight


def get_params_weight(
    dimensions_array: NDArray, label_array: NDArray, pixel_array: NDArray
) -> tuple:
    """
    Takes in model output and gets params for calculate_food_weight_plate.
    Args:
        dimensions_array (NDArray): (N, 2) with width, height for each object.
        label_array (NDArray): (N, ) with label for each object.
        pixel_array (NDArray): (N, ) with pixel relative to image for each object.
    Returns:
        params (tuple): label of food, pixel_plate, and pixal_food.
    """

    # check if plate is recognized
    plate_counter = 0
    for i, label in label_array:
        if label == "plate":
            plate_counter += 1
            plate_index = i
            break
        elif label != "plate":
            food_index = i
    if plate_counter == 0:
        raise ValueError("No plate found")
    if plate_counter > 1:
        raise ValueError("Too many plates recognized")

    # assign params
    pixel_plate = pixel_array[plate_index]
    pixel_food = pixel_array(food_index)
    label_food = label_array[food_index]

    return (label_food, pixel_plate, pixel_food)


def calculate_food_weight(
    label: str, rel_height: float, rel_width: float, camera_distance: float = 20
) -> float:
    """
    Estimates weight of food item in grams, assuming a distance.
    Args:
        label (str): Food item for estimation.
        rel_height (float): Height of food item relative to image size.
        rel_width (float): Width of food item relative to image size.
        camera_distance (float): Assumed distance of camera to food item.
    Returns:
        weight (float): Weight of food item in grams.
    """

    # calculate area in scm using constants
    abs_height = IMAGE_HEIGHT * rel_height
    abs_width = IMAGE_WIDTH * rel_width
    area = abs_height * abs_width

    # convert label to lowercase for dict values
    label = label.lower()

    # calculate weight assuming depth and density and converting into g
    weight = area * DEPTH_DICT[label] * AREA_FILL * DENSITY_DICT[label]

    return weight


def get_label_weights(dimensions_array: NDArray, label_array: NDArray) -> NDArray:
    """
    Takes in model output in form of dimension (N, 2) and label arrays (1, N)
    and returns label and weight array (N, 2).
    Args:
        dimensions_array (NDArray): (N, 2) with width, height for each object.
        label_array (NDArray): (1, N) with label for each object.
    Returns:
        NDArray: (N, 2) with label and weight for each object.
    """
    N = dimensions_array.shape[0]
    result = np.zeros((N, 2), dtype=object)

    # calculate weight for each label
    for i in range(N):
        label = label_array[0, i]
        height, width = dimensions_array[i]
        weight = calculate_food_weight(label, height, width)
        result[i, 0] = label
        result[i, 1] = weight

    # return array with labels and weights
    return result
