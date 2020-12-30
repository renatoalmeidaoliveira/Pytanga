import unittest

from pytanga.components import AbstractComponent
from pytanga.visitors import NETCONFVisitor
from pytanga.visitors import VisitorError


class testComponent(AbstractComponent):

    def __init__(self, level4=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(level4)
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

    def setAttributes(self, level4):
        attributes = {}
        attributes['leaf_l1_var1'] = 'var1'
        attributes['leaf_l1_var2'] = None
        attributes['leafList_l1'] = ['l_var1', 'l_var2', 'l_var3']
        attributes['leaf_withKey_l1'] = {
            'keys': {
                'attr_key': "value"
            },
            'value': 'var4'
        }
        attributes['level2'] = {
            'leaf_l2_var1': 'l2_var1',
            'leaf_l2_var2': None,
            'leafList_l2': ['l_var1', 'l_var2', 'l_var3'],
            'leaf_withKey_l2': {
                'keys': {
                    'testkey': "value"
                },
                'value': 'var4'
            }
        }
        attributes['level3'] = {
            'level3': {
                'leaf_l3_var1': 'l3_var1',
                'leaf_l3_var2': None,
                'leafList_l3': ['l_var1', 'l_var2', 'l_var3'],
                'leaf_withKey_l3_var3': {
                    'keys': {
                        'l3_key': 'key',
                    },
                    'value': 'var3'
                }
            }
        }
        if(level4):
            attributes['level1'] = {
                'level2': {
                    'level3': {
                        'level4': {
                            'attr': 'value'
                        }
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


class NETCONFVisitorTest(unittest.TestCase):

    def test_NETCONFVisitor(self):
        Component = testComponent()
        serializer = NETCONFVisitor()
        output = Component.parse(serializer)
        xml_string = serializer.print(output)
        teststring = '<test><leaf_l1_var1>var1</leaf_l1_var1><leaf_l1_var2 /><leafList_l1>l_var1</leafList_l1><leafList_l1>l_var2</leafList_l1><leafList_l1>l_var3</leafList_l1><leaf_withKey_l1 attr_key="value">var4</leaf_withKey_l1><level2><leaf_l2_var1>l2_var1</leaf_l2_var1><leaf_l2_var2 /><leafList_l2>var4</leafList_l2><leafList_l2>var4</leafList_l2><leafList_l2>var4</leafList_l2><leaf_withKey_l2 testkey="value">var4</leaf_withKey_l2></level2><level3><level3><leaf_l3_var1>l3_var1</leaf_l3_var1><leaf_l3_var2 /><leafList_l3>l_var1</leafList_l3><leafList_l3>l_var2</leafList_l3><leafList_l3>l_var3</leafList_l3><leaf_withKey_l3_var3 l3_key="key">var3</leaf_withKey_l3_var3></level3></level3></test>'
        self.assertEqual(xml_string, teststring)

    def test_NETCONFException(self):
        Component = testComponent(level4=True)
        serializer = NETCONFVisitor()
        self.assertRaises(VisitorError, Component.parse, serializer)

