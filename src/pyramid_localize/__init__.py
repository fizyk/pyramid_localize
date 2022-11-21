# Copyright (c) 2013-2014 by pyramid_localize authors and contributors <see AUTHORS file>
#
# This module is part of pyramid_localize and is released under
# the MIT License (MIT): http://opensource.org/licenses/MIT
"""pyramid_localize configuration module."""

try:  # pragma: no cover
    import babel
except ImportError:  # pragma: no cover
    babel = False

from pyramid_localize.request import database_locales, locales, locale_id

__version__ = "1.0.2"


def build_localize_config(settings):
    "Build localize settings."
    localize_config = {
        "pybabel": "pybabel",
        "locales": {  # available and default locale for your app
            "available": ["en", "de", "pl"],
            "default": "en",
        },
        "translation": {
            "dirs": [],
        },
    }
    localize_settings = {s: settings[s] for s in settings if s.startswith("localize")}
    for setting_key, setting_value in localize_settings.items():
        if setting_key == "localize.pybabel":
            localize_config["pybabel"] = setting_value
        elif setting_key == "localize.locales.available":
            localize_config["locales"]["available"] = setting_value
        elif setting_key == "localize.locales.default":
            localize_config["locales"]["default"] = setting_value
        elif setting_key == "localize.translation.dirs":
            localize_config["translation"]["dirs"] = setting_value
        elif setting_key == "localize.translation.destination":
            localize_config["translation"]["destination"] = setting_value
        elif setting_key == "localize.domain":
            localize_config["domain"] = setting_value

    return localize_config


def includeme(configurator):
    """pyramid_localize configuration method."""
    # let's check if we have any configuration, or not
    if babel:
        configurator.scan("pyramid_localize.subscribers.i18n")
        localize_config = build_localize_config(configurator.get_settings())
        configurator.registry["localize"] = localize_config
        configurator.include("pyramid_mako")

        configurator.set_locale_negotiator("pyramid_localize.negotiator.locale_negotiator")
        translation_dirs = localize_config["translation"]["dirs"]
        # if it's not a list, lets make it a list.
        # This is to allow creating both single, and list-like config entry
        if not isinstance(translation_dirs, list):
            translation_dirs = [translation_dirs]

        # let's add destination folder to the list
        if "destination" in localize_config["translation"]:
            translation_dirs.append(localize_config["translation"]["destination"])

        configurator.add_translation_dirs(*translation_dirs)
        # let scan all subscribers
        configurator.scan("pyramid_localize.views")

        configurator.add_route(name="localize:index", pattern="catalogue")
        configurator.add_route(name="localize:update", pattern="catalogue/update")
        configurator.add_route(name="localize:compile", pattern="catalogue/compile")
        configurator.add_route(name="localize:reload", pattern="catalogue/reload")

        # getting requests methods
        configurator.add_request_method(database_locales, name="_database_locales", reify=True)
        configurator.add_request_method(locales, name="locales")
        configurator.add_request_method(locale_id, name="locale_id", reify=True)

        # if configured
        return

    # including fake subscribers
    configurator.scan("pyramid_localize.subscribers.fake")
