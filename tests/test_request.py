"""Test request related code."""

import pytest

import transaction
from pyramid.compat import text_type
import pyramid_basemodel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_localize.models import Language


@pytest.mark.parametrize('kwargs, expected_locale', (
    (  # not filled __LOCALE__ , should return default one
        {'slug': 'some-slug'},
        'en'
    ),
    (  # filled __LOCALE__ within available, returned exact that
        {
            'slug': 'some-slug',
            '__LOCALE__': 'pl'
        },
        'pl'
    ),
    (  # filled __LOCALE__ within one not in available, returned default one
        {
            'slug': 'some-slug',
            '__LOCALE__': 'fr'
        },
        'en'
    ),
))
def test_request(web_request, kwargs, expected_locale):
    """Test whether route-parameters gets filled correctly."""
    route_params = web_request.default_locale(**kwargs)
    assert '__LOCALE__' in route_params
    assert route_params['__LOCALE__'] in web_request.registry['config'].localize.locales.available
    assert route_params['__LOCALE__'] == expected_locale


@pytest.fixture
def db_session(request):
    """SQLAlchemy session."""
    from pyramid_localize.models import Base

    engine = create_engine('sqlite:///fullauth.sqlite', echo=False, poolclass=NullPool)
    pyramid_basemodel.Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
    pyramid_basemodel.bind_engine(engine, pyramid_basemodel.Session, should_drop=True)

    def destroy():
        transaction.commit()
        Base.metadata.drop_all(engine)

    request.addfinalizer(destroy)

    return pyramid_basemodel.Session


@pytest.fixture
def db_locales(db_session):
    """Add Languages to db_session."""
    for locale in ['pl', 'cz', 'fr']:
        locale_object = Language(name=text_type(locale),
                                 native_name=text_type(locale),
                                 language_code=text_type(locale))
        db_session.add(locale_object)
    transaction.commit()


def test_locale_id(db_locales, web_request):
    """Test for creating, and getting loacel id."""
    assert isinstance(web_request.locale_id, int)


def test_locales(db_locales, web_request):
    """test return locales list."""
    assert len(web_request.locales()) == 3


def test_locales_config(db_locales, web_request):
    """
    test return locales list limited by config.

    There's a new locale, so it should create new Language entry.
    """
    assert len(web_request.locales(True)) == 4
