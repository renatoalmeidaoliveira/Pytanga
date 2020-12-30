from pytanga.components.OpenConfig.interfaces import interfaceComponent
from pytanga.components.OpenConfig.interfaces import subinterfacesComponent
from pytanga.components.OpenConfig.interfaces import subinterfaceComponent
from pytanga.components.OpenConfig.interfaces import oc_ipComponent
from pytanga.components.OpenConfig.interfaces import oc_ipAddressesComponent
from pytanga.components.OpenConfig.interfaces import oc_ipAddressComponent


def createIPInterface(name,
                      if_type,
                      ip_version,
                      address,
                      prefix_length,
                      if_description=None,
                      if_mtu=None,
                      enabled=None,
                      sub_index=0,
                      sub_desc=None):
    ifaceData = {
        'name': name,
        'if_type': if_type,
        }
    if(if_description):
        ifaceData['if_description'] = if_description
    if(if_mtu):
        ifaceData['if_mtu'] = if_mtu
    if(enabled):
        ifaceData['enabled'] = enabled
 
    iface = interfaceComponent(**ifaceData)
    ifaceSubs = subinterfacesComponent()
    subData = {
        'index': sub_index
    }
    if(sub_desc):
        subData['description'] = sub_desc
    
    ifaceSub = subinterfaceComponent(**subData)
    ifaceIP = oc_ipComponent(version=ip_version)
    ifaceIPAddrs = oc_ipAddressesComponent()
    ifaceIPAddr = oc_ipAddressComponent(address=address,
                                        prefix_length=prefix_length)

    ifaceIPAddrs.add(ifaceIPAddr)
    ifaceIP.add(ifaceIPAddrs)
    ifaceSub.add(ifaceIP)
    ifaceSubs.add(ifaceSub)
    iface.add(ifaceSubs)

    return(iface)
