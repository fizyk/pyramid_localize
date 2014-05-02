import pytest
from mock import Mock
from pyramid.decorator import reify


@pytest.fixture
def web_request():
    """Mocked web request for views testing."""

    from pyramid_localize.request import LocalizeRequestMixin
    from pyramid_localize.request import locale
    from pyramid_localize.request import database_locales
    from pyramid_localize.request import locale_id
    from pyramid_localize.request import locales

    class TestRequest(LocalizeRequestMixin, Mock):

        @reify
        def locale(self):
            return locale(self)

        @reify
        def _database_locales(self):
            return database_locales(self)

        @reify
        def locale_id(self):
            return locale_id(self)

        def locales(self, *args, **kwargs):
            return locales(self, *args, **kwargs)

    request = TestRequest()
    config = Mock()
    config.configure_mock(
        **{'localize.locales.available': ['en', 'pl', 'de', 'cz']}
    )
    request.configure_mock(
        **{
            'registry': {'config': config},
            'locale_name': 'en'
        }
    )

    return request
