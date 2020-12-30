from pytanga.components import AbstractComponent


class switchedVlanComponent(AbstractComponent):

    def __init__(self,
                 interface_mode=None,
                 native_vlan=None,
                 access_vlan=None,
                 trunk_vlans=None):
        self.parent_xmlns = {
            'xmlns': 'http://openconfig.net/yang/vlan',
        }
        self._xmlns = {}
        self._children: List[AbstractComponent] = []
        self.attributes = self.setAttributes(
                                            interface_mode,
                                            native_vlan,
                                            access_vlan,
                                            trunk_vlans)
        self.tag = 'switched-vlan'
        self.childrenData = []

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      interface_mode,
                      native_vlan,
                      access_vlan,
                      trunk_vlans):
        attributes = {}
        attributes['config'] = {}
        if(interface_mode):
            attributes['config']['interface-mode'] = interface_mode
        if(native_vlan):
            attributes['config']['native-vlan'] = native_vlan
        if(access_vlan):
            attributes['config']['access-vlan'] = access_vlan
        if(trunk_vlans):
            attributes['config']['trunk-vlans'] = trunk_vlans
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

