"""Test suite main conftest."""
import transaction
import pytest
from mock import Mock
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid import testing
from zope.sqlalchemy import register
import pyramid_basemodel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool

from pyramid_localize import build_localize_config
from pyramid_localize.models import Language


def web_request_func():
    """Mock web request for views testing."""
    # pylint:disable=import-outside-toplevel
    from pyramid_localize.request import LocalizeRequestMixin
    from pyramid_localize.request import database_locales
    from pyramid_localize.request import locale_id
    from pyramid_localize.request import locales

    class TestRequest(LocalizeRequestMixin, Request):  # pylint:disable=too-many-ancestors
        """Test request object."""

        @reify
        def _database_locales(self):
            return database_locales(self)

        @reify
        def locale_id(self):
            """Returns a database locale id."""
            return locale_id(self)

        def locales(self, *args, **kwargs):
            """Return all availablee locales."""
            return locales(self, *args, **kwargs)

    request = TestRequest({})
    localize_config = build_localize_config({
        'localize.locales.available': ['en', 'pl', 'de', 'cz'],
        "localize.domain": "test",
    })
    configurator = testing.setUp()
    request.registry = configurator.registry  # pylint:disable=attribute-defined-outside-init
    request.registry['localize'] = localize_config

    return request


@pytest.fixture
def web_request():
    """Mock web request for views testing."""
    return web_request_func()


@pytest.fixture
def locale_negotiator_request():
    """Request for locale_negotiator tests."""
    request = Mock()
    mock_configuration = {
        'cookies': {'_LOCALE_': 'cz'},
        '_LOCALE_': 'fr',
        'accept_language.best_match.return_value': 'de',
        'path': '/pl/page',
        'registry': {
            "localize": build_localize_config({
                'localize.locales.available': ['en', 'pl', 'de', 'cz', 'fr'],
                'localize.locales.default': 'en'
            })
        }
    }
    request.configure_mock(**mock_configuration)
    return request


@pytest.fixture
def db_session(request):
    """Session for SQLAlchemy."""
    from pyramid_localize.models import Base  # pylint:disable=import-outside-toplevel

    engine = create_engine('sqlite:///localize.sqlite', echo=False, poolclass=NullPool)
    pyramid_basemodel.Session = scoped_session(sessionmaker())
    register(pyramid_basemodel.Session)
    pyramid_basemodel.bind_engine(
        engine, pyramid_basemodel.Session, should_create=True, should_drop=True)

    def destroy():
        transaction.commit()
        Base.metadata.drop_all(engine)

    request.addfinalizer(destroy)

    return pyramid_basemodel.Session


@pytest.fixture
def db_locales(db_session):  # pylint:disable=redefined-outer-name
    """Add Languages to db_session."""
    for locale in ['pl', 'cz', 'fr']:
        locale_object = Language(name=locale,
                                 native_name=locale,
                                 language_code=locale)
        db_session.add(locale_object)
    transaction.commit()


@pytest.fixture
def request_i18n():
    """Create request with i18n subscribers on."""
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.i18n')
    request = Request({})
    request.registry = config.registry
    return request


@pytest.fixture
def request_fake():
    """Create request with fake i18n subscribers on."""
    config = testing.setUp()
    config.scan('pyramid_localize.subscribers.fake')
    request = Request({})
    request.registry = config.registry
    return request
