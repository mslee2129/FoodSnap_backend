import numpy as np

from app.estimator.weight import calculate_food_weight, get_label_weights


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
