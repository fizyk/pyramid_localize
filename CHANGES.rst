CHANGES
=======

.. towncrier release notes start

1.0.2 (2022-11-21)
==================

Miscellaneus
------------

- Add towncrier to manage CHANGES.rst automatically. (`#193 <https://https://github.com/fizyk/pyramid_localize/issues/193>`_)
- Migrate version bumping tool to tbump (`#403 <https://https://github.com/fizyk/pyramid_localize/issues/403>`_)


unreleased
----------

- [enhancement] Support Python 3.11


1.0.1
-------

- [packaging] use setup.cfg to define package metadata nad options

1.0.0
-------

- [dropped deprecation] removed request.locale in favour of pyramid's request.locale_name
- [breaking] Removed dependency on tzf.pyramid_yml. Now all settings should be
  set in the standard ini file.
- [enhancement] Drop support for python 2
- [dependency] Require pycountry at minimum 18.12.8, due to API change
- [functionality] Language object's name and native_name will filled automatically
  on language creation from pycountry [rmed]

0.1.0
-----

- weaker pyramid_yml requirements. Use ``registry['config']`` instead of ``request.config`` which gets added only when explicitly including tzf.pyramid_yml package.
- deprecated request.locale in favour of request.locale_name delivered by Pyramid 1.5
- moved locale negotiator into it's own submodule

backward incompatible
+++++++++++++++++++++
- required cookie name changed to _LOCALE_ to be consistent with other places
- fixed a typo from catalog to catalogue

tests
+++++
- refactor tests to pytest
- introduced pylama checks for:
    - pep8
    - pyflakes
    - pep257
    - mccabe

- license information
- requires at least pyramid 1.5a1 (rely on default localizer reify method)
- py3 compatibility (require at least babel 1.0)
- locale negotiator looks first for request attribute _LOCALE_
- added pyramid_mako dependency (required by pyramid 1.5a2 changes)

0.0.5
-----
- fixes in catalog/index template [zusel, fizyk]
- destination path added in translation_dirs as a translation source as well [fizyk]

0.0.4
-----
- fix issue with translation files path beeing not related to cwd [fizyk]

0.0.2
-----
- fixed MANIFEST.in [fizyk]

0.0.1
-----
- initial release [fizyk]
