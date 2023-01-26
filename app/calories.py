"""Functions to retrieve nutritional information from the Edamam API based on a search string."""
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict

import requests

from app.constants import EDAMAM_URL

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
    """

    label: str
    nutrition: dict[str, float]


def get_food_details(search: str) -> FoodDetails:
    """
    Entry point for generating nutritional information using the
    Edamam API for an input food search term.
    Args:
        search (str): Food item for request.
    Returns:
        FoodDetails: Food label and nutrition details.
    """
    # make Edamam API call
    data = make_request(search)

    # parse relevant data from API
    details = parse_json(data)

    return details


def make_request(search: str) -> Any:
    """
    Request calorie information from Edamam API based on input
    search string.
    Args:
        search (str): Food item for request.
    Returns:
        Any: API response in JSON form.
    """
    # parameters required for API call
    params = {"app_id": APP_ID, "app_key": APP_KEY, "ingr": search}

    # make request
    r = requests.get(url=EDAMAM_URL, params=params)

    # extract response in JSON format
    data = r.json()

    # ensure response as expected
    if not data["parsed"]:
        raise ValueError(f"Edamam API could not return information for term: {search}")

    return data


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
    label = data["parsed"][0]["food"]["label"]

    # parse nutrition data - dictionary containing multiple values (incl. KCal per 100g)
    nutrition = data["parsed"][0]["food"]["nutrients"]

    # construct food details based on relevant information
    details = FoodDetails(label, nutrition)
    log.info(f"[Edamam API] Item: {label} - Nutrition: {nutrition}")

    return details
