# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Localize route predicate."""


def language(field):
    """Create language predicate for given url match field."""

    def predicate(info, request):
        """Check whether language is one of the defaults."""
        if field in info["match"] and info["match"][field] in request.registry["localize"]["locales"]["available"]:
            return True
        return False

    return predicate


language.__text__ = "language predicate, to determine allowed languages in route"
