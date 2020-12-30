from pytanga.components import AbstractComponent


class networkComponent(AbstractComponent):

    def __init__(self, network, mask=None, route_map=None, backdoor=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(
            network,
            mask,
            route_map,
            backdoor)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'network'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      network,
                      mask,
                      route_map,
                      backdoor):
        attributes = {}
        data = {}
        if(route_map):
            data['route-map'] = route_map
        if(backdoor):
            data['backdoor'] = None
        data['number'] = network
        if(mask):
            data['mask'] = mask
            attributes['with-mask'] = data
        else:
            attributes['no-mask'] = data
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
