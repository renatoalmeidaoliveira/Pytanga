from pytanga.components import AbstractComponent


class oc_ipAddressComponent(AbstractComponent):

    def __init__(self,
                 address,
                 prefix_length):
        self._xmlns = {}
        self.attributes = self.setAttributes(address, prefix_length)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'oc-ip:address'

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, address, prefix_length):
        attributes = {
            'oc-ip:ip': address
        }
        attributes['oc-ip:config'] = {
            'oc-ip:ip': address,
            'oc-ip:prefix-length': str(prefix_length)
        }
        return attributes

    def add(self, component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component) -> None:
        self._children.remove(component)
        component.parent = None

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

