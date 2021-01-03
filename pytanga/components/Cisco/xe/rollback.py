from pytanga.components import AbstractComponent


class rollbackComponent(AbstractComponent):

    def __init__(self,
                 target_url,
                 verbose=None,
                 nolock=None,
                 revert_on_error=None,
                 revert_timer=None):
        self._xmlns = {
            "xmlns:cisco-ia": "http://cisco.com/yang/cisco-ia"
        }
        self.attributes = self.setAttributes(target_url,
                                             verbose,
                                             nolock,
                                             revert_on_error,
                                             revert_timer)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'cisco-ia:rollback'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      target_url,
                      verbose,
                      nolock,
                      revert_on_error,
                      revert_timer):
        attributes = {
                    'cisco-ia:target-url': target_url
                     }
        if(verbose is not None):
            attributes['cisco-ia:verbose'] = 'true'
        if(nolock is not None):
            attributes['cisco-ia:nolock'] = 'true'
        if(revert_on_error is not None):
            attributes['cisco-ia:revert-on-error'] = None
        if(revert_timer is not None):
            attributes['cisco-ia:revert-timer'] = str(revert_timer)
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
            child.getXMLNS()
        return self._xmlns

    def parse(self, serializer):
        self.childrenData = []
        self.getXMLNS()
        for child in self._children:
            self.childrenData.append(child.parse(serializer))
        return serializer.parse(self)
