import numpy as np

from app.estimator.yolo import get_num_plate_food


def test_get_num_plate_food():
    """Tests counter of plates and foods recognized by YOLO model"""

    labels = ["omelette", "pizza", "burger", "plate"]
    labels = np.array(labels)

    plate_counter, food_counter = get_num_plate_food(labels)

    assert plate_counter == 1
    assert food_counter == 3
