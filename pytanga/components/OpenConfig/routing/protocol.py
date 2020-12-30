from pytanga.components import AbstractComponent


class protocolComponent(AbstractComponent):

    def __init__(self,
                 identifier,
                 name=None,
                 enabled=None,
                 default_metric=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(identifier,
                                             name,
                                             enabled,
                                             default_metric)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'protocol'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self, identifier, name, enabled, default_metric):
        attributes = {}
        if(name):
            attributes['name'] = name
        attributes['identifier'] = {
            'keys': {
                'xmlns:oc-pol-types': 'http://openconfig.net/yang/policy-types'
            },
            'value': f"oc-pol-types:{identifier}"
        }
        attributes['config'] = {}
        attributes['config']['identifier'] = {
            'keys': {
                'xmlns:oc-pol-types': 'http://openconfig.net/yang/policy-types'
            },
            'value': f"oc-pol-types:{identifier}"
        }
        attributes['config']['name'] = name
        if(enabled):
            attributes['config']['enabled'] = 'true'
        if(default_metric):
            attributes['config']['default-metric'] = default_metric
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
