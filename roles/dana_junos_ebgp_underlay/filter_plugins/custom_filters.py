#!/usr/bin/python


# --------------------------------------
# Filters
# --------------------------------------

class FilterModule(object):

    def filters(self):
        return {
            'assign_underlay_asn': self.assign_underlay_asn,
            'get_local_asn': self.get_local_asn,
            'filter_own_links': self.filter_own_links
        }

    def assign_underlay_asn(self, links, asn_start, filter_device=None):
        """
        Incrementally picks an autonomous system number (ASN) starting from `asn_start` for each endpoint device.

        :param links: a list of links. Each link must be represented as a dict. The dict format is the same as the
        return value, but without the asn attributes
        :param asn_start: starting ASN. it can be int or str
        :param filter_device: a device name. If present, the return value is filtered to return only the links belonging
        to this device
        :return: list of links. Each link is a dict:
        {
            source: {
                node: {
                    name: str
                    asn: str
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
                    asn: str
                }
                interface: {
                    name: str
                    unit: str
                    ip_address: ip/mask
                }
            }
        }
        """

        # Keep track of which devices have been already assigned an ASN to
        asn_tracker = {}

        # Iterate over links and assign asn
        asn = int(asn_start)
        for link in links:

            source_name = link["source"]["node"]["name"]
            if source_name not in asn_tracker:
                # Pick a new asn
                link["source"]["node"]["asn"] = str(asn)
                # Update the asn tracker
                asn_tracker[source_name] = asn
                # Increment the asn for the next device
                asn += 1
            else:
                # Just copy the asn already selected for this device before
                link["source"]["node"]["asn"] = asn_tracker[source_name]

            # Same for the other link endpoint
            target_name = link["target"]["node"]["name"]
            if target_name not in asn_tracker:
                # Pick a new asn
                link["target"]["node"]["asn"] = str(asn)
                # Update the asn tracker
                asn_tracker[target_name] = asn
                # Increment the asn for the next device
                asn += 1
            else:
                # Just copy the asn already selected for this device before
                link["target"]["node"]["asn"] = asn_tracker[target_name]

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

    def get_local_asn(self, device_links, device):
        """
        From the list of links with already ASNs assigned, retrieve and return the ASN of the device
        :param device_links: a list of links the device is connected to.
         Each link must be represented as a dict which includes the asn information
                {
            source: {
                node: {
                    name: str
                    asn: str
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
                    asn: str
                }
                interface: {
                    name: str
                    unit: str
                    ip_address: ip/mask
                }
            }
        }
        :param device: the name of the device you want to retrieve the asn for
        :return: str. The asn of the device
        """

        # Pick the first link

        if device_links[0]["source"]["node"]["name"] == device:
            return device_links[0]["source"]["node"]["asn"]
        elif device_links[0]["target"]["node"]["name"] == device:
            return device_links[0]["target"]["node"]["asn"]
        else:
            raise ValueError("device {} not found in the first link. No ASN can be retrieved. "
                             "The device provided as input must be included in the device_links".format(device))
