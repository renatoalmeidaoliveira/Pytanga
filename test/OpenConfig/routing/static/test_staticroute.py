import unittest

from pytanga.components import configComponent
from pytanga.components.OpenConfig.routing import networkInstancesComponent
from pytanga.components.OpenConfig.routing import networkInstanceComponent
from pytanga.components.OpenConfig.routing import protocolsComponent
from pytanga.components.OpenConfig.routing import protocolComponent
from pytanga.components.OpenConfig.routing.static import staticroutesComponent
from pytanga.components.OpenConfig.routing.static import staticComponent
from pytanga.components.OpenConfig.routing.static import nexthopsComponent
from pytanga.components.OpenConfig.routing.static import nexthopComponent
from pytanga.components.OpenConfig.routing.static import interfacerefComponent
from pytanga.visitors import NETCONFVisitor

def CreateStaticRoute(prefix, name, nexthop):
    config = configComponent()
    netInsts = networkInstancesComponent()
    netinst = networkInstanceComponent()
    protos = protocolsComponent()
    proto = protocolComponent(identifier ='STATIC' , name='DEFAULT')
    staticroutes = staticroutesComponent()
    static = staticComponent(prefix= prefix)
    nexthops = nexthopsComponent()
    nexthop = nexthopComponent(index=name , next_hop=nexthop)

    nexthops.add(nexthop)
    static.add(nexthops)
    staticroutes.add(static)
    proto.add(staticroutes)
    protos.add(proto)
    netinst.add(protos)
    netInsts.add(netinst)
    config.add(netInsts)

    return config

class StaticRouteTest(unittest.TestCase):

    def testStaticRoute(self):
        self.maxDiff = None
        data = {
            'prefix':   '172.30.0.0/24',
            'name' :    'Test',
            'nexthop' : '192.168.0.4'
        }
        expected = "<config><network-instances xmlns=\"http://openconfig.net/yang/network-instance\"><network-instance><name>default</name><protocols><protocol><identifier xmlns:oc-pol-types=\"http://openconfig.net/yang/policy-types\">oc-pol-types:STATIC</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types=\"http://openconfig.net/yang/policy-types\">oc-pol-types:STATIC</identifier><name>DEFAULT</name></config><static-routes><static><prefix>{prefix}</prefix><config><prefix>{prefix}</prefix></config><next-hops><next-hop><index>{name}</index><config><index>{name}</index><next-hop>{nexthop}</next-hop></config></next-hop></next-hops></static></static-routes></protocol></protocols></network-instance></network-instances></config>"
        static  = CreateStaticRoute(**data)
        serializer = NETCONFVisitor()
        output = static.parse(serializer)
        xml_string = serializer.print(output)
        self.assertEqual(xml_string, expected.format(**data) )
