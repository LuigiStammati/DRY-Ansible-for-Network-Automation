Junos LAG
=========

This role automatically generates the Junos configuration for one or more aggregated interfaces (LAG) without 
requiring any interface name to be fed as input. 

You only create a group in the inventory file for each LAG interface you wish to configure that contains the devices for
which you want to bundle the interfaces together. The name must be `lag_bundle_<INT-NUM>`, where `<INT-NUM>` is the 
number you wish to use for that aggregate interface e.g. `lag_bundle_3>` would create the aggregate interface `ae3`.

The role will automatically discover links and interfaces connecting the two devices belonging to the group and create 
the corresponding configuration.


Requirements and Role Dependencies 
----------------------------------

roles:

* [dana_junos_topology_inspector](../dana_junos_topology_inspector/README.md)

Role Variables
--------------

* `lag_config_dir` (default `"{{ inventory_dir }}/_lag_configs"`): The path to
the directory in which configuration files will be saved. By default, it's a folder
called `_lag_configs` within the inventory file. If the folder specified does 
not exist, the role will create it automatically.


Example Playbook
----------------

```
# my_playbook.yml

- name: Generate LAG configuration
  hosts: all
  connection: local
  gather_facts: no
  tasks:
    - name: Generate LAG configuration
      include_role:
        name: dana_junos_lag
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