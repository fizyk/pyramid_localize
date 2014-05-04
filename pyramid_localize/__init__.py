# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""pyramid_localize configuration module."""

try:  # pragma: no cover
    import babel
except ImportError:  # pragma: no cover
    babel = False

from tzf.pyramid_yml import config_defaults

from pyramid_localize.request import (
    locale, database_locales, locales, locale_id
)

__version__ = '0.1.0'


def includeme(configurator):
    """pyramid_localize configuration method."""
    # let's check if we have any configuration, or not
    if babel:
        configurator.scan('pyramid_localize.subscribers.i18n')
        configuration = configurator.registry.get('config', {}).get('localize')
        if configuration:
            configurator.include('pyramid_mako')
            # once user allowed for localization, lets set up default values!
            config_defaults(configurator, 'pyramid_localize:config')

            configurator.set_locale_negotiator('pyramid_localize.negotiator.locale_negotiator')
            translation_dirs = configuration.translation.dirs
            # if it's not a list, lets make it a list.
            # This is to allow creating both single, and list-like config entry
            if not isinstance(translation_dirs, list):
                translation_dirs = [translation_dirs]

            # let's add destination folder to the list
            if 'destination' in configuration.translation:
                translation_dirs.append(configuration.translation.destination)

            configurator.add_translation_dirs(*translation_dirs)
            # let scan all subscribers
            configurator.scan('pyramid_localize.views')

            configurator.add_route(name='localize:index', pattern='catalogue')
            configurator.add_route(name='localize:update', pattern='catalogue/update')
            configurator.add_route(name='localize:compile', pattern='catalogue/compile')
            configurator.add_route(name='localize:reload', pattern='catalogue/reload')

            # getting requests methods
            configurator.add_request_method(locale, name='locale', reify=True)
            configurator.add_request_method(database_locales, name='_database_locales', reify=True)
            configurator.add_request_method(locales, name='locales')
            configurator.add_request_method(locale_id, name='locale_id', reify=True)

            # if configured
            return

    # including fake subscribers
    configurator.scan('pyramid_localize.subscribers.fake')
