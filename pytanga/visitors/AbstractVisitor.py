from abc import ABC, abstractmethod


class AbstractVisitor(ABC):

	 @abstractmethod
	 def parse(self, leaf):
	 	pass
