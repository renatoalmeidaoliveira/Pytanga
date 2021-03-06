from pytanga.components import AbstractComponent


class neighborAdvertiseMapComponent(AbstractComponent):

    def __init__(self , name, exist_map=None, non_exist_map=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(name, exist_map, non_exist_map)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'name'
        
    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, name, exist_map, non_exist_map):
        attributes = {}
        attributes['word'] = name
        if(exist_map):
            attributes['exist-map'] = exist_map
        if(non_exist_map):
            attributes['non-exist-map'] = non_exist_map
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
