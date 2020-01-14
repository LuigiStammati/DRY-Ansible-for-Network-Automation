#!/usr/bin/python

from netaddr import IPNetwork


# --------------------------------------
# Filters
# --------------------------------------

class FilterModule(object):

    def filters(self):
        return {
            'assign_underlay_ip': self.assign_underlay_ip,
            'filter_own_links': self.filter_own_links
        }

    def assign_underlay_ip(self, links, ip_subnet_start, filter_device=None):
        """
        Incrementally picks a subnet starting from `ip_subnet_start` for each link and assigns an ip to each interface.

        :param links: a list of links. Each link must be represented as a dict. The dict format id the same as the
        return value, but without the ip address attributes
        :param filter_device: a device name. If present, the return value is filtered to return only the links belonging
        to this device
        :return: list of links. Each link is a dict:
        {
            source: {
                node: {
                    name: str
                }
                interface: {
                    name: str
                    unit: str
                    ip_address: ip/mask
                }
            },
            target: {
                node: {
                    name: str
                }
                interface: {
                    name: str
                    unit: str
                    ip_address: ip/mask
                }
            }
        }
        """

        # Iterate over links and assign ip addresses
        ip_subnet = IPNetwork(ip_subnet_start)
        ip_netmask = ip_subnet.prefixlen
        for link in links:

            # First host ip of the subnet is assigned to the source
            link["source"]["interface"]["ip_address"] = "{}/{}".format(str(list(ip_subnet.iter_hosts())[0]),
                                                                       ip_netmask)

            # Seconf host ip of the subnet is assigned to the target
            link["target"]["interface"]["ip_address"] = "{}/{}".format(str(list(ip_subnet.iter_hosts())[1]),
                                                                       ip_netmask)
            ip_subnet = ip_subnet.next(step=1)

        if filter_device:
            # Filter the result to only include links belonging to the filter device
            links = [l for l in links
                     if l["source"]["node"]["name"] == filter_device or l["target"]["node"]["name"] == filter_device]
        return links

    def filter_own_links(self, links, device):

        # Filter the links to only include links belonging to the device
        links = [l for l in links
                 if l["source"]["node"]["name"] == device or l["target"]["node"]["name"] == device]
        return links
