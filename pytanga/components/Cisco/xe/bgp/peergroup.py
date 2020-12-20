from pytanga.components import AbstractComponent
from pytanga.components.Cisco.xe.bgp import neighborComponent


class peerGroupComponent(AbstractComponent):

    def __init__(self,
                 name,
                 remote_as=None,
                 cluster_id=None,
                 description=None,
                 disable_connected_check=None,
                 ebgp_multihop=None,
                 password=None,
                 shutdown=None,
                 keepalive_interval=None,
                 holdtime=None,
                 minimum_neighbor_hold=None,
                 ttl_security=None,
                 update_source=None,
                 version=None):
        self._xmlns = {}
        self.attributes = self.setAttributes()
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        neighbor = neighborComponent(name,
                                remote_as,
                                cluster_id,
                                description,
                                disable_connected_check,
                                ebgp_multihop,
                                password,
                                shutdown,
                                keepalive_interval,
                                holdtime,
                                minimum_neighbor_hold,
                                ttl_security,
                                update_source,
                                version)
        self.add(neighbor)
        self.tag = 'peer-group'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self):
        attributes = {}
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

