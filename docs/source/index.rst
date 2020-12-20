.. Pytanga documentation master file, created by
   sphinx-quickstart on Sat Dec 19 16:18:29 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pytanga's documentation!
===================================

        Pytanga is a Python library that aims to simplify YANG payload creation, its architecture is based on the Composite and Visitor design patterns.

        Similar to YANG models where a container can have leaves and other containers, building a part-whole architecture. Pitanga modules define a component with attributes (leaves), and children that represent the inner containers of the module.

        For the data output, Pytanga implements a Visitor Pattern that is injected in each component and build the desired output, currently implemented only for NETCONF.

        With that architecture, it is possible to define the YANG models' logic and syntax tests decoupled of the payload generation.


.. toctree::
   :caption: MODULES:
   :maxdepth: 2
   :glob:

   _modules/pytanga.components
   _modules/pytanga.helpers
   _modules/pytanga.visitors

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
