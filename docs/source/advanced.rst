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

Lists of actions per their route names:

* **localize:index** action, lists all configured translation domains, and it's file along with data such as modification date. See :meth:`~pyramid_localize.views.catalog.CatalogView.index`.

* **localize:update** action, updates all .po files from respective .pot's, and if needed initializes them. See :meth:`~pyramid_localize.views.catalog.CatalogView.update_catalog`.

* **localize:compile** action, compiles all .po translation files into .mo used by gettext to serve translations on your site. See :meth:`~pyramid_localize.views.catalog.CatalogView.compile_catalog`.

* **localize:reload** action is more like an example action, but still usable. Reloads translation catalogues for application. See :meth:`~pyramid_localize.views.catalog.CatalogView.reload_catalog`.
