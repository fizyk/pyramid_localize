"""Test suite main conftest."""
import pytest
from mock import Mock
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid import testing


@pytest.fixture
def web_request():
    """Mocked web request for views testing."""
    from pyramid_localize.request import LocalizeRequestMixin
    from pyramid_localize.request import database_locales
    from pyramid_localize.request import locale_id
    from pyramid_localize.request import locales

    class TestRequest(LocalizeRequestMixin, Request):

        @reify
        def _database_locales(self):
            return database_locales(self)

        @reify
        def locale_id(self):
            return locale_id(self)

        def locales(self, *args, **kwargs):
            return locales(self, *args, **kwargs)

    request = TestRequest({})
    config = Mock()
    config.configure_mock(
        **{'localize.locales.available': ['en', 'pl', 'de', 'cz']}
    )
    configurator = testing.setUp()
    request.registry = configurator.registry
    request.registry['config'] = config

    return request


@pytest.fixture
def locale_negotiator_request():
    """Request for locale_negotiator tests."""
    request = Mock()
    mock_configuration = {
        'cookies': {'_LOCALE_': 'cz'},
        '_LOCALE_': 'fr',
        'accept_language.best_match.return_value': 'de',
        'path': '/pl/page'}
    request.configure_mock(**mock_configuration)
    config = Mock()
    config.configure_mock(**{
        'localize.locales.available': ['en', 'pl', 'de', 'cz', 'fr'],
        'localize.locales.default': 'en'
    })
    request.registry = {'config': config}
    return request
