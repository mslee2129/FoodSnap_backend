"""REST API endpoint for computing calorie information from uploaded image."""

import logging
from enum import Enum
from pathlib import Path
from typing import Any, List, Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from app.estimator.calories import get_food_details
from app.estimator.vision import get_food_classification
from app.estimator.weight import (
    calculate_pixel_plate,
    get_food_weights,
    get_params_weight,
)
from app.estimator.yolo import detect_food_items, get_num_plate_food
from app.util import delete_file, save_image

log = logging.getLogger("API")

app = Flask(__name__)
cors = CORS(app)

# directory to temporarily save images
IMAGE_DIR = Path("tmp/")


# code for type of computation
class ModelCodeEnum(Enum):
    YOLO_USE_PLATE_SIZE = "YOLO_USE_PLATE_SIZE"
    YOLO_USE_IMAGE_SIZE = "YOLO_USE_IMAGE_SIZE"
    VISION_DEFAULT = "VISION_DEFAULT"
    NO_FOOD_DETECTED = "NO_FOOD_DETECTED"


def get_model_predictions(
    image: Path, plate_diameter: float = 25.0
) -> Tuple[List, List, bool, bool]:
    """
    Obtain food classifications from YOLO model and compute weights
    based on the plate (if present) or image size.
    Args:
        image (Path): Image location for calorie prediction.
        plate_diameter (float): Diameter of plate.
    Returns:
        labels_list (List): List of food items.
        weights_list (List): List of weights corresponding to food items.
        use_plate (bool): Whether or not the plate was used for weight
            calculation.
        success (bool): Whether or not the prediction was a success.
    """
    # initialise return values
    success, use_plate = False, False
    labels_list: List[str] = []
    weights_list: List[float] = []

    # Step 1 - generate predictions from YOLO model
    labels, areas, _ = detect_food_items(image)

    # Step 2 - parse output from YOLO model and see if predictions available
    if any(labels):
        # count number of plates and food items identified
        plate_counter, food_counter = get_num_plate_food(labels)

        # generate weights if food is recognized by YOLO
        if food_counter >= 1:
            # Step 3 - get list of foods and pixels without plate
            labels_list, pixels_food = get_params_weight(labels, areas)
            log.info(f"[YOLO] {len(labels_list)} food items recognised.")

            # Step 4a - calculate weight assuming a plate size
            if plate_counter == 1:
                # adds all the food and plate pixel up, assuming all foods are on the plate
                pixel_plate = calculate_pixel_plate(areas)

                # ensure supplied plate size is sensible otherwise set to default
                if plate_diameter < 10.0 or plate_diameter > 40.0:
                    plate_diameter = 25.0

                # compute weight using plate
                weights_list = get_food_weights(
                    labels_list, pixels_food, pixel_plate, plate_diameter, plate=True
                )
                log.info(
                    f"[YOLO] Using plate of size {plate_diameter}cm to estimate weight."
                )
                use_plate = True

            # Step 4b - calculate weight assuming image size (no plate)
            else:
                log.info("[YOLO] Using image size to estimate weight.")
                weights_list = get_food_weights(labels_list, pixels_food)

            # set model success
            success = True

    return labels_list, weights_list, use_plate, success


def get_calories(
    image: Path, plate_diameter: float = 25.0
) -> Tuple[List, ModelCodeEnum]:
    """
    Retrieve calorie information for image located at specified path.
    Args:
        image (Path): Image location for calorie prediction.
        plate_diameter (float): Diameter of plate.
    Returns:
        food_details (List): Food label and nutrition details.
        model_code (ModelCodeEnum): Model calculation mode used.
    """
    # Step 1 - invoke YOLO model
    log.info("[Endpoint] Invoking YOLO model.")
    items, weights, use_plate, success = get_model_predictions(image, plate_diameter)
    if success:
        if use_plate:
            model_code = ModelCodeEnum.YOLO_USE_PLATE_SIZE
        else:
            model_code = ModelCodeEnum.YOLO_USE_IMAGE_SIZE

    # Step 2 - invoke Vision API as default if YOLO unsuccessful
    else:
        log.info("[Endpoint] Invoking Vision API.")
        items, weights = [], []
        model_code = ModelCodeEnum.VISION_DEFAULT
        item = get_food_classification(image)
        # set default weight to 100g
        if item:
            items.append(item)
            weights.append(100.0)

    # Step 3 - generate calorie information using Edamam API
    food_details = []
    if items and weights and len(items) == len(weights):
        for i in range(len(items)):
            data = get_food_details(items[i], weights[i])
            food_details.append(
                {
                    "label": data.label,
                    "nutrition": data.nutrition,
                    "weight": data.weight,
                }
            )

    return food_details, model_code


@app.route("/", methods=["POST"])
def get_calorie_estimation() -> Any:
    """Endpoint to retrieve calorie information from image in POST request."""

    try:
        # check that file is in request
        if "file" not in request.files.to_dict():
            abort(400, "File not received.")

        # extract image from request
        image = request.files.to_dict()["file"]

        # extract plate size from request if available otherwise set default
        try:
            plate_size = float(request.files.to_dict()["plateValue"])
        except Exception:
            plate_size = 25.0

        # ensure filename present
        if not image.filename:
            raise ValueError("Filename for uploaded image not present.")

        # save image
        IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        image_path = IMAGE_DIR / image.filename
        save_image(image.read(), image_path)

        try:
            # generate calorie information
            results, model_code = get_calories(image_path, plate_size)
        except Exception:
            raise
        finally:
            # remove directory irrespective of failure
            delete_file(image_path)
            IMAGE_DIR.rmdir()

        # send response depending on whether or not food items are detected
        response = {
            "status": "failure",
            "model_code": ModelCodeEnum.NO_FOOD_DETECTED.value,
            "results": [],
        }
        if results:
            response = {
                "status": "success",
                "model_code": model_code.value,
                "results": results,
            }
            log.info(f"[Endpoint] Sending successful response: {response}")
        return jsonify(response)

    except Exception as e:
        msg = f"Unable to return calorie information due to error: {e}"
        log.error(msg)
        abort(500, msg)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
