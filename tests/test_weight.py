import numpy as np

from app.estimator.constants import DENSITY_DICT, DEPTH_DICT, IMAGE_HEIGHT, IMAGE_WIDTH
from app.estimator.weight import get_food_weights, get_label_weights, get_params_weight


def test_get_food_weights():
    """
    Tests function that calculates food weights, with and without plate.
    Includes tests for calculate_food_weight_plate() and calculate_food_weight.
    These functions are called by get_food_weights.

    """
    # test calculation without plate
    labels_list = ["omelette", "pizza", "burger"]
    pixels_food = [0.2, 0.3, 0.2]

    weights_list = get_food_weights(labels_list, pixels_food)

    # calculate weights for all three items
    area_image = IMAGE_HEIGHT * IMAGE_WIDTH

    area_omelette = area_image * 0.2
    weight_omelette = (
        area_omelette * DEPTH_DICT[labels_list[0]] * DENSITY_DICT[labels_list[0]]
    )

    area_pizza = area_image * 0.3
    weight_pizza = (
        area_pizza * DEPTH_DICT[labels_list[1]] * DENSITY_DICT[labels_list[1]]
    )

    area_burger = area_image * 0.2
    weight_burger = (
        area_burger * DEPTH_DICT[labels_list[2]] * DENSITY_DICT[labels_list[2]]
    )

    # compare results
    assert weight_omelette == weights_list[0]
    assert weight_pizza == weights_list[1]
    assert weight_burger == weights_list[2]

    # test calculation with plate, assuming plate pixel of 0.8
    pixel_plate = 0.8
    weights_list_plate = get_food_weights(
        labels_list, pixels_food, pixel_plate, plate=True
    )

    # calculate plate area
    plate_area = np.pi * (25.0 / 2) ** 2

    # calculate weights of all three items
    area_omelette_plate = (pixels_food[0] / pixel_plate) * plate_area
    weight_omelette_plate = (
        area_omelette_plate * DEPTH_DICT[labels_list[0]] * DENSITY_DICT[labels_list[0]]
    )

    area_pizza_plate = (pixels_food[1] / pixel_plate) * plate_area
    weight_pizza_plate = (
        area_pizza_plate * DEPTH_DICT[labels_list[1]] * DENSITY_DICT[labels_list[1]]
    )

    area_burger_plate = (pixels_food[2] / pixel_plate) * plate_area
    weight_burger_plate = (
        area_burger_plate * DEPTH_DICT[labels_list[2]] * DENSITY_DICT[labels_list[2]]
    )

    # compare results
    assert weight_omelette_plate == weights_list_plate[0]
    assert weight_pizza_plate == weights_list_plate[1]
    assert weight_burger_plate == weights_list_plate[2]


def test_get_params_weight():
    """Tests functions that fetches params for calculate_food_weight_plate"""

    # create test input arrays and call function
    label_array = np.array(["plate", "omelette", "apple"])
    pixel_array = np.array([0.5, 0.3, 0.1])

    label_food, pixel_food = get_params_weight(label_array, pixel_array)

    plate_counter = 0
    for item in label_food:
        if item == "plate":
            plate_counter += 1

    # assert results
    assert label_food[0] == "omelette"
    assert label_food[1] == "apple"
    assert pixel_food[0] == 0.3
    assert pixel_food[1] == 0.1
    assert plate_counter == 0


def test_get_label_weights():
    """Tests simple weight calculation with sample data"""

    dimensions_array = np.array([[0.3, 0.4], [0.5, 0.6], [0.7, 0.6]])
    label_array = np.array([["omelette", "burger", "pizza"]])

    result = get_label_weights(dimensions_array, label_array)

    expected_labels = ["omelette", "burger", "pizza"]
    for i, label in enumerate(expected_labels):
        assert result[i, 0] == label
        assert isinstance(result[i, 1], float)
