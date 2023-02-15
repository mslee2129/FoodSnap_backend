from unittest.mock import MagicMock

import requests_mock

from app.estimator.calories import FoodDetails, check_response, make_request, parse_json
from app.estimator.constants import EDAMAM_URL


def test_food_details_object_is_correct():
    """Test instantiation of FoodDetails object."""
    label = "pizza"
    nutrition = {
        "fat": 12.0,
    }
    details = FoodDetails(label, nutrition)
    assert details.label == label
    assert details.nutrition == nutrition


def test_make_request_success():
    """Tests function handles successful requests appropriately"""
    search = "pizza"
    with requests_mock.Mocker() as m:
        m.get(
            EDAMAM_URL,
            status_code=200,
            json={"parsed": [{"food": {"label": "pizza", "nutrients": {"kcal": 100}}}]},
        )
        response = make_request(search)

        assert response is not None
        assert response.ok
        assert response.json() == {
            "parsed": [{"food": {"label": "pizza", "nutrients": {"kcal": 100}}}]
        }


def test_make_request_failure():
    """Tests function handles unsuccessful requests appropriately"""
    search = "no_pizza"

    try:
        make_request(search)
    except ValueError as e:
        assert (
            str(e) == f"Edamam API could not return information for term: {search}"
        ), "Incorrect error message"


def test_data_integrity_is_checked():
    """Tests that data integrity check successfully returns parsed key"""
    mock_json = MagicMock()
    data = {"parsed": [{"food": {"label": "Test Food", "nutrients": {"KCal": 100}}}]}
    mock_json.loads(data)

    assert check_response(mock_json)


def test_data_integrity_check_raises_error():
    """Tests that KeyError is raised with missing data"""
    mock_json = MagicMock()
    data = {
        "no_parsed": [{"food": {"no_label": "Test Food", "nutrients": {"KCal": 100}}}]
    }
    mock_json.loads(data)

    try:
        check_response(mock_json)
    except KeyError as e:
        assert (
            str(e) == "API response data does not contain expected label key"
        ), "Incorrect error message"

    """ Tests that KeyError is raised with missing nutrients"""
    mock_json = MagicMock()
    data = {
        "no_parsed": [
            {"food": {"no_label": "Test Food", "no_nutrients": {"KCal": 100}}}
        ]
    }
    mock_json.loads(data)

    try:
        check_response(mock_json)
    except KeyError as e:
        assert (
            str(e) == "API response data does not contain expected nutrients key"
        ), "Incorrect error message"


def test_json_is_parsed():
    """Tests that check JSON files are sufficiently parsed"""
    # Test data
    data = {"label": "Test Food", "nutrients": {"KCal": 100}}

    # Call the function
    result = parse_json(data)

    # Check the result
    assert isinstance(result, FoodDetails)
    assert result.label == "Test Food"
    assert result.nutrition == {"KCal": 100}
