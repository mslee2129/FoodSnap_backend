from app.calories import FoodDetails


def test_food_details_values():
    """Test instantiation of FoodDetails object."""
    label = "pizza"
    nutrition = {
        "fat": 12.0,
    }
    details = FoodDetails(label, nutrition)
    assert details.label == label
    assert details.nutrition == nutrition
