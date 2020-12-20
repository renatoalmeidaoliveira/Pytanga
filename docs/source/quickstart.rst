Quick Start
==================================

Installing
---------------------------

::

  pip install pytanga

Basic Usage
-----------------


Pytanga uses a Composite pattern to abstract YANG models, so each component has an add method which is we
ed to compose the payload.

Therefore, to build the desired payload it will be necessary to instantiate all modules equivalent to the YANG models and use the add method building the necessary hierarchy, as the example bellow:

.. code-block:: python

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
    from xml.dom.minidom import parseString

    config = configComponent()
    netInsts = networkInstancesComponent()
    netinst = networkInstanceComponent()
    protos = protocolsComponent()
    proto = protocolComponent(identifier ='STATIC' , name='DEFAULT')
    staticroutes = staticroutesComponent()
    static = staticComponent(prefix= '172.30.0.0/24')
    nexthops = nexthopsComponent()
    nexthop = nexthopComponent(index='NETCONF' , next_hop='192.168.0.4')

    nexthops.add(nexthop)
    static.add(nexthops)
    staticroutes.add(static)
    proto.add(staticroutes)
    protos.add(proto)
    netinst.add(protos)
    netInsts.add(netinst)
    config.add(netInsts)

    serializer = NETCONFVisitor()
    output = static.parse(serializer)
    xml_string = serializer.print(output)
    print(parseString(xml_string).toprettyxml())


Resulting in the following output


.. code-block:: XML

    <static>
        <prefix>172.30.0.0/24</prefix>
        <config>
            <prefix>172.30.0.0/24</prefix>
        </config>
        <next-hops>
            <next-hop>
                <index>NETCONF</index>
                <config>
                    <index>NETCONF</index>
                    <next-hop>192.168.0.4</next-hop>
                </config>
            </next-hop>
        </next-hops>
    </static>


Configuring BGP
---------------------------

For configure BGP use the :meth:`ConfigureBGP <pytanga.helpers.Cisco.xe.bgp.ConfigureBGP>` Helper


.. code-block:: python

    from pytanga.components import configComponent
    from pytanga.components.Cisco.xe import nativeComponent
    from pytanga.components.Cisco.xe import routerComponent
    from pytanga.helpers.Cisco.xe import ConfigureBGP
    from pytanga.visitors import NETCONFVisitor
    from xml.dom.minidom import parseString

    BGPHelper = ConfigureBGP(asn=100 , router_id='10.0.0.2')
    BGPHelper.addAfi_Safi(afi_name ='ipv4' , safi_name='unicast')
    BGPHelper.addNeighbor(address= '10.0.0.1'  , remote_as='100')
    BGPHelper.addNeighbor(address= '10.0.0.3'  , remote_as='100')
    BGPHelper.addAfiSafiNeighbor(afi_safi='ipv4-unicast' , address= '10.0.0.1')
    BGPHelper.addAfiSafiNeighbor(afi_safi='ipv4-unicast' , address= '10.0.0.3')
    BGPHelper.addAfiSafiNeighborRouteMap(afi_safi='ipv4-unicast' , nei_address= '10.0.0.3' , inout='in' , name='Teste')
    BGPHelper.addAfiSafiNetwork(afi_safi='ipv4-unicast' , network="10.0.0.0" , mask='255.255.255.255')
    BGP = BGPHelper.getBGP()

    router = routerComponent()
    XENative = nativeComponent()
    config = configComponent()

    router.add(BGP)
    XENative.add(router)
    config.add(XENative)

    serializer = NETCONFVisitor()
    output = config.parse(serializer)
    xml_string = serializer.print(output)
    print(parseString(xml_string).toprettyxml())


Resulting in the following output


.. code-block:: XML

    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <router>
                <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-bgp">
                    <id>100</id>
                    <bgp>
                        <router-id>
                            <ip-id>10.0.0.1</ip-id>
                        </router-id>
                    </bgp>
                    <address-family>
                        <no-vrf>
                            <ipv4>
                                <af-name>unicast</af-name>
                                <ipv4-unicast>
                                    <neighbor>
                                        <id>10.0.0.2</id>
                                    </neighbor>
                                    <neighbor>
                                        <id>10.0.0.3</id>
                                        <route-map>
                                            <inout>in</inout>
                                            <route-map-name>Teste</route-map-name>
                                        </route-map>
                                    </neighbor>
                                    <network>
                                        <with-mask>
                                            <number>10.0.0.0</number>
                                            <mask>255.255.255.255</mask>
                                        </with-mask>
                                    </network>
                                </ipv4-unicast>
                            </ipv4>
                        </no-vrf>
                    </address-family>
                    <neighbor>
                        <id>10.0.0.2</id>
                        <remote-as>100</remote-as>
                    </neighbor>
                    <neighbor>
                        <id>10.0.0.3</id>
                        <remote-as>100</remote-as>
                    </neighbor>
                </bgp>
            </router>
        </native>
    </config>
   


