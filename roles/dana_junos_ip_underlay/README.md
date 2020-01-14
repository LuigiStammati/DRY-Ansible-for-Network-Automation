Junos IP Underlay
=========

This role generates Junos configurations for IP underlay connectivity.

You do NOT need to provide any information about the underlay topology! 
You only need to create a group in your inventory called 'ip_underlay' with the
list of devices you want to be part of it. That's all. The role will automatically:

1. discover the links connecting the devices in the underlay group, 
2. pick a unique ip subnet for each link, 
3. generate the interface configuration for each device properly assigning 
ip addresses from the selected subnet


Role Variables
--------------

* `ip_subnet_start` (default `"10.100.0.0/31"`): The subnet used for the first link. 
For each further link the next subnet will be incrementally picked 
* `underlay_mtu` (default `9216`): The MTU the interface will be configured with
* `underlay_group` (default `"ip_underlay"`): The name of the group used to configure 
the underlay. This group must be defined in the inventory file.
* `ip_underlay_config_dir` (default `"{{ inventory_dir }}/_ip_underlay_configs"`): The path to
the directory in which configuration files will be saved. By default, it's a folder
called `ip_underlay_configs` within the inventory file. If the folder specified does 
not exist, the role will create it automatically.

* `include_interface_description`: (default `yes`): If yes, it will configure neighbor's name as the description 
for each underlay interface


Dependencies
------------

roles:

* [dana_junos_topology_inspector](../dana_junos_topology_inspector/README.md)

Example Playbook
----------------


License
-------

BSD

Author Information
------------------

Luigi Stammati