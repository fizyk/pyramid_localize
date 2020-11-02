"""Test request related code."""

import pytest


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
    assert route_params['__LOCALE__'] in web_request.registry["localize"]["locales"]["available"]
    assert route_params['__LOCALE__'] == expected_locale


def test_locale_id(db_locales, web_request):  # pylint:disable=unused-argument
    """Test for creating, and getting loacel id."""
    assert isinstance(web_request.locale_id, int)


def test_locales(db_locales, web_request):  # pylint:disable=unused-argument
    """Test return locales list."""
    assert len(web_request.locales()) == 3


def test_locales_config(db_locales, web_request):  # pylint:disable=unused-argument
    """
    Test return locales list limited by config.

    There's a new locale, so it should create new Language entry.
    """
    assert len(web_request.locales(True)) == 4
