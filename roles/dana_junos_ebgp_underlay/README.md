Role Name
=========

This role generates Junos configurations for EBGP underlay connectivity.

The role will automatically:

1. Discover the links connecting the devices in the underlay group,  
2. Generate the underlay IP address configurations,
3. Assign a unique ASN to each device and generate the EBGP configurations to establish BGP peering over the physical 
interfaces and redistribute the loopback interface addresses.

Requirements and Role Dependencies
----------------------------------

roles:

* [dana_junos_ip_underlay](../dana_junos_ip_underlay/README.md)



Role Variables
--------------

* `ebgp_underlay_config_dir` (default `"{{ inventory_dir }}/_ebgp_underlay_configs"`): The path to
the directory in which configuration files will be saved. If the folder specified does 
not exist, it will be automatically created.
* `underlay_group` (default `"ip_underlay"`): A group name that should also be defined in the inventory file. 
Only devices that are members of this group will be discovered and configured.
* `asn_start` (default `"4200000100"`): the first Autonomous System Number (ASN) that will be assigned to the first 
device. Further ASNs will be picked incrementally from this value. The default value represents a 32-bits ASN. However,
 the variable is just a string, therefore it can be also used to represent a 16-bit ASN e.g.`"65000"`


Example Playbook
----------------

```
# my_playbook.yml

- name: Generate IP and EBGP underlay configuration
  hosts: ip_underlay
  connection: local
  gather_facts: no
  tasks:
    - name: Generate IP and EBGP underlay configuration
      include_role:
        name: dana_junos_ebgp_underlay
        public: yes
        # Apply tags required to make role's tasks inherit the desired tags
        apply:
          tags:
            - always
      tags:
        - always
```


License
-------

BSD

Author Information
------------------

Luigi Stammati