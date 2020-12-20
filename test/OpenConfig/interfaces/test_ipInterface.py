import unittest
from pytanga.components import configComponent
from pytanga.components.OpenConfig.interfaces import interfacesComponent
from pytanga.components.OpenConfig.interfaces import interfaceComponent
from pytanga.components.OpenConfig.interfaces import subinterfacesComponent
from pytanga.components.OpenConfig.interfaces import subinterfaceComponent
from pytanga.components.OpenConfig.interfaces import oc_ipComponent
from pytanga.components.OpenConfig.interfaces import oc_ipAddressesComponent
from pytanga.components.OpenConfig.interfaces import oc_ipAddressComponent
from pytanga.helpers.OpenConfig.interfaces import createIPInterface
from pytanga.visitors import NETCONFVisitor



class ipInterfaceTest(unittest.TestCase):

    IETF_INTERFACE_TYPES = {
        "loopback": "ianaift:softwareLoopback",
        "ethernet": "ianaift:ethernetCsmacd"
    }

    def test_CorrectIPInterfaceCreation(self):
        self.maxDiff = None
        data = {
            'name' : 'GigabitEthernet0/2',
            'if_type' : 'ethernet',
            'if_description' : "Test Interface",
            'if_mtu' :1500,
            'enabled' : True,
            'sub_index' : 0,
            'sub_desc' : None,
            'ip_version' : 4,
            'address' : '10.0.0.1',
            'prefix_length' : 30
        }
        iface  = createIPInterface(**data)
        serializer = NETCONFVisitor()
        output = iface.parse(serializer)
        xml_string = serializer.print(output)
        data['if_type'] = self.IETF_INTERFACE_TYPES[data['if_type']]
        if(data['enabled']) :
            data['enabled'] = 'true'
        teststring = "<interface><name>{name}</name><config><description>{if_description}</description><mtu>{if_mtu}</mtu><enabled>{enabled}</enabled><type xmlns:ianaift=\"urn:ietf:params:xml:ns:yang:iana-if-type\">{if_type}</type></config><subinterfaces><subinterface><index>{sub_index}</index><oc-ip:ipv4><oc-ip:addresses><oc-ip:address><oc-ip:ip>{address}</oc-ip:ip><oc-ip:config><oc-ip:ip>{address}</oc-ip:ip><oc-ip:prefix-length>{prefix_length}</oc-ip:prefix-length></oc-ip:config></oc-ip:address></oc-ip:addresses></oc-ip:ipv4></subinterface></subinterfaces></interface>"
        self.assertEqual(xml_string, teststring.format(**data) )




