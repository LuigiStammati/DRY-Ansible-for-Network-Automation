Junos Backup Config
=========

This role retrieves the active configuration of the target device and saves it in the 
designated folder. The configuration file is named with the current timestamp followed 
by the hostname. I.e. ``2019-08-30_1645.ex4300-3.conf ``. 

Additionally, you can provide a string label that will be appended after the 
timestamp in the file name. I.e. ``2019-08-30_1645.my_setup.ex4300-3.conf``.
You can specify the label by overriding the variable ``config_label``, either 
in the inventory (group_vars or host_vars) or via cli as extra var. 


Requirements
------------

None

Role Variables
--------------

* __backup_config_dir__: the local folder path where configuration files will be saved.
Default is a folder "_backup_configs" in the inventory directory. Override this variables
in group_vars or host_vars to select a different backup path. The folder will be automatically
created if it does not exist.
* __config_label__: the string label you want to include in the file name


Dependencies
------------

The following roles:

* Juniper.junos

Example Playbook
----------------



```buildoutcfg
# playbook.yml

- name: Backup configurations
  hosts: all
  connection: local
  gather_facts: no
  roles:
    - dana_junos_backup_config
```

License
-------

BSD

Author Information
------------------

Luigi Stammati