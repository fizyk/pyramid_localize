# -*- coding: utf-8 -*-

# Copyright (c) 2013 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT

try:  # pragma: no cover
    import babel
except ImportError:  # pragma: no cover
    babel = False

from tzf.pyramid_yml import config_defaults

from pyramid_localize import tools
from pyramid_localize.request import locale
from pyramid_localize.request import database_locales
from pyramid_localize.request import locales
from pyramid_localize.request import locale_id

__version__ = '0.1a1'


def includeme(configurator):
    '''
        i18n includeme action
    '''

    # TODO: Find a better way to run other stuff than translation methods
    configuration = configurator.registry['config'].get('localize')
    # let's check if we have any configuration, or not
    if babel:
        configurator.scan('pyramid_localize.subscribers.i18n')
        if configuration:
            # once user allowed for localization, lets set up default values!
            config_defaults(configurator, 'pyramid_localize:config')

            configurator.set_locale_negotiator(tools.locale_negotiator)
            translation_dirs = configuration.translation.dirs
            # if it's not a list, lets make it a list. This is to allow creating both single, and list-like config entry
            if not isinstance(translation_dirs, list):
                translation_dirs = [translation_dirs]
            configurator.add_translation_dirs(*translation_dirs)
            # let scan all subscribers
            configurator.scan('pyramid_localize.views')

            configurator.add_route(name='localize:index', pattern='catalog')
            configurator.add_route(name='localize:update', pattern='catalog/update')
            configurator.add_route(name='localize:compile', pattern='catalog/compile')
            configurator.add_route(name='localize:reload', pattern='catalog/reload')

            # getting requests methods
            configurator.add_request_method(locale, name='locale', reify=True)
            configurator.add_request_method(database_locales, name='_database_locales', reify=True)
            configurator.add_request_method(locales, name='locales')
            configurator.add_request_method(locale_id, name='locale_id', reify=True)
    else:
        # including fake subscribers
        configurator.scan('pyramid_localize.subscribers.fake')
