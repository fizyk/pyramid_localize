"""Route predicate related tests."""

import pytest

from pyramid_localize.routing.predicates import language


@pytest.mark.parametrize('match_info, matched', (
    (
        {'match': {'_LOCALE_': 'en'}},
        True
    ), (
        {'match': {'_LOCALE_': 'fr'}},
        False
    ), (
        {'match': {}},
        False
    )
))
def test_predicate(web_request, match_info, matched):
    """Test matches according to web_request config."""
    predicate = language('_LOCALE_')
    assert predicate(match_info, web_request) == matched
