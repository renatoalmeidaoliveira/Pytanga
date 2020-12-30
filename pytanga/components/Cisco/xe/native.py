from pytanga.components import AbstractComponent


class nativeComponent(AbstractComponent):

    def __init__(self):
        self._xmlns = {
            'xmlns': "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
        }
        self.attributes = {}
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'native'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def add(self, component) -> None:
        self._children.append(component)

    def remove(self, component) -> None:
        self._children.remove(component)

    def is_composite(self) -> bool:
        return False

    def getXMLNS(self):
        childrenData = []
        for child in self._children:
            self._xmlns.update(child.getXMLNS())
        return self._xmlns

    def parse(self, serializer):
        self.childrenData = []
        self.getXMLNS()
        for child in  self._children:
            self.childrenData.append(child.parse(serializer))
        return serializer.parse(self)
