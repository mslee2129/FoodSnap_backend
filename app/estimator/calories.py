"""Functions to retrieve nutritional information from the Edamam API based on a search string."""
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict

import requests

from app.estimator.constants import EDAMAM_URL

log = logging.getLogger("calories")

try:
    # load environment variables for using Edamam API
    APP_KEY = os.environ["EDAMAM_KEY"]
    APP_ID = os.environ["EDAMAM_ID"]
except KeyError:
    raise EnvironmentError(
        "Not all environment variables seem to be set: "
        + f"\n EDAMAM_KEY = {os.environ.get('EDAMAM_KEY', '<UNSET>')}"
        + f"\n EDAMAM_ID = {os.environ.get('EDAMAM_ID', '<UNSET>')}"
    )


@dataclass
class FoodDetails:
    """
    Store food label and nutritional information.
    Attributes:
        label (str): Label from Edamam API
        nutrition (dict[str, float]): Nutritional values for specified weight.
        weight (float): Weight of item in grams (used to scale nutrition values).
    """

    label: str
    nutrition: dict[str, float]
    weight: float = 100.0


def get_food_details(search: str, weight: float = 100.0) -> FoodDetails:
    """
    Entry point for generating nutritional information using the
    Edamam API for an input food search term.
    Args:
        search (str): Food item for request.
        weight (float): Estimated weight in grams.
    Returns:
        FoodDetails: Food label and nutrition details.
    """
    # make Edamam API call
    response = make_request(search)
    data = check_response(response)

    # parse relevant data from API
    details = parse_json(data)

    # scale nutrition by weight
    details = scale_nutrition(details, weight)

    return details


def make_request(search: str) -> Any:
    """
    Request calorie information from Edamam API based on input
    search string.
    Args:
        search (str): Food item for request.
    Returns:
        Any: API response in JSON form if response is successful.
    """

    # parameters required for API call
    params = {"app_id": APP_ID, "app_key": APP_KEY, "ingr": search}

    # make request
    response = requests.get(url=EDAMAM_URL, params=params)

    if not response.ok:
        raise ValueError(f"Edamam API could not return information for term: {search}")

    return response


def check_response(response: Any) -> Any:
    """
    Takes an Edamam API response and checks response integrity.
    Args:
        response (Any): JSON response from API call.
    Returns:
        data (Any): SUbset of integrity-checked data from API
            call as JSON.
    """
    # extract response in JSON format
    data = response.json()

    # extract relevant key: either 'parsed' or 'hints'
    key = "parsed"
    if len(data[key]) == 0:
        key = "hints"

    # check for integrity of data
    if not data[key][0]["food"]["label"]:
        raise KeyError("API response data does not contain expected 'label' key")

    if not data[key][0]["food"]["nutrients"]:
        raise KeyError("API response data does not contain expected 'nutrients' key")

    return data[key][0]["food"]


def parse_json(data: Dict[Any, Any]) -> FoodDetails:
    """
    Parse JSON returned from Edamam API. Extract only the relevant
    information which includes the food label and nutrition details.
    Args:
        data (dict[Any, Any]): JSON returned from Edamam API.
    Returns:
        FoodDetails: Food label and nutrition details.
    """
    # parse food label
    label = data["label"]

    # parse nutrition data - dictionary containing multiple values (incl. KCal per 100g)
    nutrition = data["nutrients"]

    # construct food details based on relevant information
    details = FoodDetails(label, nutrition)
    log.info(f"[Edamam API] Item: {label} - Nutrition: {nutrition}")

    return details


def scale_nutrition(details: FoodDetails, weight: float) -> FoodDetails:
    """
    Scale nutritional values (default 100g) in FoodDetails based on
    input weight.
    Args:
        details (FoodDetails): FoodDetails class containg nutritional
            values to be scaled.
        weight (float): Weight in grams.
    Returns:
        details (FoodDetails): FoodDetails object with scaled values.
    """
    # Scale nutrition values by weight
    details.nutrition = {
        k: round((entry / 100.0) * weight, 1) for k, entry in details.nutrition.items()
    }
    # Set weight attribute to passed in weight
    details.weight = round(weight, 2)

    return details
