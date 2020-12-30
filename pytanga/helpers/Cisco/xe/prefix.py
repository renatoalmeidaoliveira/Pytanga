from pytanga.components.Cisco.xe.ip import ipComponent
from pytanga.components.Cisco.xe.ip import prefixeslistsComponent
from pytanga.components.Cisco.xe.ip import prefixlistComponent
from pytanga.components.Cisco.xe.ip import prefixComponent


class ConfigurePrefixListError(Exception):
    pass


class ConfigurePrefixList():
    """
    Prefix List configuration helper Class

    :param name: the prefix list name
    :type name: string
    :param replace: set to config replace
    :type replace: string
    :param step: The sequence step for prefix list creation defaults 5
    :type step: integer

    """

    def __init__(self,
                 name,
                 replace=False,
                 step=5,):

        self.prefixLists = prefixeslistsComponent()
        operation=None
        if(replace):
            operation='replace'
        self.prefixlist = prefixlistComponent(name=name, operation=operation)
        self.prefixLists.add(self.prefixlist)
        self.step = step
        self.position = step
        self.prefixes = {}

    def addPrefix(self, action, network, seq=None):
        """
        Add a prefix to the prefix List

        :param action: The prefix action should be in ["permit" , "deny"]
        :type action: string

        :param network: The network
        :type network: string

        :param seq: The prefix sequence
        :type seq: integer, optional
        """
        if(action not in ["permit", "deny"]):
            raise ConfigurePrefixListError("Incorrect Action")
        if((network not in self.prefixes.keys()) and (seq is None)):
            prefix = prefixComponent(
                seq=self.position, action=action, network=network)
            self.position = self.position + self.step
            self.prefixes[network] = prefix
            self.prefixes[self.position] = prefix
            self.prefixlist.add(prefix)
        else:
            raise ConfigurePrefixListError("Network already configured")
        if(seq is not None):
            if((seq not in self.prefixes) and (network not in self.prefixes)):
                prefix = prefixComponent(
                    seq=seq, action=action, network=network)
                self.prefixes[network] = prefix
                self.prefixes[seq] = prefix
                self.prefixlist.add(prefix)
            else:
                raise ConfigurePrefixListError(
                    "Network or Seq already configured")

    def getPrefixList(self):
        """
        :return: The prefixList Component
        :rtype: prefixeslistsComponent
        """
        return self.prefixLists
