from pytanga.components import AbstractComponent


class addressFamilyVRFComponent(AbstractComponent):

    def __init__(self, with_vrf):
        self._xmlns = {}
        self.attributes = self.setAttributes()
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        if(with_vrf):
            self.tag = 'with-vrf'
        else:
            self.tag = 'no-vrf'
        
    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self):
        attributes = {}
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
