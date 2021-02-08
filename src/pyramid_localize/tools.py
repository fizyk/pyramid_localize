# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""methods in this module are tools, thank to which pyramid_localize works most of its magic."""

import sys
import os
import logging

from translationstring import _interp_regex
from pyramid.i18n import make_localizer
from pyramid.i18n import TranslationString
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.interfaces import ILocalizer
from pyramid.interfaces import ITranslationDirectories

log = logging.getLogger(__name__)


def set_localizer(request, reset=False):
    """
    Set localizer and auto_translate methods for request.

    :param pyramid.request.Request request: request object
    :param bool reset: flag that directs resetting localizer within app
    """
    if reset:

        for locale in request.registry["localize"]["locales"]["available"]:
            log.debug("Resetting %s localizator", locale)
            tdirs = request.registry.queryUtility(ITranslationDirectories, default=[])
            localizer = make_localizer(locale, tdirs)
            request.registry.registerUtility(localizer, ILocalizer, name=locale)

    def auto_translate(*args, **kwargs):
        # lets pass default domain, so we don't have to determine it with
        # each _() function in apps.
        if len(args) <= 1 and "domain" not in kwargs:
            kwargs["domain"] = request.registry["localize"]["domain"]

        # unlike in examples we use TranslationString, to make sure we always
        # use appropriate domain
        return request.localizer.translate(TranslationString(*args, **kwargs))

    request._ = auto_translate


def destination_path(request):
    """
    Return absolute path of the translation destination.

    :param pyramid.request.Request request: a request object

    :returns: A combined translation destination path
    :rtype: str
    """
    package_name, filename = resolve_asset_spec(request.registry["localize"]["translation"]["destination"])

    if package_name is None:  # absolute filename
        directory = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        directory = os.path.join(package_path(package), filename)
    return directory


def dummy_autotranslate(msgid, domain=None, default=None, mapping=None):  # pylint:disable=unused-argument
    """
    Simulate autotranslate.

    :param str msgid: Message or message id
    :param str domain: Translation domain
    :param str default: Default message
    :param dict mapping: Mapping dictionary for message variables

    :returns: *translated* string
    :rtype: str
    """
    # Try to return defaults first:
    tstr = None
    if default:
        tstr = default
    else:
        tstr = msgid

    if mapping and tstr:

        def replace(match):
            whole, param1, param2 = match.groups()
            return str(mapping.get(param1 or param2, whole))

        tstr = _interp_regex.sub(replace, tstr)

    return tstr
