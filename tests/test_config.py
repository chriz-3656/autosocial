import os
import pytest
from autosocial.core.config import Settings

def test_settings_default_values():
    settings = Settings()
    assert settings.timezone == "UTC"
    assert settings.default_language == "en"
    assert settings.log_level == "INFO"

def test_settings_env_override():
    os.environ["DEFAULT_BRAND"] = "testbrand"
    settings = Settings()
    assert settings.default_brand == "testbrand"
    del os.environ["DEFAULT_BRAND"]
