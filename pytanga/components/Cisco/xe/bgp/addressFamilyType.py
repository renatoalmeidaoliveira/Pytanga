from pytanga.components import AbstractComponent


class addressFamilyTypeSyntaxError(Exception):
    pass


class addressFamilyTypeComponent(AbstractComponent):

    def __init__(self, afi_name, safi_name):
        self._xmlns = {}
        self.attributes = self.setAttributes(safi_name)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        types = {
            'ipv4': ['flowspec', 'mdt', 'multicast', 'mvpn', 'unicast'],
            'ipv6': ['flowspec',  'multicast', 'mvpn', 'unicast'],
            'l2vpn': ['evpn', 'vpls'],
            'link-state': ['link-state'],
            'nsap': ['unicast'],
            'rtfilter': ['unicast'],
            'vpnv4': ['flowspec',  'multicast', 'unicast'],
            'vpnv6': ['flowspec',  'multicast', 'unicast']
        }
        if(afi_name not in types.keys()):
            raise addressFamilyTypeSyntaxError(
                f"afi_name: {afi_name} not allowed. Must be one of {types}")
            if(safi_name not in types[afi_name]):
                raise addressFamilyTypeSyntaxError(
                    f"safi_name: {safi_name} not allowed. Must be one of {types[afi_name]}")
        self.tag = afi_name

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, safi_name):
        attributes = {
            'af-name': safi_name
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
