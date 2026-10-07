# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Request related code."""

from typing import Any

import pyramid_basemodel
from pyramid.registry import Registry
from pyramid.request import Request

from pyramid_localize.models import Language


class LocalizeRequestMixin:
    """Mixin adding overwriting Request methods."""

    registry: Registry
    locale_name: str

    def default_locale(self, **kw: Any) -> dict[str, Any]:
        """Set up default locale for path kwargs.

        Can be used in custom route_url overwrites.

        :param kwargs kw: list of route parts

        :returns: kw
        """
        if "__LOCALE__" not in kw or kw["__LOCALE__"] not in self.registry["localize"]["locales"]["available"]:
            kw["__LOCALE__"] = self.locale_name

        return kw

    def route_url(self, route_name: str, *elements: Any, **kw: Any) -> str:
        """Overwrite original route_url to handle default locale within route.

        .. note:: see :meth:`pyramid.request.Request.route_url`
        """
        return super().route_url(route_name, *elements, **self.default_locale(**kw))  # type: ignore[misc,no-any-return]


def locale_id(request: Request) -> int:
    """Return database id of a current locale name.

    :returns: database id of a language code needed for translations
    :rtype: int
    """
    if request.locale_name not in request._database_locales:
        _create_locale(request.locale_name, request)

    return request._database_locales[request.locale_name].id  # type: ignore[no-any-return]


def database_locales(request: Request) -> dict[str, Language]:
    """Return all database locales available.

    :returns: dictionary of Language objects language_code: Language
    :rtype: dict
    """
    db_locales: dict[str, Language] = {}
    for language in pyramid_basemodel.Session.query(Language).all():
        db_locales[language.language_code] = language

    return db_locales


def locales(request: Request, *, config: bool = False) -> dict[str, Language]:
    """Return locales.

    :param bool config: Whether to restrict list with config

    :returns: dictionary of Language objects language_code: Language
    :rtype: dict
    """
    if config:
        available_locales: dict[str, Language] = {}
        for available_locale in request.registry["localize"]["locales"]["available"]:
            if available_locale not in request._database_locales:
                _create_locale(available_locale, request)
            available_locales[available_locale] = request._database_locales[available_locale]

        return available_locales

    return request._database_locales  # type: ignore[no-any-return]


def _create_locale(new_locale: str, request: Request) -> None:
    language = Language(name=str(new_locale), native_name=str(new_locale), language_code=str(new_locale))
    pyramid_basemodel.Session.add(language)
    request._database_locales = database_locales(request)
