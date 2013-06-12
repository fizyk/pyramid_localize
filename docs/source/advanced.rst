Advanced
========

Localized URLs
--------------

**pyramid_localize** allows to include locale definition inside routes. In order to utilise this functionality, your request factory, have to inherit :class:`~pyramid_localize.request.LocalizeRequestMixin`, and your routes, you wish to localise should include a _LOCALE_ parameter. You can pass it to route_url, but if you do not, this mixin will set it to current locale, making sure, it's always set. :func:`~pyramid_localize.tools.locale_negotiator` set by pyramid_localize will take route locale in before any other possibility.


.. _web-api:

Web API
-------

Web API is a collection of actions used to work on translations files.

At the moment, it includes loading them into application, creating /updating catalogues for all available translations, compiling, and reloading translations without the need to restart application.

TODO: describe all actions, and routes.
