"""Test request related code."""

from typing import Any

import pytest
from pyramid.request import Request


@pytest.mark.parametrize(
    "kwargs, expected_locale",
    (
        (  # not filled __LOCALE__ , should return default one
            {"slug": "some-slug"},
            "en",
        ),
        (  # filled __LOCALE__ within available, returned exact that
            {"slug": "some-slug", "__LOCALE__": "pl"},
            "pl",
        ),
        (  # filled __LOCALE__ within one not in available, returned default one
            {"slug": "some-slug", "__LOCALE__": "fr"},
            "en",
        ),
    ),
)
def test_request(web_request: Request, kwargs: dict[str, Any], expected_locale: str) -> None:
    """Test whether route-parameters gets filled correctly."""
    route_params = web_request.default_locale(**kwargs)
    assert "__LOCALE__" in route_params
    assert route_params["__LOCALE__"] in web_request.registry["localize"]["locales"]["available"]
    assert route_params["__LOCALE__"] == expected_locale


def test_locale_id(db_locales: None, web_request: Request) -> None:
    """Test for creating, and getting loacel id."""
    assert isinstance(web_request.locale_id, int)


def test_locales(db_locales: None, web_request: Request) -> None:
    """Test return locales list."""
    assert len(web_request.locales()) == 3  # noqa: PLR2004


def test_locales_config(db_locales: None, web_request: Request) -> None:
    """Test return locales list limited by config.

    There's a new locale, so it should create new Language entry.
    """
    assert len(web_request.locales(config=True)) == 4  # noqa: PLR2004
