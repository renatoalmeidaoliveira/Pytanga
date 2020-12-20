from pytanga.components.Cisco.xe.bgp import bgpComponent
from pytanga.components.Cisco.xe.bgp import bgpConfigComponent
from pytanga.components.Cisco.xe.bgp import neighborComponent
from pytanga.components.Cisco.xe.bgp import networkComponent
from pytanga.components.Cisco.xe.bgp import neighborRouteMapComponent
from pytanga.components.Cisco.xe.bgp import peerGroupComponent
from pytanga.components.Cisco.xe.bgp import addressFamiliesComponent
from pytanga.components.Cisco.xe.bgp import addressFamilyVRFComponent
from pytanga.components.Cisco.xe.bgp import addressFamilyTypeComponent
from pytanga.components.Cisco.xe.bgp import addressFamilyIPv4UnicastComponent


class ConfigureBGPError(Exception):
    pass


class ConfigureBGP():

    def __init__(self,
                 asn,
                 aigp_rib_metric=None,
                 always_compare_med=None,
                 cluster_id=None,
                 deterministic_med=None,
                 enforce_first_as=None,
                 enhanced_error=None,
                 fast_external_fallover=None,
                 log_neighbor_changes=None,
                 maxas_limit=None,
                 maxcommunity_limit=None,
                 route_map_cache=None,
                 update_delay=None,
                 router_id=None,):

        self.bgp = bgpComponent(asn=asn,
                                aigp_rib_metric=aigp_rib_metric,
                                always_compare_med=always_compare_med,
                                cluster_id=cluster_id,
                                deterministic_med=deterministic_med,
                                enforce_first_as=enforce_first_as,
                                enhanced_error=enhanced_error,
                                fast_external_fallover=fast_external_fallover,
                                log_neighbor_changes=log_neighbor_changes,
                                maxas_limit=maxas_limit,
                                maxcommunity_limit=maxcommunity_limit,
                                route_map_cache=route_map_cache,
                                update_delay=update_delay,
                                router_id=router_id,
                                )
        self.neighbor = {}
        self.afis_safis = addressFamiliesComponent()
        self.bgp.add(self.afis_safis)
        self.afis_safis_noVRF = addressFamilyVRFComponent(with_vrf=False)
        self.afis_safis.add(self.afis_safis_noVRF)
        self.afis_safic_types = {}

    def addAfi_Safi(self, afi_name, safi_name):
        types = {
            'ipv4': ['flowspec', 'mdt', 'multicast', 'mvpn', 'unicast'],
            'ipv6': ['flowspec',  'multicast', 'mvpn', 'unicast'],
            'l2vpn': ['evpn', 'vpls'],
            'link-state': ['link-state'],
            'nsap': ['unicast'],
            'rtfilter': ['unicast'],
            'vpnv4': ['flowspec',  'multicast', 'unicast'],
            'vpnv6': ['flowspec',  'multicast', 'unicast']
        }
        if(afi_name not in types.keys()):
            raise ConfigureBGPError(f"unknown afi_name must be in {types.keys()}")
            if(safi_name not in types[afi_name]):
                raise ConfigureBGPError(f"unknown safi_name must be in {types[afi_name]}")
        afiKey = f"{afi_name}-{safi_name}"
        if(afiKey not in self.afis_safic_types):
            if(afiKey == 'ipv4-unicast' or afiKey == 'ipv4-multicast'):
                ipv4 = addressFamilyTypeComponent(
                    afi_name=afi_name, safi_name=safi_name)
                ipv4_uni = addressFamilyIPv4UnicastComponent()
                ipv4.add(ipv4_uni)
                self.afis_safis_noVRF.add(ipv4)
                self.afis_safic_types[afiKey] = {
                    'outer': ipv4,
                    'inner': ipv4_uni,
                    'neighbors': {},
                    'networks': {}
                }
            else:
                raise ConfigureBGPError("Address Family not implemented")

    def configureAfiSafiBGP(self, afi_safi,
                            advertise_best_external=None,
                            dmzlink_bw=None,
                            suppress_inactive=None,
                            soft_reconfig_backup=None,
                            scan_time=None):
        if(afi_safi not in self.afis_safic_types):
            raise ConfigureBGPError(
                "Address Family not created. Create First with addAfi_Safi()")

        bgpconf = bgpConfigComponent(
            advertise_best_external=advertise_best_external,
            dmzlink_bw=dmzlink_bw,
            suppress_inactive=suppress_inactive,
            soft_reconfig_backup=soft_reconfig_backup,
            scan_time=scan_time)
        self.afis_safic_types[afi_safi]['inner'].add(bgpconf)

    def addNeighbor(self,
                    address,
                    remote_as=None,
                    cluster_id=None,
                    description=None,
                    disable_connected_check=None,
                    ebgp_multihop=None,
                    password=None,
                    peer_group=None,
                    shutdown=None,
                    keepalive_interval=None,
                    holdtime=None,
                    minimum_neighbor_hold=None,
                    ttl_security=None,
                    update_source=None,
                    version=None):
        if(address not in self.neighbor):
            neighbor = neighborComponent(address=address,
                                         remote_as=remote_as,
                                         cluster_id=cluster_id,
                                         description=description,
                                         disable_connected_check=disable_connected_check,
                                         ebgp_multihop=ebgp_multihop,
                                         password=password,
                                         peer_group=peer_group,
                                         shutdown=shutdown,
                                         keepalive_interval=keepalive_interval,
                                         holdtime=holdtime,
                                         minimum_neighbor_hold=minimum_neighbor_hold,
                                         ttl_security=ttl_security,
                                         update_source=update_source,
                                         version=version)

            self.neighbor[address] = neighbor
            self.bgp.add(neighbor)

    def addAfiSafiNeighbor(self,
                           afi_safi,
                           address,
                           activate=None,
                           advertisement_interval=None,
                           allow_policy=None,
                           allowas_in=None,
                           default_originate=None,
                           default_originate_route_map=None,
                           dmzlink_bw=None,
                           maximum_prefix_n=None,
                           maximum_prefix_threshold=None,
                           maximum_prefix_restart=None,
                           maximum_prefix_warning=None,
                           next_hop_self=None,
                           next_hop_self_all=None,
                           next_hop_unchanged=None,
                           route_reflector_client=None,
                           send_community=None,
                           send_label=None,
                           soft_reconfiguration=None,
                           weight=None):
        if(afi_safi not in self.afis_safic_types):
            raise ConfigureBGPError(
                "Address Family not created. Create First with addAfi_Safi()")
        if(address not in self.afis_safic_types[afi_safi]['neighbors']):
            neighbor = neighborComponent(
                address=address,
                activate=activate,
                advertisement_interval=advertisement_interval,
                allow_policy=allow_policy,
                allowas_in=allowas_in,
                default_originate=default_originate,
                default_originate_route_map=default_originate_route_map,
                dmzlink_bw=dmzlink_bw,
                maximum_prefix_n=maximum_prefix_n,
                maximum_prefix_threshold=maximum_prefix_threshold,
                maximum_prefix_restart=maximum_prefix_restart,
                maximum_prefix_warning=maximum_prefix_warning,
                next_hop_self=next_hop_self,
                next_hop_self_all=next_hop_self_all,
                next_hop_unchanged=next_hop_unchanged,
                route_reflector_client=route_reflector_client,
                send_community=send_community,
                send_label=send_label,
                soft_reconfiguration=soft_reconfiguration,
                weight=weight
            )
            self.afis_safic_types[afi_safi]['inner'].add(neighbor)
            self.afis_safic_types[afi_safi]['neighbors'][address] = {
                'object': neighbor,
                'route-maps': []
            }

    def addAfiSafiNeighborRouteMap(self, afi_safi, nei_address, inout, name):
        if(afi_safi not in self.afis_safic_types):
            raise ConfigureBGPError(
                "Address Family not created. Create First with addAfi_Safi()")
        if(nei_address not in self.afis_safic_types[afi_safi]['neighbors']):
            raise ConfigureBGPError(
                "Neighbor not created. Create First with addAfiSafiNeighbor()")
        route_map = neighborRouteMapComponent(inout=inout, name=name)
        routeKey = f"{name}-{inout}"
        if(routeKey not in self.afis_safic_types[afi_safi]['neighbors'][nei_address]['route-maps']):
            self.afis_safic_types[afi_safi]['neighbors'][nei_address]['object'].add(
                route_map)
            self.afis_safic_types[afi_safi]['neighbors'][nei_address]['route-maps'].append(
                routeKey)

    def addAfiSafiNetwork(self, afi_safi, network, mask=None, route_map=None, backdoor=None):
        if(afi_safi not in self.afis_safic_types):
            raise ConfigureBGPError(
                "Address Family not created. Create First with addAfi_Safi()")
        netmask = f"{network}-{mask}"
        if(netmask not in self.afis_safic_types[afi_safi]['networks']):
            network = networkComponent(network, mask, route_map, backdoor)
            self.afis_safic_types[afi_safi]['inner'].add(network)

    def getBGP(self):
        return self.bgp

