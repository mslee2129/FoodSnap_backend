"""Functions to estimate the weight of a food item."""
from typing import List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

from app.estimator.constants import DENSITY_DICT, DEPTH_DICT, IMAGE_HEIGHT, IMAGE_WIDTH


def get_food_weights(
    label_list: List,
    pixel_list: List,
    pixel_plate: Optional[float] = None,
    plate_diameter: float = 25.0,
    plate: bool = False,
) -> List[float]:
    """
    Puts the weights of all recognized food items into a list.
    Args:
        label_list (List): List of food items recognized.
        pixel_list (List): List of pixel for each food item, corresponding to label_list.
        pixel_plate (float): Pixel of plate relative to image (None default).
        plate_diameter (float): Diameter of plate.
        plate (bool): If true, pixel plate must also be passed; invokes calculation using plate.
    Returns:
        List[float]: List of weights (in g) of all recognized food items.
    """

    # initialize list
    weights = []

    # calculation without plate
    if not plate:
        for i in range(len(label_list)):
            weight = calculate_food_weight(label_list[i], pixel_list[i])
            weights.append(weight)

    # calculate with plate if recognized
    else:
        if not pixel_plate:
            raise ValueError("No plate pixel passed!")
        for i in range(len(label_list)):
            weight = calculate_food_weight_plate(
                label_list[i], pixel_plate, pixel_list[i], plate_diameter
            )
            weights.append(weight)

    return weights


def calculate_pixel_plate(areas: NDArray) -> float:
    """
    Adds up all the relative pixel values of the food items and the plate,
    assuming all food items are placed on the plate.
    Args:
        areas (NDarray): Pixels relative to image of all recognized objects.
    Returns:
        pixel_item (float): Pixels of the plate relative to total image pixels.
    """
    pixel_plate = 0
    for pixel_item in areas:
        pixel_plate += pixel_item

    return pixel_item


def calculate_food_weight_plate(
    label: str, pixel_plate: float, pixel_food: float, plate_diameter: float = 25.0
) -> float:
    """
    Estimates weight of food item in grams given a plate of fixed size as reference.
    Args:
        label (str): Food item for estimation.
        pixel_plate (float): Number of pixels of the plate relative to image.
        pixel_food (float): Number of pixels of the food relative to image.
        plate_diameter (float): Diameter of plate (default is 25.0).
    Returns:
        weight (float): Weight of food item in grams.
    """
    # calculate plate area
    plate_area = np.pi * (plate_diameter / 2) ** 2

    # calculate the area of the food
    area_rel = pixel_food / pixel_plate
    area = area_rel * plate_area

    # convert label to lowercase for dict values
    label = label.lower()

    # calculate weight assuming depth and density and converting into g
    weight = area * DEPTH_DICT[label] * DENSITY_DICT[label]

    return weight


def get_params_weight(label_array: NDArray, pixel_array: NDArray) -> Tuple[List, List]:
    """
    Removes the plate from the numpy arrays and returns two lists with food
    labels and pixels.
    Args:
        label_array (NDArray): (N, ) with label for each object.
        pixel_array (NDArray): (N, ) with pixel relative to image for each object.
    Returns:
        Tuple[List, List]: Two lists of all food labels and relative pixel areas.
    """

    # initialize empty lists
    label_list, pixel_list = [], []

    # copy foods and pixels into lists
    for i, label in enumerate(label_array):
        if label != "plate":
            label_list.append(label)
            pixel_list.append(pixel_array[i])

    return label_list, pixel_list


def calculate_food_weight(
    label: str, pixel_food: float, camera_distance: float = 20.0
) -> float:
    """
    Estimates weight of food item in grams, assuming a camera distance and the
    angle of the camera being directly above.
    Args:
        label (str): Food item for estimation.
        pixel_food (float): Pixel of food relative to image pixels.
        camera_distance (float): Assumed distance of camera to food item. Please note,
            the camera distance is not used in the calculation itself, but determines the
            constants IMAGE_HEIGHT and IMAGE_WIDTH used. 20cm in this case corresponds to
            a height and width of 30cm and 22cm.
    Returns:
        weight (float): Weight of food item in grams.
    """

    # calculate area image in scm
    area_image = IMAGE_HEIGHT * IMAGE_WIDTH

    # calculate area of food in scm
    area_food = area_image * pixel_food

    # convert label to lowercase for dict values
    label = label.lower()

    # calculate weight assuming depth and density and converting into g
    weight = area_food * DEPTH_DICT[label] * DENSITY_DICT[label]

    return weight


# currently not used
def get_label_weights(dimensions_array: NDArray, label_array: NDArray) -> NDArray:
    """
    Takes in model output in form of dimension (N, 2) and label arrays (1, N)
    and returns label and weight array (N, 2), assuming a camera distance.
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
