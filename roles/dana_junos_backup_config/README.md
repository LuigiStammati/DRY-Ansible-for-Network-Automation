Junos Backup Config
=========

This role retrieves the active configuration of the target device and saves it in the 
designated folder. The configuration file is named with the current timestamp followed 
by the hostname. I.e. `2019-08-30_1645.ex4300-3.conf `. 

Additionally, you can provide a string label that will be appended after the 
timestamp in the file name, e.g. `2019-08-30_1645.my_setup.ex4300-3.conf`.

You can specify the label by overriding the variable `config_label`, either 
in the inventory (group_vars or host_vars) or via cli as extra var. 


Requirements and Role Dependencies
----------------------------------

* __Juniper.junos__ role. Already included in the _meta_, 
no need to import this role at the playbook level.


Role Variables
--------------

* __backup_config_dir__ (default `{{ inventory_dir }}/_backup_configs`): the local folder path where configuration files
 will be saved. The folder will be automatically created if it does not exist.
* __config_label__ (default `null`): optional string label you may want to include in the file name.
* __include_timestamp__ (default `yes`): by default, the current timestamp is included in the file name. You can 
exclude it by setting this variable to `no`.

Example Playbook
----------------

```
# my_playbook.yml

- name: Backup active configurations
  hosts: all
  connection: local
  gather_facts: no
  tasks:
    - name: Backup active configurations
      include_role:
        name: dana_junos_backup_config
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