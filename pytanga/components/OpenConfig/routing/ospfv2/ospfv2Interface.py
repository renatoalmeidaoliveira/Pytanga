from pytanga.components import AbstractComponent


class ospfv2InterfaceComponent(AbstractComponent):

    def __init__(
            self,
            if_id,
            network_type=None,
            priority=None,
            multi_area_adjacency_primary=None,
            authentication_type=None,
            metric=None,
            passive=None,
            hide_network=None):

        self._xmlns = {}
        self.attributes = self.setAttributes(if_id, network_type, priority, multi_area_adjacency_primary, authentication_type, metric, passive, hide_network)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'interface'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, if_id, network_type, priority, multi_area_adjacency_primary, authentication_type, metric, passive, hide_network):
        atributes = {
            'id' : if_id
        }
        atributes['config'] = {}
        if(network_type):
            attributes['config']['network-type'] = {
                'keys' : {
                    'xmlns:oc-ospf-types' : 'http://openconfig.net/yang/ospf-types'
                },
                'value' : f"oc-ospf-types:{network_type}"
            }
        if(priority):
            atributes['config']['priority'] = priority
        if(multi_area_adjacency_primary):
            atributes['config']['multi-area-adjacency-primary'] = multi_area_adjacency_primary
        if(authentication_type):
            atributes['config']['authentication-type'] = authentication_type
        if(metric):
            atributes['config']['metric'] = metric
        if(passive):
            atributes['config']['passive'] = passive
        if(hide_network):
            atributes['config']['hide-network'] = hide_network
        if(atributes['config'] == {}):
            del atributes['config']
        return atributes


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

