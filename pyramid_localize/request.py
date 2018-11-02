# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""Request related code."""

import warnings

from pyramid.compat import text_type
import pyramid_basemodel

from pyramid_localize.models import Language


class LocalizeRequestMixin(object):
    """Mixin adding overwriting Request methods."""

    def default_locale(self, **kw):
        """
        Set up default locale for path kwargs.

        Can be used in custom route_url overwrites.

        :param kwargs kw: list of route parts

        :returns: kw
        """
        if '__LOCALE__' not in kw \
                or kw['__LOCALE__'] not in self.registry['config'].localize.locales.available:
            kw['__LOCALE__'] = self.locale_name

        return kw

    def route_url(self, route_name, *elements, **kw):
        """
        Overwrite original route_url to handle default locale within route.

        .. note:: see :meth:`pyramid.request.Request.route_url`
        """
        return super(LocalizeRequestMixin, self).route_url(
            route_name, *elements, **self.default_locale(**kw)
        )


def locale(request):
    """
    Return locale name.

    .. warning::

        Since pyramid 1.5 this function is obsolete and will be deprecated
        in future versions of pyramid_localize

    When called for the first time, it ask environment for language code,
    which is later available as a pure property
    overriding this method

    :returns: language code needed for translations
    :rtype: string
    """
    warnings.warn(
        'request.locale is deprecated as of pyramid_localize 0.1. '
        'Please use request.locale_name delivered by Pyramid 1.5.',
        DeprecationWarning,
        2
    )
    return request.locale_name


def locale_id(request):
    """
    Return database id of a current locale name.

    :returns: database id of a language code needed for translations
    :rtype: int
    """
    if request.locale_name not in request._database_locales:
        _create_locale(request.locale_name, request)

    return request._database_locales[request.locale_name].id


def database_locales(request):  # pylint:disable=unused-argument
    """
    Return all database locales available.

    :returns: dictionary of Language objects language_code: Language
    :rtype: dict
    """
    db_locales = {}
    for language in pyramid_basemodel.Session.query(Language).all():  # pylint:disable=no-member
        db_locales[language.language_code] = language

    return db_locales


def locales(request, config=False):
    """
    Return locales.

    :param bool config: Whether to restrict list with config

    :returns: dictionary of Language objects language_code: Language
    :rtype: dict
    """
    if config:
        available_locales = {}
        for available_locale in request.registry['config'].localize.locales.available:
            if available_locale not in request._database_locales:
                _create_locale(available_locale, request)
            available_locales[available_locale] = request._database_locales[available_locale]

        return available_locales

    return request._database_locales


def _create_locale(new_locale, request):
    language = Language(name=text_type(new_locale),
                        native_name=text_type(new_locale),
                        language_code=text_type(new_locale))
    pyramid_basemodel.Session.add(language)  # pylint:disable=no-member
    request._database_locales = database_locales(request)
