from pytanga.components import AbstractComponent

class subinterfaceComponent(AbstractComponent):

    def __init__(self, index, description=None):
        self.parent_xmlns = {}
        self._xmlns = {}
        self._children: List[AbstractComponent] = []
        self.attributes = self.setAttributes( index , description )
        self.tag = 'subinterface'
        self.childrenData = []



    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, index, description):
        attributes = {
            'index' : str(index)
        }
        if(description):
            attributes['config'] = {
                'description' : description
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
        for child in  self._children:
            self.childrenData.append(child.parse(serializer))
        return serializer.parse(self)

