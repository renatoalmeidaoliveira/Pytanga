from pytanga.components import AbstractComponent


class staticComponent(AbstractComponent):

    def __init__(self,
                 prefix,
                 set_tag=None,
                 description=None,
                 operation=None):
        self._xmlns = {}
        if(operation):
            self._xmlns['operation'] = operation
        self.attributes = self.setAttributes(prefix, set_tag, description)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'static'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, prefix, set_tag, description):
        attributes = {
            'prefix': prefix
        }
        attributes['config'] = {}
        attributes['config']['prefix'] = prefix
        if(set_tag):
            attributes['config']['set-tag'] = set_tag
        if(description):
            attributes['config']['description'] = description
        if(attributes['config'] == {}):
            del attributes['config']
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

