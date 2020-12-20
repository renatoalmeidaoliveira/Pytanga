# Welcome to Pytanga’s documentation!
Pytanga is a Python library that aims to simplify YANG payload creation, its architecture is based on the Composite and Visitor design patterns.

Similar to YANG models where a container can have leaves and other containers, building a part-whole architecture. Pitanga modules define a component with attributes (leaves), and children that represent the inner containers of the module.

For the data output, Pytanga implements a Visitor Pattern that is injected in each component and build the desired output, currently implemented only for NETCONF.

With that architecture, it is possible to define the YANG models’ logic and syntax tests decoupled of the payload generation.

Documentation link: https://pytanga.renatooliveira.eng.br/
