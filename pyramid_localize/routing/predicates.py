# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Localize route predicate."""

from collections.abc import Callable
from typing import Any

from pyramid.request import Request


def language(field: str) -> Callable[[dict[str, Any], Request], bool]:
    """Create language predicate for given url match field."""

    def predicate(info: dict[str, Any], request: Request) -> bool:
        """Check whether language is one of the defaults."""
        if field in info["match"] and info["match"][field] in request.registry["localize"]["locales"]["available"]:
            return True
        return False

    return predicate


language.__text__ = "language predicate, to determine allowed languages in route"  # type: ignore[attr-defined]  # ty: ignore[unresolved-attribute]
