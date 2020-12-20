from pytanga.components import AbstractComponent

class interfaceComponent(AbstractComponent):


    IETF_INTERFACE_TYPES = {
        "loopback": "ianaift:softwareLoopback",
        "ethernet": "ianaift:ethernetCsmacd"
    }       

    def __init__(self, name , if_type, if_description=None, if_mtu=None , enabled=None):
        self.parent_xmlns = {}
        self._xmlns = {}
        self._children: List[AbstractComponent] = []
        self.attributes = self.setAttributes( name , if_type, if_description, if_mtu , enabled)
        self.tag = 'interface'
        self.childrenData = []



    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, name , if_type, if_description, if_mtu , enabled):
        attributes = {
            'name' : name
        }
        attributes['config'] = {}
        if(if_description):
            attributes['config']['description'] = if_description
        if(if_mtu):
            attributes['config']['mtu'] = str(if_mtu)
        if(enabled):
            attributes['config']['enabled'] = 'true'
        typeConf = {}
        if( if_type ):
            typeConf = {
                'keys' : {
                    'xmlns:ianaift' : 'urn:ietf:params:xml:ns:yang:iana-if-type'
                    },
                'value': self.IETF_INTERFACE_TYPES[if_type]
            }
            attributes['config']['type'] = typeConf
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

