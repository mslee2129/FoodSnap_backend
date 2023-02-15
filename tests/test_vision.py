from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from app.estimator.vision import get_food_classification

VALID_ITEMS = ["pizza", "omelette", "burger"]


@patch("google.cloud.vision.ImageAnnotatorClient")
@patch("builtins.open", new_callable=mock_open, read_data=b"data")
def test_get_food_classification(mock_file, mock_vision):
    """Tests response from Google vision request with a mock object"""
    mock_response = MagicMock()
    mock_labels = [
        MagicMock(description="Pizza", score=0.9),
        MagicMock(description="Burger", score=0.8),
        MagicMock(description="Omelette", score=0.7),
    ]
    mock_response.label_annotations = mock_labels
    mock_vision().label_detection.return_value = mock_response

    # call the function with mock input
    input_data = Path("path/to/image")
    result = get_food_classification(input_data)

    # assert the result is as expected
    assert "Pizza" == result


@patch("google.cloud.vision.ImageAnnotatorClient")
@patch("builtins.open", new_callable=mock_open, read_data=b"data")
def test_get_food_classification_none(mock_file, mock_vision):
    """Tests response from Google vision request with a mock object"""
    mock_response = MagicMock()
    mock_labels = [
        MagicMock(description="apple", score=0.9),
        MagicMock(description="banana", score=0.8),
        MagicMock(description="orange", score=0.7),
    ]
    mock_response.label_annotations = mock_labels
    mock_vision().label_detection.return_value = mock_response

    # call the function with mock input
    input_data = Path("path/to/image")
    result = get_food_classification(input_data)

    # assert the result is as expected
    assert result is None
