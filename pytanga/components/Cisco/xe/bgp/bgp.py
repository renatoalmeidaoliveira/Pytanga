from pytanga.components import AbstractComponent


class bgpConfigComponent(AbstractComponent):

    def __init__(self,
                 aigp_rib_metric=None,
                 always_compare_med=None,
                 cluster_id=None,
                 deterministic_med=None,
                 enforce_first_as=None,
                 enhanced_error=None,
                 fast_external_fallover=None,
                 log_neighbor_changes=None,
                 maxas_limit=None,
                 maxcommunity_limit=None,
                 route_map_cache=None,
                 update_delay=None,
                 router_id=None,
                 advertise_best_external=None,
                 dmzlink_bw=None,
                 suppress_inactive=None,
                 soft_reconfig_backup=None,
                 scan_time=None,
                 ):
        self._xmlns = {}
        self.attributes = self.setAttributes(
            aigp_rib_metric,
            always_compare_med,
            cluster_id,
            deterministic_med,
            enforce_first_as,
            enhanced_error,
            fast_external_fallover,
            log_neighbor_changes,
            maxas_limit,
            maxcommunity_limit,
            route_map_cache,
            update_delay,
            router_id,
            advertise_best_external,
            dmzlink_bw,
            suppress_inactive,
            soft_reconfig_backup,
            scan_time
        )
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'bgp'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      aigp_rib_metric,
                      always_compare_med,
                      cluster_id,
                      deterministic_med,
                      enforce_first_as,
                      enhanced_error,
                      fast_external_fallover,
                      log_neighbor_changes,
                      maxas_limit,
                      maxcommunity_limit,
                      route_map_cache,
                      update_delay,
                      router_id,
                      advertise_best_external,
                      dmzlink_bw,
                      suppress_inactive,
                      soft_reconfig_backup,
                      scan_time
                      ):
        attributes = {}
        if(aigp_rib_metric):
            attributes['aigp-rib-metric'] = None
        if(always_compare_med):
            attributes['always-compare-med'] = None
        if(cluster_id):
            attributes['cluster-id'] = cluster_id
        if(deterministic_med):
            attributes['deterministic_med'] = None
        if(enforce_first_as):
            attributes['enforce-first-as'] = None
        if(enhanced_error):
            attributes['enhanced-error'] = 'true'
        if(fast_external_fallover):
            attributes['fast-external-fallover'] = 'true'
        if(log_neighbor_changes):
            attributes['log-neighbor-changes'] = 'true'
        if(maxas_limit):
            attributes['maxas-limit'] = str(maxas_limit)
        if(maxcommunity_limit):
            attributes['maxcommunity-limit'] = str(maxcommunity_limit)
        if(route_map_cache):
            attributes['route-map-cache'] = None
        if(update_delay):
            attributes['update-delay'] = update_delay
        if(router_id):
            attributes['router-id'] = {
                'ip-id': router_id
            }
        if(advertise_best_external):
            attributes['advertise-best-external'] = None
        if(dmzlink_bw):
            attributes['dmzlink-bw'] = None
        if(suppress_inactive):
            attributes['suppress-inactive'] = None
        if(soft_reconfig_backup):
            attributes['soft-reconfig-backup'] = None
        if(scan_time):
            attributes['scan-time'] = str(scan_time)
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


class bgpComponent(AbstractComponent):

    def __init__(self,
                 asn,
                 aigp_rib_metric=None,
                 always_compare_med=None,
                 cluster_id=None,
                 deterministic_med=None,
                 enforce_first_as=None,
                 enhanced_error=None,
                 fast_external_fallover=None,
                 log_neighbor_changes=None,
                 maxas_limit=None,
                 maxcommunity_limit=None,
                 route_map_cache=None,
                 update_delay=None,
                 router_id=None,
                 ):
        self._xmlns = {
            'xmlns': "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp",
        }
        self.attributes = self.setAttributes(
            asn
        )
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'bgp'
        if(aigp_rib_metric or
                always_compare_med or
                cluster_id or
                deterministic_med or
                enforce_first_as or
                enhanced_error or
                fast_external_fallover or
                log_neighbor_changes or
                maxas_limit or
                maxcommunity_limit or
                route_map_cache or
                update_delay or
                router_id):
            bgp = bgpConfigComponent(aigp_rib_metric,
                                     always_compare_med,
                                     cluster_id,
                                     deterministic_med,
                                     enforce_first_as,
                                     enhanced_error,
                                     fast_external_fallover,
                                     log_neighbor_changes,
                                     maxas_limit,
                                     maxcommunity_limit,
                                     route_map_cache,
                                     update_delay,
                                     router_id)
            self.add(bgp)

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      asn):
        attributes = {
            'id': str(asn)
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
