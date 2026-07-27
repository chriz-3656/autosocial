import pytest
from unittest.mock import patch, MagicMock

from autosocial.models.post import PostConfig, MediaItem
from autosocial.publishers.instagrapi_publisher import InstagrapiPublisher

@pytest.fixture
def mock_instagrapi_client():
    with patch("autosocial.publishers.instagrapi_publisher.Client") as MockClient:
        mock_instance = MockClient.return_value
        yield mock_instance

def test_login_success(mock_instagrapi_client):
    publisher = InstagrapiPublisher()
    
    # Mock successful login
    mock_instagrapi_client.login.return_value = True
    
    result = publisher.login("test_user", "test_pass")
    
    assert result is True
    mock_instagrapi_client.login.assert_called_once_with("test_user", "test_pass")

def test_login_with_session(mock_instagrapi_client):
    publisher = InstagrapiPublisher()
    session_data = {"cookies": "test"}
    
    result = publisher.login("test_user", "test_pass", session_data)
    
    assert result is True
    mock_instagrapi_client.set_settings.assert_called_once_with(session_data)
    mock_instagrapi_client.login.assert_called_once_with("test_user", "test_pass")

def test_publish_photo_post(mock_instagrapi_client):
    publisher = InstagrapiPublisher()
    
    config = PostConfig(
        caption="Hello world",
        media=[MediaItem(path="/tmp/photo.jpg", media_type="photo")]
    )
    
    mock_media = MagicMock()
    mock_media.pk = "12345"
    mock_instagrapi_client.photo_upload.return_value = mock_media
    
    result = publisher.publish_post(config)
    
    assert result.success is True
    assert result.media_id == "12345"
    mock_instagrapi_client.photo_upload.assert_called_once_with("/tmp/photo.jpg", "Hello world")
