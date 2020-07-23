#!/usr/bin/python

from collections import namedtuple


# --------------------------------------
# Helper functions to process link data
# --------------------------------------

def dict2link_nt(link_dict):
    """
    Convert a dict representing a link to a namedtuple.
    This makes links hashable and easier to compare
    :param link_dict:
    :return:
    """

    TopologyInterface = namedtuple('TopologyInterface', ['node', 'interface', 'unit', 'parent'])
    TopologyLink = namedtuple('TopologyLink', ['source', 'target'])

    source = TopologyInterface(
        node=link_dict["source"]["node"]["name"],
        interface=link_dict["source"]["interface"]["name"],
        unit=link_dict["source"]["interface"]["unit"],
        parent=link_dict["source"]["interface"]["parent"]
    )
    target = TopologyInterface(
        node=link_dict["target"]["node"]["name"],
        interface=link_dict["target"]["interface"]["name"],
        unit=link_dict["target"]["interface"]["unit"],
        parent=link_dict["target"]["interface"]["parent"]
    )
    link = TopologyLink(source=source, target=target)

    return link


def link_nt2dict(link_nt):
    """
    Convert a namedtuple representing a link to a dict.
    :param link_nt:
    :return:
    """
    link_dict = {
        "source": {
            "node": {
                "name": link_nt.source.node
            },
            "interface": {
                "name": link_nt.source.interface,
                "unit": link_nt.source.unit,
                "parent": link_nt.source.parent
            }
        },
        "target": {
            "node": {
                "name": link_nt.target.node
            },
            "interface": {
                "name": link_nt.target.interface,
                "unit": link_nt.target.unit,
                "parent": link_nt.target.parent
            }
        }
    }

    return link_dict


# --------------------------------------
# Filters
# --------------------------------------

