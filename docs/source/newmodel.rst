Component Creation
===========================

For create a custom component it is required to create a new implementation of the :meth:`AbstractComponent <pytanga.components.AbstractComponent.AbstractComponent>` 

In the __init__ method the class should receive all the desired attributes for the YANG module, and pass then to the setAttributes method that will perform the data validation and construction of the modules attribute schema.

Set the attribute self.tag to the model desired tag, and if required set self._xmlns to the XMLNS with the following syntax:

.. code-block:: python

    self._xmlns = {
        'xmlns' : "http://cisco.com/ns/yang/Cisco-IOS-XE-native" ,
    }

.. warning::

   The NETCONFVisitor only supports three levels of attributes nesting. If you need more than four levels consider building a new module.

Implemantation Example
-----------------------

.. code-block:: python

    from pytanga.components import AbstractComponent


    class testComponent(AbstractComponent):

        def __init__(self, attribute1 , attribute2):
            self._xmlns = {}
            self.attributes = self.setAttributes(attribute1 , attribute2)
            self.parent_xmlns = {}
            self._children: List[AbstractComponent] = []
            self.childrenData = []
            self.tag = 'test'

        @property
        def xmlns(self):
            return self._xmlns

        @xmlns.setter
        def xmlns(self, xmlns):
            self._xmlns = xmlns

        def setAttributes(self, attribute1 , attribute2):
            attributes = {}
            attributes['l1_var1'] = attribute1
            attributes['l1_var2'] = 'var2'
            attributes['l1_var3'] = None
            attributes['l1_var4'] = {
                'keys': {
                    'attr_key' : attribute2
                },
                'value' : 'var4'
            }
            attributes['level2'] = {
                'l2_var1': 'l2_var1',
                'l2_var2': 'l2_var2',
                'l2_var3': None,
                'l2_var4': {
                    'keys': {
                        'testkey': "value"
                    },
                    'value' : 'var4'
                }
            }
            attributes['level3'] = {
                'level3': {
                    'l3_var1': 'l3_var1',
                    'l3_var2' : None,
                    'l3_var3' : {
                        'keys' : {
                            'l3_key' : 'key',
                        },
                        'value' : 'var3'
                    }
                }
            }

            return attributes

        def add(self, component) -> None:
            self._children.append(component)

        def remove(self, component) -> None:
            self._children.remove(component)

        def is_composite(self) -> bool:
            return False

        def getXMLNS(self):
            childrenData = []
            for child in self._children:
                self.parent_xmlns.update(child.getXMLNS())
            return self.parent_xmlns

        def parse(self, serializer):
            self.childrenData = []
            self.getXMLNS()
            for child in self._children:
                self.childrenData.append(child.parse(serializer))
            return serializer.parse(self)

 
Using the new Module
---------------------


.. code-block:: python


    from newmodule import testComponent
    from pytanga.visitors import NETCONFVisitor
    from xml.dom.minidom import parseString

    module = testComponent("Value1" , "Value2")
    serializer = NETCONFVisitor()
    output = module.parse(serializer)
    xml_string = serializer.print(output)
    print(parseString(xml_string).toprettyxml())

Resulting in the following output

.. code-block:: XML

    <test>
        <l1_var1>Value1</l1_var1>
        <l1_var2>var2</l1_var2>
        <l1_var3/>
        <l1_var4 attr_key="Value2">var4</l1_var4>
        <level2>
            <l2_var1>l2_var1</l2_var1>
            <l2_var2>l2_var2</l2_var2>
            <l2_var3/>
            <l2_var4 testkey="value">var4</l2_var4>
        </level2>
        <level3>
            <level3>
                <l3_var1>l3_var1</l3_var1>
                <l3_var2/>
                <l3_var3 l3_key="key">var3</l3_var3>
            </level3>
        </level3>
    </test>

