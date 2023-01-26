"""REST API endpoint for computing calorie information from uploaded image."""

from typing import Any, Optional

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from app.calories import FoodDetails, get_food_details
from app.vision import get_food_classification

PORT = 5000

app = Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True


def get_calories(image: bytes) -> Optional[FoodDetails]:
    """
    Retrieve calorie information for base64 encoded input image.
    Args:
        image(bytes): Base64 encoded image for calorie prediction.
    Returns:
        FoodDetails: Food label and nutrition details.
    """
    # generate food classification from Google Vision API
    search = get_food_classification(image)

    # if classification available then get details
    if search:
        # retrieve calorie information for classification from Edamam API
        details = get_food_details(search)
        return details

    return None


@app.route("/", methods=["POST"])
def get_calorie_estimation() -> Any:
    """Endpoint to retrieve calorie information from image in POST request."""
    try:
        # check that file is in request
        if "file" not in request.files.to_dict():
            abort(400, "File not received.")

        # extract image from request
        image = request.files.to_dict()["file"]

        # generate calorie information
        data = get_calories(image.read())

        # send response if food classified correctly
        if not data:
            raise ValueError
        return jsonify(
            {
                "msg": "success",
                "label": data.label,
                "nutrition": data.nutrition,
            }
        )
    except Exception:
        abort(500, "Unable to return calorie information.")


if __name__ == "__main__":
    app.run(port=PORT, debug=True)
