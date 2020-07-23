Junos Topology Inspector
=========

This role automatically discovers links and interfaces connecting all the members of particular group. 

You do NOT need to preconfigure any discovery protocol or interface!
The only input you must provide is the name of the group (or optionally a list of groups) you want to inspect.


The results of this inspection are exposed in three variables that become available as facts in each device involved:

* `topology_links`
* `topology_links_per_group`
* `topology_interfaces`

You can find out more details about the above output variables in the _Role Variable_ section.

How does it work:

To carry out the inspection, this role automatically configures the interfaces connecting the devices involved 
and enables LLDP on all of them. However, you don't really need to worry about it: upon retrieving the relevant 
information and storing it in the output variables, this pre-configuration is cleaned up by a rollback operation.  


Requirements and Role Dependencies
------------

Roles:

* __Juniper.junos__ role. Already included in the _meta_, 
no need to import this role at the playbook level.


Target devices must run a Junos version that supports the LLDP option 
`neighbour-port-info-display port-description`. Please check the 
[juniper documentation](https://www.juniper.net/documentation/en_US/junos/topics/reference/configuration-statement/neighbor-port-info-display-edit-lldp.html)


Role Variables
--------------

Below the list of variables that this role employs to carry out the discovery operations. Each variable is provided with the
default value if there is one.


* `group_to_inspect` (default `"all"`): The name of the group you wish to inspect. Only links connecting devices of
 this group will be discovered and returned;
* `device_filter` (default `null`): If a device name is provided, output variables will be filtered to only contain results 
involving that device (the links connecting that device to any other member of the group under inspection). If null,
all links connecting all members of the group under inspection will be returned;

* `group_list_to_inspect` (default `null`): A list of group names. If provided, each group will be processed 
to figure out the links connecting its members. Results will be stored in the output variable `topology_links_per_group`.

* `consider_aggregate` (default `yes`): If yes, it will prioritise aggregated interfaces over physical interfaces 
to represent a link, when an aggregate is found. In this case, the results will not display the physical interfaces
belonging to an aggregate bundle, only the aggregate interface itself will be considered. If no, only physical links
will be included in the result, ignoring any possible aggregate bundle configured on top.

* `lldp_convergence_time` (default `5`) Seconds to wait after enabling LLDP before retrieving neighbours info.

* `commit_timeout` (default `30`) Timeout value when the configuration is committed. Refer to the `timeout` option in the
 _Junos_junos_config_ documentation for more details. 

Example Playbook
----------------

```
# my_playbook.yml

- name: Inspect topology
  hosts: all
  connection: local
  gather_facts: no
  tasks:
    - name: Inspect topology
      include_role:
        name: dana_junos_topology_inspector
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