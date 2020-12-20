from pytanga.components import AbstractComponent


class ospfComponent(AbstractComponent):

    def __init__(self,
                 process_id,
                 vrf=None,
                 router_id=None,
                 nsr=None,
                 maximum_paths=None,
                 domain_tag=None,
                 ispf=None,
                 prefix_suppression=None,
                 priority=None,
                 shutdown=None,
                 cost=None,
                 flood_reduction=None,
                 hello_interval=None,
                 mtu_ignore=None,
                 resync_timeout=None,
                 retransmit_interval=None,
                 transmit_delay=None
                 ):
        self._xmlns = {
            'xmlns': "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf",
        }
        self.attributes = self.setAttributes(
            process_id,
            vrf,
            router_id,
            nsr,
            maximum_paths,
            domain_tag,
            ispf,
            prefix_suppression,
            priority,
            shutdown,
            cost,
            flood_reduction,
            hello_interval,
            mtu_ignore,
            resync_timeout,
            retransmit_interval,
            transmit_delay
        )
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'ospf'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      process_id,
                      vrf,
                      router_id,
                      nsr,
                      maximum_paths,
                      domain_tag,
                      ispf,
                      prefix_suppression,
                      priority,
                      shutdown,
                      cost,
                      flood_reduction,
                      hello_interval,
                      mtu_ignore,
                      resync_timeout,
                      retransmit_interval,
                      transmit_delay):
        attributes = {}
        if(process_id):
            attributes['id'] = str(process_id)
        if(vrf):
            attributes['vrf'] = vrf
        if(router_id):
            attributes['router-id'] = router_id
        if(nsr):
            attributes['nsr'] = None
        if(maximum_paths):
            attributes['maximum-paths'] = str(maximum_paths)
        if(domain_tag):
            attributes['domain-tag'] = str(domain_tag)
        if(ispf):
            attributes['ispf'] = None
        if(prefix_suppression):
            attributes['prefix-suppression'] = None
        if(priority):
            attributes['priority'] = str(priority)
        if(shutdown):
            attributes['shutdown'] = 'true'
        if(cost):
            attributes['cost'] = str(cost)
        if(flood_reduction):
            attributes['flood-reduction'] = None
        if(hello_interval):
            attributes['hello-interval'] = str(hello_interval)
        if(mtu_ignore):
            attributes['mtu-ignore'] = str(mtu_ignore)
        if(resync_timeout):
            attributes['resync-timeout'] = str(resync_timeout)
        if(retransmit_interval):
            attributes['retransmit-interval'] = str(retransmit_interval)
        if(transmit_delay):
            attributes['transmit-delay'] = transmit_delay

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