IOS-XE 16.9.1 resulting configuration:

::
  
    router bgp 100
     bgp router-id 10.0.0.2
     bgp log-neighbor-changes
     neighbor 10.0.0.1 remote-as 100
     neighbor 10.0.0.3 remote-as 100
     !
     address-family ipv4
      network 10.0.0.0 mask 255.255.255.255
      neighbor 10.0.0.1 activate
      neighbor 10.0.0.3 activate
      neighbor 10.0.0.3 route-map Teste in
     exit-address-family


Configuring Prefix-List
---------------------------

For configure prefix list use the :meth:`ConfigurePrefixList <pytanga.helpers.Cisco.xe.prefix.ConfigurePrefixList>` Helper

.. code-block:: python

    from pytanga.components import configComponent
    from pytanga.components.Cisco.xe import nativeComponent
    from pytanga.components.Cisco.xe.ip import ipComponent
    from pytanga.helpers.Cisco.xe import ConfigurePrefixList
    from pytanga.visitors import NETCONFVisitor
    from xml.dom.minidom import parseString

    config = configComponent()
    native = nativeComponent()
    ip = ipComponent()
    PrefixListHelper = ConfigurePrefixList(name="TEST-AS")
    PrefixListHelper.addPrefix(action="permit" , network="10.0.40.0/24")
    PrefixListHelper.addPrefix(action="permit" , network="10.0.50.0/24")

    ip.add(PrefixListHelper.getPrefixList())
    native.add(ip)
    config.add(native)

    serializer = NETCONFVisitor()
    output = config.parse(serializer)
    xml_string = serializer.print(output)
    print(parseString(xml_string).toprettyxml())


Resulting in the following output

.. code-block:: XML

    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <ip>
                <prefix-list>
                    <prefixes>
                        <name>TEST-AS</name>
                        <seq>
                            <no>5</no>
                            <permit>
                                <ip>10.0.40.0/24</ip>
                            </permit>
                        </seq>
                        <seq>
                            <no>10</no>
                            <permit>
                                <ip>10.0.50.0/24</ip>
                            </permit>
                        </seq>
                    </prefixes>
                </prefix-list>
            </ip>
        </native>
    </config>

IOS-XE 16.9.1 resulting configuration:

::

  ip prefix-list TEST-AS seq 5 permit 10.0.40.0/24
  ip prefix-list TEST-AS seq 10 permit 10.0.50.0/24


Configuring IP Interface with OpenConfig
-----------------------------------------------

For configure an IP Interface use the :meth:`CreateIPInterface <pytanga.helpers.OpenConfig.interfaces.createIPInterface>` Helper

.. code-block:: python

    from pytanga.components import configComponent
    from pytanga.helpers.OpenConfig.interfaces import createIPInterface
    from pytanga.components.OpenConfig.interfaces import interfacesComponent
    from pytanga.visitors import NETCONFVisitor
    from xml.dom.minidom import parseString

    interfaces = interfacesComponent()
    interface = createIPInterface(name="GigabitEthernet2",
                      if_type='ethernet',
                      ip_version=4,
                      address='10.0.0.5',
                      prefix_length=30,
                      if_mtu= 1650,
                      if_description='Test Configuration',
                      enabled=True)

    interfaces.add(interface)
    config = configComponent()
    config.add(interfaces)
    serializer = NETCONFVisitor()
    output = config.parse(serializer)
    xml_string = serializer.print(output)
    print(parseString(xml_string).toprettyxml())


Resulting in the following output

.. code-block:: XML

    <config>
        <interfaces xmlns="http://openconfig.net/yang/interfaces" xmlns:oc-ip="http://openconfig.net/yang/interfaces/ip">
            <interface>
                <name>GigabitEthernet2</name>
                <config>
                    <description>Test Configuration</description>
                    <mtu>1650</mtu>
                    <enabled>true</enabled>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                </config>
                <subinterfaces>
                    <subinterface>
                        <index>0</index>
                        <oc-ip:ipv4>
                            <oc-ip:addresses>
                                <oc-ip:address>
                                    <oc-ip:ip>10.0.0.5</oc-ip:ip>
                                    <oc-ip:config>
                                        <oc-ip:ip>10.0.0.5</oc-ip:ip>
                                        <oc-ip:prefix-length>30</oc-ip:prefix-length>
                                    </oc-ip:config>
                                </oc-ip:address>
                            </oc-ip:addresses>
                        </oc-ip:ipv4>
                    </subinterface>
                </subinterfaces>
            </interface>
        </interfaces>
    </config>


IOS-XE 16.9.1 resulting configuration:

::

    interface GigabitEthernet2
     description Test Configuration
     mtu 1650
     ip address 10.0.0.5 255.255.255.252
    end
