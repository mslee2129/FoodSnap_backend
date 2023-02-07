"""Common test functions."""
from unittest.mock import MagicMock

import pytest

# set fake environment variables
from google.cloud import vision

mp = pytest.MonkeyPatch()
mp.setenv("EDAMAM_KEY", "FAKE_EDAMAM_KEY")
mp.setenv("EDAMAM_ID", "FAKE_EDAMAM_ID")


@pytest.fixture
def mock_vision(monkeypatch):
    mock_vision = MagicMock()
    monkeypatch.setattr(vision, "ImageAnnotatorClient", mock_vision)
    return mock_vision
