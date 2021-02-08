# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Locale negotiator."""


def locale_negotiator(request):
    """
    Locale negotiator.

    It sets best suited locale variable for given user:

    1. Check for presence and value of **request._LOCALE_** value
    2. Then tries the address url, if the first part has locale indicator.
    3. It checks cookies, for value set here
    4. Tries to best match accepted language for browser user is visiting
        website with
    5. Defaults to **localize.locales.default** configuration setting value

    :param pyramid.request.Request request: a request object
    :returns: locale name
    :rtype: str
    """
    available_languages = request.registry["localize"]["locales"]["available"]
    locale = request.registry["localize"]["locales"]["default"]
    # We do not have a matchdict present at the moment, lets get our own split
    # (request.path is always a /, so we'll get two elements)
    route_elements = request.path.split("/")
    if hasattr(request, "_LOCALE_") and request._LOCALE_ in available_languages:
        locale = request._LOCALE_
    # we check if route_element[1] is a locale indicator for path
    elif len(route_elements[1]) == 2 and route_elements[1] in available_languages:
        locale = route_elements[1]
    elif request.cookies and "_LOCALE_" in request.cookies and request.cookies["_LOCALE_"] in available_languages:
        locale = request.cookies["_LOCALE_"]
    elif request.accept_language:
        locale = request.accept_language.best_match(available_languages)

    return locale
