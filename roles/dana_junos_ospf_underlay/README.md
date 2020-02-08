DANA - Junos OSPF Underlay
=========

This role generates Junos configurations for OSPF underlay connectivity.

The role will automatically:

1. Discover the links connecting the devices in the underlay group,  
2. Generate the underlay IP address configurations,
3. Generate the OSPF configurations to enable OSPF over the underlay interfaces and redistribute the loopback interface
 addresses.

Requirements and Role Dependencies
------------

This role relies on the following roles:

* [dana_junos_ip_underlay](../dana_junos_ip_underlay/README.md)


Role Variables
--------------

* `ospf_underlay_config_dir` (default `"{{ inventory_dir }}/_ospf_underlay_configs"`): The path to
the directory in which configuration files will be saved. If the folder specified does 
not exist, it will be automatically created.
* `underlay_group` (default `"ip_underlay"`): A group name that should also be defined in the inventory file. 
Only devices that are members of this group will be discovered and configured.
* `ospf_area` (default `"0.0.0.0"`): The OSPF area that will be configured.


Example Playbook
----------------

```
# my_playbook.yml

- name: Generate and provision OSPF underlay configurations
  hosts: ip_underlay
  connection: local
  gather_facts: no
  tasks:
    - name: Generate IP and OSPF underlay configurations
      include_role:
        name: dana_junos_ospf_underlay
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