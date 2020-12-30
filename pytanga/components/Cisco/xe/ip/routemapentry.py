from pytanga.components import AbstractComponent


class routemapSyntaxError(Exception):
    pass


class routemapentryComponent(AbstractComponent):

    def __init__(self,
                 operation,
                 description=None,
                 seq_no=None,
                 ordering_seq=None):
        self._xmlns = {}

        self.parent_xmlns = {}
        self._children: List[AbstractComponent] = []
        self.childrenData = []
        if(seq_no is None and ordering_seq is None):
            self.tag = 'route-map-without-order-seq'
        elif(ordering_seq is None and seq_no is not None):
            self.tag = 'route-map-without-order-seq'
        elif(seq_no is None and ordering_seq is not None):
            self.tag = 'route-map-seq'
        else:
            routemapSyntaxError(
                "seq_no and ordering_seq cannot be used together")
        self.attributes = self.setAttributes(
            operation,
            description,
            seq_no,
            ordering_seq)

    @property
    def xmlns(self):
        return self._xmlns

    @xmlns.setter
    def xmlns(self, xmlns):
        self._xmlns = xmlns

    def setAttributes(self,
                      operation,
                      description,
                      seq_no,
                      ordering_seq):
        attributes = {}
        if(operation == 'permit' or operation == 'deny'):
            attributes['operation'] = operation
        else:
            routemapSyntaxError("Invalid operation")
        if(description):
            attributes['description'] = description
        if(seq_no):
            attributes['seq_no'] = seq_no
        if(ordering_seq):
            attributes['ordering-seq'] = ordering_seq
        
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
