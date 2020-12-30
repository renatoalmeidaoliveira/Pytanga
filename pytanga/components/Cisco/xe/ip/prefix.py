from pytanga.components import AbstractComponent


class prefixSyntaxError(Exception):
    pass


class prefixComponent(AbstractComponent):

    def __init__(self,
                 seq,
                 action,
                 network,
                 ge=None,
                 le=None):
        self._xmlns = {}
        self.attributes = self.setAttributes(seq,
                                             action,
                                             network,
                                             ge,
                                             le)
        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        self.tag = 'seq'

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      seq,
                      action,
                      network,
                      ge,
                      le):
        attributes = {}

        attributes['no'] = str(seq)
        if(action=='permit' or action=='deny'):
            attributes['action'] = action
        else:
            raise prefixSyntaxError("Incorrect action")
        attributes['ip'] = network
        if(ge):
            attributes['ge'] = ge
        if(le):
            attributes['le'] = le


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

