from pytanga.components import AbstractComponent

class nexthopComponent(AbstractComponent):

    def __init__(self, index, next_hop=None, metric=None, recurse=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(index, next_hop, metric, recurse)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'next-hop'


    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, index, next_hop, metric, recurse):
        attributes = {
            'index' : index,
        }
        attributes['config'] = {}
        attributes['config']['index'] = index
        if(next_hop):
            attributes['config']['next-hop'] = next_hop
        if(metric):
            attributes['config']['metric'] = metric
        if(recurse):
            attributes['config']['recurse'] = recurse
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
        for child in  self._children:
            self.childrenData.append(child.parse(serializer))
        return serializer.parse(self)
