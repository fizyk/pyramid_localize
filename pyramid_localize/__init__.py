# -*- coding: utf-8 -*-

from tzf.pyramid_yml import config_defaults

from pyramid_localize import tools
from pyramid_localize.request import locale
from pyramid_localize.request import database_locales
from pyramid_localize.request import locales
from pyramid_localize.request import locale_id

__version__ = '0.0.1'


def includeme(configurator):
    '''
        i18n includeme action
    '''
    config_defaults(configurator, 'pyramid_localize:config')

    configuration = configurator.registry['config'].get('localize')
    # let's check if we have any configuration, or not
    if configuration:
        app_domain = configuration
        configurator.set_locale_negotiator(tools.locale_negotiator)
        translation_dirs = configuration.translation.dirs
        # if it's not a list, lets make it a list. This is to allow creating both single, and list-like config entry
        if not isinstance(translation_dirs, list):
            translation_dirs = [translation_dirs]
        configurator.add_translation_dirs(*translation_dirs)
        # let scan all subscribers
        configurator.scan('pyramid_localize.subscribers')
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
        # TODO: if no configuration is passed, let's emit a warning in logs?
        pass
