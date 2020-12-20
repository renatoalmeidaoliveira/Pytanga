from pytanga.components import AbstractComponent

class neighborPrefixListComponent(AbstractComponent):

    def __init__(self , inout , name ):
        self._xmlns = {}
        self.attributes = self.setAttributes(inout, name)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'prefix-list'
        

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, inout , name):
        attributes = {
            'inout' : inout,
            'prefix-list-name' : name
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

