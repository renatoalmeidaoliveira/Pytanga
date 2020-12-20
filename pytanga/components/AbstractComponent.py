"""
This modules define the Abstract Component Class

"""
from abc import ABC, abstractmethod
from pytanga.visitors import AbstractVisitor

class AbstractComponent(ABC):


    @abstractmethod
    def add(self, component) -> None:
        """ This should method add a subComponent.    
        """
        pass

    
    @abstractmethod
    def remove(self, component) -> None:
        """ This should method remove a subComponent.    
        """
        pass


    @abstractmethod
    def parse(self , serializer: AbstractVisitor ) :
        """ This method should call the parse method for all childrens passing the serializer.    
        """
        pass

    @abstractmethod
    def getXMLNS(self) :
        pass


