"""Common test functions."""
import pytest

# set fake environment variables
mp = pytest.MonkeyPatch()
mp.setenv("EDAMAM_KEY", "FAKE_EDAMAM_KEY")
mp.setenv("EDAMAM_ID", "FAKE_EDAMAM_ID")
