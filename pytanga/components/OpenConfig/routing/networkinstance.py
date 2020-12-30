from pytanga.components import AbstractComponent


class networkInstanceComponent(AbstractComponent):

    def __init__(self,
                 name='default',
                 net_type=None,
                 enabled=None,
                 description=None,
                 router_id=None,
                 route_distinguisher=None):
        self._xmlns = {}
        self.attributes = {}
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.attributes = self.setAttributes(name,
                                             net_type,
                                             enabled,
                                             description,
                                             router_id,
                                             route_distinguisher)
        self.childrenData = []
        self.tag = 'network-instance'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      name,
                      net_type,
                      enabled,
                      description,
                      router_id,
                      route_distinguisher):
        attributes = {
            'name': name
        }
        attributes['config'] = {}
        if(net_type):
            attributes['config']['type'] = net_type
        if(enabled):
            attributes['config']['enabled'] = 'true'
        if(description):
            attributes['config']['description'] = description
        if(router_id):
            attributes['config']['router-id'] = router_id
        if(route_distinguisher):
            attributes['config']['route-distinguisher'] = route_distinguisher
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

