import pytest
from mock import Mock


@pytest.fixture
def web_request():
    """Mocked web request for views testing."""
    request = Mock()
    config = Mock()
    config.configure_mock(
        **{'localize.locales.available': ['en', 'pl', 'de', 'cz']}
    )
    request.configure_mock(
        **{'registry': {'config': config}}
    )

    return request
