from pytanga.components import AbstractComponent


class oc_ipAddressesComponent(AbstractComponent):

    def __init__(self):
        self._xmlns = {}
        self.attributes = {}
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'oc-ip:addresses'

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

