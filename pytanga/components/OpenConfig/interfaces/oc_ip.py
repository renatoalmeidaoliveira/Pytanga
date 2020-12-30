from pytanga.components import AbstractComponent


class oc_ipComponent(AbstractComponent):

    def __init__(self, version):
        self._xmlns = {}
        self.attributes = {}
        self.parent_xmlns = {
            "xmlns:oc-ip": "http://openconfig.net/yang/interfaces/ip"
        }
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        if(version == 4):
            self.tag = 'oc-ip:ipv4'
        elif(version == 6):
            self.tag = 'oc-ip:ipv6'

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
