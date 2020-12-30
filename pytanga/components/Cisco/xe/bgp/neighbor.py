from pytanga.components import AbstractComponent
import re


class neighborSyntaxError(Exception):
    pass


class neighborComponent(AbstractComponent):

    def __init__(self,
                 address=None,
                 name=None,
                 remote_as=None,
                 cluster_id=None,
                 description=None,
                 disable_connected_check=None,
                 ebgp_multihop=None,
                 password=None,
                 peer_group=None,
                 shutdown=None,
                 keepalive_interval=None,
                 holdtime=None,
                 minimum_neighbor_hold=None,
                 ttl_security=None,
                 update_source=None,
                 version=None,
                 activate=None,
                 advertisement_interval=None,
                 allow_policy=None,
                 allowas_in=None,
                 default_originate=None,
                 default_originate_route_map=None,
                 dmzlink_bw=None,
                 maximum_prefix_n=None,
                 maximum_prefix_threshold=None,
                 maximum_prefix_restart=None,
                 maximum_prefix_warning=None,
                 next_hop_self=None,
                 next_hop_self_all=None,
                 next_hop_unchanged=None,
                 route_reflector_client=None,
                 send_community=None,
                 send_label=None,
                 soft_reconfiguration=None,
                 weight=None

                 ):
        self._xmlns = {}
        self.attributes = self.setAttributes(
            address,
            name,
            remote_as,
            cluster_id,
            description,
            disable_connected_check,
            ebgp_multihop,
            password,
            peer_group,
            shutdown,
            keepalive_interval,
            holdtime,
            minimum_neighbor_hold,
            ttl_security,
            update_source,
            version,
            activate,
            advertisement_interval,
            allow_policy,
            allowas_in,
            default_originate,
            default_originate_route_map,
            dmzlink_bw,
            maximum_prefix_n,
            maximum_prefix_threshold,
            maximum_prefix_restart,
            maximum_prefix_warning,
            next_hop_self,
            next_hop_self_all,
            next_hop_unchanged,
            route_reflector_client,
            send_community,
            send_label,
            soft_reconfiguration,
            weight
        )
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'neighbor'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      address,
                      name,
                      remote_as,
                      cluster_id,
                      description,
                      disable_connected_check,
                      ebgp_multihop,
                      password,
                      peer_group,
                      shutdown,
                      keepalive_interval,
                      holdtime,
                      minimum_neighbor_hold,
                      ttl_security,
                      update_source,
                      version,
                      activate,
                      advertisement_interval,
                      allow_policy,
                      allowas_in,
                      default_originate,
                      default_originate_route_map,
                      dmzlink_bw,
                      maximum_prefix_n,
                      maximum_prefix_threshold,
                      maximum_prefix_restart,
                      maximum_prefix_warning,
                      next_hop_self,
                      next_hop_self_all,
                      next_hop_unchanged,
                      route_reflector_client,
                      send_community,
                      send_label,
                      soft_reconfiguration,
                      weight
                      ):
        attributes = {}
        if(not ((address and not name) or (not address and name))):
            if((address in None and name is None)):
                raise neighborSyntaxError(
                      "name or address must be defined")
            else:
                raise neighborSyntaxError(
                      "name and address can't be defined together")
        if(address):
            attributes['id'] = address
        if(name):
            attributes['id'] = name
            attributes['peer-group'] = None
            if(peer_group):
                raise neighborSyntaxError("Incorrect peer-group attribuition")
        if(remote_as):
            attributes['remote-as'] = remote_as
        if(cluster_id):
            attributes['cluster-id'] = cluster_id
        if(description):
            attributes['description'] = description
        if(disable_connected_check):
            attributes['disable-connected-check'] = None
        if(ebgp_multihop):
            attributes['ebgp-multihop'] = {'max-hop': ebgp_multihop}
        if(password):
            attributes['password'] = {'text': password}
        if(peer_group):
            attributes['peer-group'] = {'peer-group-name': peer_group}
        if(shutdown):
            attributes['shutdown'] = None
        attributes['timers'] = {}
        if(keepalive_interval):
            attributes['timers']['keepalive-interval'] = keepalive_interval
        if(holdtime):
            attributes['timers']['holdtime'] = holdtime
        if(minimum_neighbor_hold):
            attributes['timers']['minimum-neighbor-hold'] = minimum_neighbor_hold
        if(attributes['timers'] == {}):
            del attributes['timers']
        if(ttl_security):
            attributes['ttl-security'] = {'hops': ttl_security}
        if(update_source):
            p1 = re.compile(r'(?P<type>\D+)(?P<number>.*)')
            m = p1.match(update_source)
            if_type = m.groupdict()['type']
            if_number = m.groupdict()['number']
            attributes['update-source'] = {}
            attributes['update-source'][if_type] = if_number
        if(version):
            attributes['version'] = str(version)
        if(activate):
            attributes['activate'] = None
        if(advertisement_interval):
            attributes['advertisement-interval'] = str(advertisement_interval)
        if(allow_policy):
            attributes['allow-policy'] = None
        if(allowas_in):
            attributes['allowas-in'] = None
        if(default_originate):
            attributes['default-originate'] = None
        if(default_originate_route_map):
            attributes['default-originate'] = {
                'route-map' : default_originate_route_map
            }
        if(dmzlink_bw):
            attributes['dmzlink-bw'] = None
        if(maximum_prefix_n):
            if('maximum-prefix' not in attributes):
                attributes['maximum-prefix'] = {}
            attributes['maximum-prefix']['max-prefix-no'] = maximum_prefix_n
        if(maximum_prefix_threshold):
            if('maximum-prefix' not in attributes):
                attributes['maximum-prefix'] = {}
            attributes['maximum-prefix']['threshold'] = maximum_prefix_threshold
        if(maximum_prefix_restart):
            if('maximum-prefix' not in attributes):
                attributes['maximum-prefix'] = {}
            attributes['maximum-prefix']['restart'] = maximum_prefix_restart
        if(maximum_prefix_warning):
            if('maximum-prefix' not in attributes):
                attributes['maximum-prefix'] = {}
            attributes['maximum-prefix']['warning-only'] = None
        if(next_hop_self):
            attributes['next-hop-self'] = None
        if(next_hop_self_all):
            attributes['next-hop-self'] = {
                'all': None
            }
        if(next_hop_unchanged):
            attributes['next-hop-unchanged'] = None
        if(route_reflector_client):
            attributes['route-reflector-client'] = None
        if(send_community):
            attributes['send-community'] = None
        if(send_label):
            attributes['send-label'] = None
        if(soft_reconfiguration):
            attributes['soft-reconfiguration'] = soft_reconfiguration
        if(weight):
            attributes['weight'] = str(weight)

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
