# -*- coding: utf-8 -*-
'''
    methods in this module are tools, thank to which pyramid_localize works most of its magic
'''
import sys
import os
import logging

from translationstring import _interp_regex
from pyramid.i18n import get_localizer
from pyramid.i18n import make_localizer
from pyramid.i18n import TranslationString
from pyramid.asset import resolve_asset_spec
from pyramid.path import package_path
from pyramid.httpexceptions import HTTPNotFound
from pyramid.interfaces import ILocalizer
from pyramid.interfaces import ITranslationDirectories
from pyramid.compat import text_type

logger = logging.getLogger(__name__)


def set_localizer(request, reset=False):
    '''
        Sets localizer and auto_translate methods for request

        :param pyramid.request.Request request: request object
        :param bool reset: flag that directs resetting localizer within app
    '''

    if reset:

        request.localizer = None
        for locale in request.config.localize.locales.available:
            logger.debug('Resetting {0} localizator'.format(locale))
            tdirs = request.registry.queryUtility(ITranslationDirectories,
                                                  default=[])
            localizer = make_localizer(locale, tdirs)
            request.registry.registerUtility(localizer, ILocalizer,
                                             name=locale)

    localizer = get_localizer(request)

    def auto_translate(*args, **kwargs):
        # lets pass default domain, so we don't have to determine it with
        # each _() function in apps.
        if len(args) <= 1 and not 'domain' in kwargs:
            kwargs['domain'] = request.config.localize.domain

        # unlike in examples we use TranslationString, to make sure we always
        # use appropriate domain
        return localizer.translate(TranslationString(*args, **kwargs))

    request.localizer = localizer
    request._ = auto_translate


def locale_negotiator(request):
    '''
        Locale negotiator. It sets best suited locale variable for given user:

        1. Tries the address url first, if the first part has locale indicator.
        2. It checks cookies, for value set here
        3. Tries to best match accepted language for browser user is visiting website with
        4. Defaults to en

        :param pyramid.request.Request request: a request object
        :returns: locale name
        :rtype: str

    '''
    available_languages = request.config.localize.locales.available
    locale = request.config.localize.locales.default
    # We do not have a matchdict present at the moment, lets get our own split
    # (request.path is always a /, so we'll get two elements)
    route_elements = request.path.split('/')
    # we check if route_element[1] is a locale indicator for path
    if len(route_elements[1]) == 2 and route_elements[1] in available_languages:
        locale = route_elements[1]
        # TODO: Code below is a wish,. After detecting locale on url, remove it and progress with standard url name
        # route_elements.remove(locale)
        # request.set_property(lambda request: '/'.join(route_elements), name='path', reify=True)
    elif request.cookies and 'lang' in request.cookies and\
            request.cookies['lang'] in available_languages:
        locale = request.cookies['lang']
    elif request.accept_language:
        locale = request.accept_language.best_match(available_languages)

    return locale


def destination_path(request):
    '''
        Returns absolute path of the translation destination

        :param pyramid.request.Request request: a request object

        :returns: A combined translation destination path
        :rtype: str
    '''
    package_name, filename = resolve_asset_spec(request.config.localize.translation.destination)

    if package_name is None:  # absolute filename
        directory = filename
    else:
        __import__(package_name)
        package = sys.modules[package_name]
        directory = os.path.join(package_path(package), filename)
    return directory


def dummy_autotranslate(msgid, domain=None, default=None, mapping=None):
    '''
        Method that simulate autotranslate

        :param str msgid: Message or message id
        :param str domain: Translation domain
        :param str default: Default message
        :param dict mapping: Mapping dictionary for message variables

        :returns: *translated* string
        :rtype: str

    '''
    # Try to return defaults first:
    tstr = None
    if default:
        tstr = default
    else:
        tstr = msgid

    if mapping and tstr:
        def replace(match):
            whole, param1, param2 = match.groups()
            return text_type(mapping.get(param1 or param2, whole))
        tstr = _interp_regex.sub(replace, tstr)

    return tstr
