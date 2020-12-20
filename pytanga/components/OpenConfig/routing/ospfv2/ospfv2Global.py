from pytanga.components import AbstractComponent


class ospfv2GlobalComponent(AbstractComponent):

    def __init__(
            self,
            router_id=None,
            summary_route_cost_mode=None,
            igp_shortcuts=None,
            log_adjacency_changes=None,
            hide_transit_only_networks=None):

        self._xmlns = {}
        self.attributes = self.setAttributes(router_id, summary_route_cost_mode, igp_shortcuts, log_adjacency_changes, hide_transit_only_networks)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'global'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, router_id, summary_route_cost_mode, igp_shortcuts, log_adjacency_changes, hide_transit_only_networks):
        attributes = {}
        attributes['config'] = {}
        if(router_id):
            attributes['config']['router-id'] = router_id
        if(summary_route_cost_mode):
            attributes['config']['summary-route-cost-mode'] =  summary_route_cost_mode
        if(igp_shortcuts):
            attributes['config']['igp-shortcuts'] =  igp_shortcuts
        if(log_adjacency_changes):
            attributes['config']['log-adjacency-changes'] =  log_adjacency_changes
        if(hide_transit_only_networks):
            attributes['config']['hide-transit-only-networks'] =  hide_transit_only_networks
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

