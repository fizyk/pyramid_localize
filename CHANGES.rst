=======
CHANGES
=======

0.1.0 (prerelease)
------------------
- license information
- requires at least pyramid 1.5a1 (rely on default localizer reify method)
- py3 compatibility (require at least babel 1.0)
- locale negotiator looks first for request attribute _LOCALE_

backward incompatible
+++++++++++++++++++++
- required cookie name changed to _LOCALE_ to be consistent with other places

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
