from . import AbstractComponent


class rpcComponent(AbstractComponent):

    """This module defines the rpc Component.

        <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id=<message_id> >
        </rpc>

    """
    
    def __init__(self, message_id=""):
        """        
        Args:
            message_id (str, optional): rpc message-id, defaults to ""
        """
        self._xmlns = {
            'xmlns': "urn:ietf:params:xml:ns:netconf:base:1.0",
            'message-id': message_id
        }
        self.attributes = {}
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'rpc'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

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
