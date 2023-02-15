"""REST API endpoint for computing calorie information from uploaded image."""

from enum import Enum
from pathlib import Path
from typing import Any, Optional

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from app.estimator.calories import FoodDetails, get_food_details
from app.estimator.vision import get_food_classification
from app.estimator.weight import calculate_food_weight
from app.estimator.yolo import detect_food_items, parse_output
from app.util import delete_file, save_image

app = Flask(__name__)
cors = CORS(app)

# directory to temporarily save images
IMAGE_DIR = Path("tmp/")


# mode for estimation
class ModeEnum(Enum):
    VISION = "vision"
    YOLO = "yolo"


def get_calories(
    image: Path, mode: ModeEnum = ModeEnum.VISION
) -> Optional[FoodDetails]:
    """
    Retrieve calorie information for image located at specified path.
    Args:
        image (Path): Image location for calorie prediction.
        mode (ModeEnum): Estimation mode (default is to use Vision API).
    Returns:
        FoodDetails: Food label and nutrition details.
    """
    # set default weight to 100g
    weight = 100.0

    if mode == ModeEnum.VISION:
        # generate food classification from Google Vision API
        item = get_food_classification(image)

    elif mode == ModeEnum.YOLO:
        # generate output from YOLO model
        dims, labels = detect_food_items(image)

        # extract relevant fields from model output
        item, height, width = parse_output(dims, labels)

        # compute weight estimation
        if item:
            weight = calculate_food_weight(item, height, width)

    else:
        raise KeyError(f"Unknown estimation mode: {mode}")

    # if classification available then get details
    if item:
        # retrieve calorie information for classification from Edamam API
        details = get_food_details(item, weight)
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

        # ensure filename present
        if not image.filename:
            raise ValueError("Filename for uploaded image not present.")

        # save image
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        image_path = IMAGE_DIR / image.filename
        save_image(image.read(), image_path)

        # generate calorie information
        data = get_calories(image_path, ModeEnum.YOLO)

        # remove image
        delete_file(image_path)
        IMAGE_DIR.rmdir()

        # send response if food classified correctly
        if not data:
            raise ValueError(f"Failed to estimate calories for image: {image.filename}")
        return jsonify(
            {
                "msg": "success",
                "label": data.label,
                "nutrition": data.nutrition,
                "weight": data.weight,
            }
        )
    except Exception as e:
        abort(500, f"Unable to return calorie information due to error: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
