Basic usage
===========

Installation
------------

To install pyramid_localize, run:

``pip install pyramid_localize``

or add **pyramid_localize** to your **setup.py** requirements.


Include in your project
-----------------------

To use this plugin, simply include it into your configurator object:

.. code-block:: python

    config.include('pyramid_localize')

pyramid_localize will add translation methods both to request object and for template.

Using without configuration
---------------------------

Basic usage won't require any additional plugin's configuration. You just include the plugin, and make sure you have a `Babel <http://babel.edgewall.org/>`_ installed in the same environment. You can either install *babel* on your own, or add dependency to **pyramid_localize[babel]**. This is introduced, to allow creating code, that both works with translations and without, see :ref:`fake-translations`.

However in this case, all translation configuration would need to be done within Your application, as described in chapter `Internationalization and Localization <http://docs.pylonsproject.org/projects/pyramid/en/1.4-branch/narr/i18n.html>`_ of pyramid's documentation.

Configuration
-------------

.. note::
    Plugins uses `tzf.pyramid_yml <https://tzfpyramid_yml.readthedocs.org/en/latest/>`_ for its configuration settings

This is full usage example, where **pyramid_localize** provides everything needed for your application, including :func:`~pyramid_localize.tools.locale_negotiator`, and sqlalchemy model for :class:`~pyramid_localize.models.Language`, to be able to store localized data in database.

.. code-block:: yaml

    localize:
        pybabel: pybabel # pybabel's bin localisation. Used to call compile and extract commands
        domain: APP_DOMAIN  # your application domain name
        locales:    # available and default locale for your app
            available: [en, de, pl]
            default: en
        translation:
            # directory, where translatons can be found, might be a list,
            # defaults to empty list
            dirs: 'roots.app:resources/locale'
            # destination, where .po and .mo files will be created
            # can be same format as pyramid's asset path,
            # it's also added to dirs, as translation source
            destination: 'app:resources/locale'
            # sources, where translations can be found domain: localisation
            # can be same format as pyramid's asset path
            sources:
                APP_DOMAIN: 'app:resources/locale/'
                PACKAGE: 'package.subpackage:resources/locale/'

Having configured this, your app, and all subpackages will be fully localized, you'll also have the ability to automatically reload translations without having to restart application. See :ref:`web-api`.


.. _fake-translations:

Fake translation support
------------------------

In order to be able to allow application creation, that will be usable with translated applications, and  those without translations, pyramid_localize has simple switch, which detects presence of babel.

If Babel will not be found, then pyramid_localize will install dummy translation methods, that will do nothing, except placing translation string args in place, after getting all the arguments, so You can still create apps, or pyramid plugins using translation functionality.

Code behind that can be seen here :func:`pyramid_localize.tools.dummy_autotranslate`.



