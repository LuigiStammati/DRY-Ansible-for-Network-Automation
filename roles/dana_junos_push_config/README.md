Junos Push Config
=========

This Ansible role provides a quick way to push a configuration file to a juniper device.

You only specify the folder that contains the configuration files. This role will first search for a configuration file 
that matches the target device name (file name must end with _hostname_.conf). Finally, it will load and commit 
(by default with the merge option) the configuration to the remote host. 


If more than one file match the device name, only one will be used. 


Requirements
------------

None

Role Variables
--------------

Variable in default/main.yml:


* `built_configs_dir` (default `{{ inventory_dir }}/_built_configs`): Path to the directory where the configuration 
files you wish to load and commit are located;
* `loading_option` (default `merge`): the junos loading method to use. Common options are `merge`, `override`, `update`, 
`set`. Check [juniper_junos_config](https://junos-ansible-modules.readthedocs.io/en/2.0.0/juniper_junos_config.html)
documentation for more info;
* `telnet_user` (default `root`) and `telnet_password` (default `''`): the credential that will be used to attempt a 
telnet connection if the first SSH connection fails. Useful to push the initial default configuration to devices 
not configured with SSH yet (for example _zeroized_ devices)
* `prefix_filter_label` (default `null`): an optional string. If provided, only configuration files starting with 
this prefix will be looked up in the folder;


Dependencies
------------

* __Juniper.junos__ role. Already included in the meta, no need to import this role at the playbook level.


License
-------


Author Information
------------------

Luigi Stammati
