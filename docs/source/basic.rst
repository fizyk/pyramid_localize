Installation
============

To install pyramid_localize, run:

``pip install pyramid_localize``

or add **pyramid_localize** to your **setup.py** requirements.


Include in your project
-----------------------

Basic usage won't require any additional plugin's configuration. You just include the plugin, and make sure you have a `Babel <http://babel.edgewall.org/>`_ installed in the same environment.

.. code-block:: python

    config.include('pyramid_localize')


pyramid_localize will add translation methos both to request object and for template. All translation configuration would need to be done within You application.

.. note::
    If Babel will not be found, then pyramid_localize will install dummy translation methods, that will do nothing, after getting all the arguments, so You can still create apps, or pyramid plugins using translation functionality.
