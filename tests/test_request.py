import pytest

import transaction
from pyramid.compat import text_type
import pyramid_basemodel
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from zope.sqlalchemy import ZopeTransactionExtension

from pyramid_localize.models import Language
from pyramid_localize.request import locale_id
from pyramid_localize.request import locales


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
    route_parameters = web_request.default_locale(**kwargs)
    assert '__LOCALE__' in route_parameters
    assert route_parameters['__LOCALE__'] in web_request.registry['config'].localize.locales.available
    assert route_parameters['__LOCALE__'] == expected_locale


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

    for locale in ['pl', 'cz', 'fr']:
        locale_object = Language(name=text_type(locale),
                                 native_name=text_type(locale),
                                 language_code=text_type(locale))
        db_session.add(locale_object)
    transaction.commit()


def test_locale_id(db_locales, web_request):
    '''Test for creating, and getting loacel id'''
    lid = locale_id(web_request)
    assert isinstance(lid, int)


def test_locales(db_locales, web_request):
    '''test return locales list'''
    locales_list = locales(web_request)
    assert len(locales_list) == 3


def test_locales_config(db_locales, web_request):
    '''test return locales list limited by config'''
    locales_list = locales(web_request, True)
    assert 4 == len(locales_list)
