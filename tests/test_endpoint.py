from pathlib import Path
from unittest.mock import patch

import pytest
from pytest_mock import MockerFixture

# get_calories mock
# test enum paths are calling correct values
# mock -> return classificaiton
# get_calorie_estimation mock
#
from app.api.endpoint import ModeEnum, get_calories
from app.util import delete_file, save_image
from tests.test_images.b64image import TEST_OMELETTE


@pytest.fixture()
def mock_fn(mocker: "MockerFixture"):
    fn = mocker.patch("app.estimator.vision.get_food_classification")
    return fn


@patch("google.cloud.vision.ImageAnnotatorClient")
@patch("app.estimator.vision.get_food_classification")
def test_get_calories_vision_calls_vision_function(mock_client, mock_vision):
    enum = ModeEnum.VISION
    save_image(TEST_OMELETTE, Path("test_images/omelette.jpeg"))
    image = Path("test_images/omelette.jpeg")
    get_calories(image, enum)
    mock_vision.assert_called_once()
    delete_file(image)


# @patch("app.estimator.yolo.detect_food_items")
# @patch("app.estimator.yolo.parse_output")
# @patch("app.estimator.yolo.MODEL_VERSION")
# def test_get_calories_yolo_calls_yolo_functions(mock_yolo, mock_parse, null):
#     enum = ModeEnum.YOLO
#     image = Path("test_images/omelette.jpeg")
#     get_calories(image, enum)
#     mock_yolo.assert_called_once()
#     mock_parse.assert_called_once()


# def test_get_calories_yolo_returns_item_height_width():


# def test_get_calories_keyerror_is_raised_with_invalid_enum():


# def test_classification_unavailable_returns_none():
#     # mock empty item
#     empty_image = Path("test_images/")
#     assert get_calories(empty_image) is None


# def test_classification_available_returns_details():
#
