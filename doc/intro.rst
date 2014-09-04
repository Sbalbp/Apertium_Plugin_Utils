Apertium Plugin Utils
*********************

Python modules originally developed to be used with my two plugin projects (for `Pidgin <https://github.com/Sbalbp/Pidgin_Translator_Plugin>`_ and `XChat <https://github.com/Sbalbp/Xchat_Translator_Plugin>`_). However, since the module can be used separately to develop new plugins, it has gotten its own repository.

The module
==========

This module has two parts:

- **apertiumFiles.** Manages the language pair bindings and plugin preferences.
- **apertiumInterfaceAPY.** Used to interact with an `APY <http://wiki.apertium.org/wiki/Apy>`_). Can be used independently from the apertiumFiles module to make requests to the APY.

Installing
==========

You can opt for a global installation with

- sudo python setup.py install

Alternatively, you can install the module to a chosen directory (prefix installation). To do this run the following

- python setup.py install --prefix=route/to/module

don't forget to use your own custom route to install the module there. After that, a new directory tree containing the Python module will be created. You still need to tell Python to look for the module in this new directory, so you will have to add its route to your PYTHONPATH environment variable:

- export PYTHONPATH=route/to/module/lib/pythonX.Y/site-packages:$PYTHONPATH

don't forget to add the whole route up to the site-packages directory (included). You can also edit your .profile/.bash_profile/.login file to add the above line so that the route is added to the PYTHONPATH automatically when you log in (therefore, you won't have to manually edit it every time).

You can refer to this `documentation <https://docs.python.org/2/install/>`_ for other different installing alternatives.
