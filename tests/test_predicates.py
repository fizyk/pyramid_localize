"""Route predicate related tests."""

from typing import Any

import pytest
from pyramid.request import Request

from pyramid_localize.routing.predicates import language


@pytest.mark.parametrize(
    "match_info, matched",
    (
        ({"match": {"_LOCALE_": "en"}}, True),
        ({"match": {"_LOCALE_": "fr"}}, False),
        ({"match": {}}, False),
    ),
)
def test_predicate(web_request: Request, match_info: dict[str, Any], matched: bool) -> None:  # noqa: FBT001
    """Test matches according to web_request config."""
    predicate = language("_LOCALE_")
    assert predicate(match_info, web_request) == matched
