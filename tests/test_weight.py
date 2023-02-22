import numpy as np

from app.estimator.weight import (
    calculate_food_weight,
    calculate_food_weight_plate,
    get_label_weights,
    get_params_weight,
)


def test_calculate_food_weight_plate():
    """Tests weight function that uses plate as refernce"""

    # test function with test inputs for omelette
    label = "omelette"
    pixel_food = 0.25
    pixel_plate = 0.3

    # assuming a plate of area 490 scm as in the function
    area_rel = pixel_food / (pixel_food + pixel_plate)
    area = area_rel * 490
    weight_test = area * 1.0 * 0.8

    result = calculate_food_weight_plate(label, pixel_plate, pixel_food)

    assert weight_test == result


def test_get_params_weight():
    """Tests functions that fetches params for calculate_food_weight_plate"""

    # create test input arrays and call function
    dimensions_array = None
    label_array = np.array(["plate", "omelette"])
    pixel_array = np.array([0.5, 0.3])

    label_food, pixel_plate, pixel_food = get_params_weight(
        dimensions_array, label_array, pixel_array
    )

    # assert results
    assert label_food == "omelette"
    assert pixel_plate == 0.5
    assert pixel_food == 0.3


def test_calculate_food_weight():
    """Tests simple weight calculation with sample data"""

    # test function with test inputs for omelette
    height_test = 0.2 * 30
    width_test = 0.3 * 22
    area_test = height_test * width_test
    weight_test = area_test * 1.0 * 0.7 * 0.8

    result = calculate_food_weight("omelette", 0.2, 0.3)

    assert weight_test == result


def test_get_label_weights():
    """Tests simple weight calculation with sample data"""

    dimensions_array = np.array([[0.3, 0.4], [0.5, 0.6], [0.7, 0.6]])
    label_array = np.array([["omelette", "burger", "pizza"]])

    result = get_label_weights(dimensions_array, label_array)

    expected_labels = ["omelette", "burger", "pizza"]
    for i, label in enumerate(expected_labels):
        assert result[i, 0] == label
        assert isinstance(result[i, 1], float)
