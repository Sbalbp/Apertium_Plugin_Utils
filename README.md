Apertium Plugin Utils
=====================

Python modules originally developed to be used with my two plugin projects (for [Pidgin](https://github.com/Sbalbp/Pidgin_Translator_Plugin "Pidgin") and [XChat](https://github.com/Sbalbp/Xchat_Translator_Plugin "XChat")). However, since the module can be used separately to develop new plugins, it has gotten its own repository.

###The module

This module has two parts:

* **apertiumFiles.** Manages the language pair bindings and plugin preferences.

* **apertiumInterfaceAPY.** Used to interact with an [APY](http://wiki.apertium.org/wiki/Apy "APY"). Can be used independently from the apertiumFiles module to make requests to the APY.

###Installing

To install the module run:

* python setup.py install
