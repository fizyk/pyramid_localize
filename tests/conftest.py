"""Test suite main conftest."""

from typing import Any

import pyramid_basemodel
import pytest
import transaction
from mock import Mock
from pyramid import testing
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid_basemodel import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from zope.sqlalchemy import register

from pyramid_localize import build_localize_config
from pyramid_localize.models import Language
from pyramid_localize.request import LocalizeRequestMixin, database_locales, locale_id, locales


def web_request_func() -> Request:
    """Mock web request for views testing."""

    class TestRequest(LocalizeRequestMixin, Request):  # type: ignore[misc]
        """Test request object."""

        @reify  # type: ignore[untyped-decorator]
        def _database_locales(self) -> dict[str, Language]:
            return database_locales(self)

        @reify  # type: ignore[untyped-decorator]
        def locale_id(self) -> int:
            """Return a database locale id."""
            return locale_id(self)

        def locales(self, *args: Any, **kwargs: Any) -> dict[str, Language]:
            """Return all availablee locales."""
            return locales(self, *args, **kwargs)

    request = TestRequest({})
    localize_config = build_localize_config(
        {
            "localize.locales.available": ["en", "pl", "de", "cz"],
            "localize.domain": "test",
        }
    )
    configurator = testing.setUp()
    request.registry = configurator.registry
    request.registry["localize"] = localize_config

    return request


@pytest.fixture
def web_request() -> Request:
    """Mock web request for views testing."""
    return web_request_func()


@pytest.fixture
def locale_negotiator_request() -> Mock:
    """Request for locale_negotiator tests."""
    request = Mock()
    mock_configuration = {
        "cookies": {"_LOCALE_": "cz"},
        "_LOCALE_": "fr",
        "accept_language.best_match.return_value": "de",
        "path": "/pl/page",
        "registry": {
            "localize": build_localize_config(
                {
                    "localize.locales.available": ["en", "pl", "de", "cz", "fr"],
                    "localize.locales.default": "en",
                }
            )
        },
    }
    request.configure_mock(**mock_configuration)
    return request


@pytest.fixture
def db_session(request: pytest.FixtureRequest) -> scoped_session[Session]:
    """Session for SQLAlchemy."""
    engine = create_engine("sqlite:///localize.sqlite", echo=False, poolclass=NullPool)
    pyramid_basemodel.Session = scoped_session(sessionmaker())
    register(pyramid_basemodel.Session)
    pyramid_basemodel.bind_engine(engine, pyramid_basemodel.Session, should_create=True, should_drop=True)

    def destroy() -> None:
        transaction.commit()
        Base.metadata.drop_all(engine)

    request.addfinalizer(destroy)

    return pyramid_basemodel.Session


@pytest.fixture
def db_locales(db_session: scoped_session[Session]) -> None:
    """Add Languages to db_session."""
    for locale in ["pl", "cz", "fr"]:
        locale_object = Language(name=locale, native_name=locale, language_code=locale)
        db_session.add(locale_object)
    transaction.commit()


@pytest.fixture
def request_i18n() -> Request:
    """Create request with i18n subscribers on."""
    config = testing.setUp()
    config.scan("pyramid_localize.subscribers.i18n")
    request = Request({})
    request.registry = config.registry
    return request


@pytest.fixture
def request_fake() -> Request:
    """Create request with fake i18n subscribers on."""
    config = testing.setUp()
    config.scan("pyramid_localize.subscribers.fake")
    request = Request({})
    request.registry = config.registry
    return request
