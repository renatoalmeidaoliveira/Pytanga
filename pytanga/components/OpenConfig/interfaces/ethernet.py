from pytanga.components import AbstractComponent


class ethernetComponent(AbstractComponent):

    def __init__(self,
                 mac_address=None,
                 auto_negotiate=None,
                 duplex_mode=None,
                 port_speed=None,
                 enable_flow_control=None):
        self.parent_xmlns = {}
        self._xmlns = {
            'xmlns' : 'http://openconfig.net/yang/interfaces/ethernet'
        }
        self._children: List[AbstractComponent] = []
        self.attributes = self.setAttributes(mac_address,
                                             auto_negotiate,
                                             duplex_mode,
                                             port_speed,
                                             enable_flow_control)
        self.tag = 'ethernet'
        self.childrenData = []

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      mac_address,
                      auto_negotiate,
                      duplex_mode,
                      port_speed,
                      enable_flow_control):
        attributes = {}
        attributes['config'] = {}
        if(mac_address):
            attributes['config']['mac-address'] = mac_address
        if(auto_negotiate):
            attributes['config']['auto-negotiate'] = 'true'
        if(duplex_mode):
            attributes['config']['duplex-mode'] = duplex_mode
        if(port_speed):
            attributes['config']['port-speed'] = port_speed
        if(enable_flow_control):
            attributes['config']['enable-flow-control'] = enable_flow_control
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