class FilterModule(object):

    def filters(self):
        return {
            'extract_links': self.extract_links,
            'get_group_links': self.get_group_links,
            'filter_interface_terse': self.filter_interface_terse,
            'select_group_interfaces': self.select_group_interfaces,
            'get_multiple_groups_links': self.get_multiple_groups_links
        }

    def extract_links(self, lldp_info, inventory_hostname_short, include_parents=True):
        """
        This filter returns a list of links from the lldp information passed as input. Each link is represented as a
        dictionary with the following structure:
        {
            source: {
                node: {
                    name: str
                }
                interface: {
                    name: str,
                    unit: str,
                    parent: str
                }
            },
            target: {
                node: {
                    name: str
                }
                interface: {
                    name: str,
                    unit: str,
                    parent: str
                }
            }
        }
        :param lldp_info:
        :param inventory_hostname_short:
        :param include_parents: If True, include parent interface name in the link representation.
        otherwise, set the parent to None
        :return:

        Example structure of lldp_info["lldp-neighbors-information"][0]["lldp-neighbor-information"]:

        {
            u'lldp-local-parent-interface-name': [{   u'data': u'ae0'}],
            u'lldp-local-port-id': [{   u'data': u'xe-0/0/0'}],
            u'lldp-remote-chassis-id': [{   u'data': u'64:64:9b:25:5d:80'}],
            u'lldp-remote-chassis-id-subtype': [{   u'data': u'Mac address'}],
            u'lldp-remote-port-description': [{   u'data': u'xe-0/0/1'}],
            u'lldp-remote-system-name': [{   u'data': u'ex4600-101'}]
        }
        """

        links = []
        for lldp_neighbour in lldp_info["lldp-neighbors-information"][0]["lldp-neighbor-information"]:

            # It would be great to use defaultdict, but this leads to incompatibility problems when loading variables
            # as input to other filters
            # link = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))

            link = {
                "source": {
                    "node": {
                        "name": None
                    },
                    "interface": {
                        "name": None,
                        "unit": None,
                        "parent": None
                    }
                },
                "target": {
                    "node": {
                        "name": None
                    },
                    "interface": {
                        "name": None,
                        "unit": None,
                        "parent": None
                    }
                },
            }

            # Data structure to represent an interface
            # Parent represents the aggregated interface is the current interface is part of a bundle
            Interface = namedtuple("Interface", ['node_name', 'port_name', 'parent_name'])

            try:
                # Get information parsing the lldp data
                neighbor_short_name = lldp_neighbour["lldp-remote-system-name"][0]["data"].split('.')[0]
                neighbor_port = lldp_neighbour["lldp-remote-port-description"][0]["data"]
                local_port = lldp_neighbour["lldp-local-port-id"][0]["data"]
                # If the parent is not present because the interface is not part of a bundle, this field is "-".
                # In this case, set the parent attribute to None
                local_parent = (lldp_neighbour["lldp-local-parent-interface-name"][0]["data"]
                                if lldp_neighbour["lldp-local-parent-interface-name"][0]["data"] != "-" and include_parents else None)
            except Exception:
                # If neighbour's info are not readable, just skip that link and assume that is not active.
                continue

            # Create interface structures for each node
            local_interface = Interface(inventory_hostname_short, port_name=local_port, parent_name=local_parent)
            neighbor_interface = Interface(neighbor_short_name, port_name=neighbor_port, parent_name=None)

            # The sorting is used to make sure that source and target are consistently assigned based on the
            # alphabetical order of node's names, regardless who is the local and who the remote node
            link_tuple = sorted((local_interface, neighbor_interface), key=lambda item: item[0])

            link["source"]["node"]["name"] = link_tuple[0].node_name
            link["source"]["interface"]["name"] = link_tuple[0].port_name
            link["source"]["interface"]["unit"] = "0"
            link["source"]["interface"]["parent"] = link_tuple[0].parent_name

            link["target"]["node"]["name"] = link_tuple[1].node_name
            link["target"]["interface"]["name"] = link_tuple[1].port_name
            link["target"]["interface"]["unit"] = "0"
            link["target"]["interface"]["parent"] = link_tuple[1].parent_name

            links.append(link)

        return links

    def get_group_links(self, local_links_list, devices=None, filter_device=None, consider_aggregate=True):
        """
        Process the list of links representing all the connections of a group of devices and return a unified
        list of links with no duplicates and possibly filtered based on the device group.
        :param local_links_list: a list of lists. Each list contains the links of an individual device from its own
        prospective. Therefore, the same link can be present in multiple lists, which is the case for neighbor devices.
        :param devices: a list of device names. If given, it will only return the links connecting these devices
        :param filter_device: a device name. If present, the returned list is filtered to contain only the links
        belonging to this device
        :param consider_aggregate: If True, link bundles will be represented by the corresponding aggregated interface
        (i.e. ae0) while the physical constituent interfaces will be ignored.
        :return: list of link dicts
        """

        # flatten the list of lists in a single one
        links = []
        for local_links in local_links_list:
            for link in local_links:
                links.append(link)

        # Convert dicts to namedtuple objects
        links_nt = [dict2link_nt(l) for l in links]

        if consider_aggregate:
            # Consolidate aggregated links
            # Because from lldp there is no parent information on the neighbour interface, let's figure it out
            links_nt = self._squash_bundle_links(links_nt)

        # Remove duplicates
        links_nt = list(set(links_nt))

        if devices:
            # Exclude links that do not belong to the device list
            links_nt = [l for l in links_nt if l.source.node in devices and l.target.node in devices]
        # Convert links back to dict
        links = [link_nt2dict(l) for l in links_nt]

        if filter_device:
            # Filter the result to only include links belonging to the filter device
            links = [l for l in links
                     if l["source"]["node"]["name"] == filter_device or l["target"]["node"]["name"] == filter_device]

        return links

    def get_multiple_groups_links(self, local_links_list, group_names, group_members, filter_device=None, consider_aggregate=True):
        """

        :param local_links_list
        :param group_names:
        I.e. ['group_1', 'group_2']
        :param group_members:
        I.e.
        {
            'group_1': [
                'device_1',
                'device_2'
            ],
            'group_2': [
                'device_1',
                'device_3'
            ]

        }
        :param filter_device: a device name. If present, the returned list is filtered to contain only the links
        belonging to this device
        :return: dict whose keys are the group names and value are the list of links connecting
        the devices belonging to that group, possibly filtered
        """

        topology_links_per_group = {}

        for group in group_names:
            # get the list of links for this specific group
            topology_links = self.get_group_links(local_links_list,
                                                  devices=group_members[group],
                                                  filter_device=filter_device,
                                                  consider_aggregate=consider_aggregate)

            topology_links_per_group[group] = topology_links

        return topology_links_per_group

    def select_group_interfaces(self, group_links, device):
        """
        From the list of links select only the interfaces that belong to the device and return them in a list of dict
        :param group_links:
        :param device:
        :return: list of interfaces

        [

            {
                name: str
                unit: str
            }
        ]
        """

        # First filter the result to only include links belonging to the device
        device_links = [l for l in group_links
                        if l["source"]["node"]["name"] == device or l["target"]["node"]["name"] == device]

        # Start from the source interfaces
        device_interfaces = [{"name": link['source']['interface']['name'],
                              "unit": link['source']['interface']['unit']}
                             for link in device_links if link["source"]["node"]["name"] == device]

        # Add the target interfaces
        device_interfaces.extend([{"name": link['target']['interface']['name'],
                                   "unit": link['target']['interface']['unit']}
                                  for link in device_links if link["target"]["node"]["name"] == device])

        return device_interfaces

    def filter_interface_terse(self, show_interface_output, admin_status=None, link_status=None,
                               interface_start_with=None, exclude_protocols=None):
        """
        Filter the output of show interface terse by interface name and status
        :param show_interface_output:
        :param admin_status:
        :param link_status:
        :param interface_start_with:
        :param exclude_protocols: List of protocol names to exclude (I.e. inet to exclude ipv4 interfaces,
        or aenet to exclude children interfaces participating in an aggregated )
        :return:
        """

        interface_dicts = show_interface_output['stdout_lines'][0]['interface-information'][0]['physical-interface']

        if admin_status:
            interface_dicts = [inter for inter in interface_dicts if inter['admin-status'][0]['data'] == admin_status]

        if link_status:
            interface_dicts = [inter for inter in interface_dicts if inter['oper-status'][0]['data'] == link_status]

        if interface_start_with:
            interface_dicts = [inter for inter in interface_dicts
                               if any(list(map(lambda s: str(inter["name"][0]['data']).startswith(s),
                                               interface_start_with)))]
        if exclude_protocols:
            tmp_dicts = []
            for inter in interface_dicts:
                try:
                    if inter['logical-interface'][0]['address-family'][0]['address-family-name'][0]['data'] not in exclude_protocols:
                        tmp_dicts.append(inter)
                except KeyError:
                    # Logical interface not configured at all. Just accept the interface and move forward
                    tmp_dicts.append(inter)

            interface_dicts = tmp_dicts

        return interface_dicts

    def _squash_bundle_links(self, links):
        """
        Squash links that belong to a bundle to represent the link with the corresponding aggregate interface while
        removing physical constituent interfaces from the result
        :param links: list of links. Each link is represented as a namedtuple
        :return:
        """

        # Consolidate aggregated links
        # Because from lldp there is no parent information on the neighbour interface, let's figure it out
        consolidated_links = []

        for link in links:
            if any([link.source.parent, link.target.parent]):
                # the link is part of a bundle

                # Pick the label (source or target) corresponding to the interface part of the bundle
                current_label = "source" if link.source.parent else "target"
                opposite_label = "source" if current_label == "target" else "source"

                # Find another link whose opposite interface has same name and parent populated
                opposite_link = [l for l in links
                                 if getattr(l, opposite_label).parent
                                 and getattr(l, opposite_label).interface == getattr(link, current_label).interface][0]

                # Create a new link whose interface name is now the parent lag
                lag_link_dict = {
                    "source": {
                        "node": {
                            "name": None
                        },
                        "interface": {
                            "name": None,
                            "unit": "0",
                            "parent": None
                        }
                    },
                    "target": {
                        "node": {
                            "name": None
                        },
                        "interface": {
                            "name": None,
                            "unit": "0",
                            "parent": None
                        }
                    },
                }
                lag_link_dict[current_label]["node"]["name"] = getattr(link, current_label).node
                lag_link_dict[current_label]["interface"]["name"] = getattr(link, current_label).parent
                lag_link_dict[current_label]["interface"]["parent"] = None
                lag_link_dict[opposite_label]["node"]["name"] = getattr(opposite_link, opposite_label).node
                lag_link_dict[opposite_label]["interface"]["name"] = getattr(opposite_link, opposite_label).parent
                lag_link_dict[opposite_label]["interface"]["parent"] = None

                # There will be duplicates, removed afterwards
                lag_link_dict_nt = dict2link_nt(lag_link_dict)
                consolidated_links.append(lag_link_dict_nt)
            else:
                # The link is a normal one. Just append it
                consolidated_links.append(link)
        return consolidated_links
