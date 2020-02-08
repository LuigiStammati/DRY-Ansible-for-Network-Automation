# Playbook - Backup Active Configurations 

Playbook name: pb_backup_config.yml

This playbook retrieves all the active configurations of target devices and collects them in a local backup folder.
Configuration files are named with the corresponding device hostname, along with an optional timestamp and label.

## Roles Dependencies 

This Playbook relies on the following roles

* [dana_junos_backup_config](roles/dana_junos_backup_config/README.md)

## Example 1 - Basic

We assume you have an inventory folder structured as following:

```
inventory
├── group_vars
├── host_vars
└── hosts.ini
```

Your `hosts.ini` looks like this

```
# invenotry/hosts.ini

router-1
router-2
router-3
router-4
router-5
router-6
```

Run the playbook with no input variables:
 
```
ansible-playbook pb_backup_config.yml -i invenotry/hosts.ini
```

Output: 

```
inventory
├── _backup_configs
│   ├── 2020-01-01_1200.router-1.conf
│   ├── 2020-01-01_1200.router-2.conf
│   ├── 2020-01-01_1200.router-3.conf
│   ├── 2020-01-01_1200.router-4.conf
│   ├── 2020-01-01_1200.router-5.conf
│   └── 2020-01-01_1200.router-6.conf
```

By default, all the inventory hosts are targeted. You can be more selective 
by populating the variable`targets` with a particular device or group name.


## Example 2 - No Timestamps

By default, the current timestamp is included in the file name, but you can exclude it by editing the variable 
`include_timestamp`:

```yaml
# inventory/group_vars/all.yml

include_timestamp: no
```

Output: 

```
inventory
├── _backup_configs
│   ├── router-1.conf
│   ├── router-2.conf
│   ├── router-3.conf
│   ├── router-4.conf
│   ├── router-5.conf
│   └── router-6.conf
```

## Example 3 - Custom Labels

You can prepend a custom label to the configuration file name by editing:

```yaml
# inventory/group_vars/all.yml

config_label: MY-SETUP
```

Output: 

```
inventory
├── _backup_configs
│   ├── MY-SETUP.2020-01-01_1200.router-1.conf
│   ├── MY-SETUP.2020-01-01_1200.router-2.conf
│   ├── MY-SETUP.2020-01-01_1200.router-3.conf
│   ├── MY-SETUP.2020-01-01_1200.router-4.conf
│   ├── MY-SETUP.2020-01-01_1200.router-5.conf
│   └── MY-SETUP.2020-01-01_1200.router-6.conf
```

You can of course be more specific and set different labels for different devices with group or individual host 
granularity. You simply need to set the variables in the right place:

```
# inventory/hosts.ini

router-1
router-2

[my_core]
router-3
router-4

[my_access]
router-5
router-6
```

```yaml
# inventory/group_vars/all.yml

config_label: GENERIC
```

```yaml
# inventory/group_vars/my_core.yml

config_label: MY-CORE
```

```yaml
# inventory/group_vars/my_access.yml

config_label: MY-ACCESS
```

```yaml
# inventory/host_vars/router-1.yml

config_label: MY-BEST-ROUTER
```

Run the playbook:

```
ansible-playbook pb_backup_config.yml -i inventory/hosts.ini 
```

Output: 

```
inventory
├── _backup_configs
│   ├── MY-BEST-ROUTER.2020-01-01_1200.router-1.conf
│   ├── GENERIC.2020-01-01_1200.router-2.conf
│   ├── MY-CORE.2020-01-01_1200.router-3.conf
│   ├── MY-CORE.2020-01-01_1200.router-4.conf
│   ├── MY-ACCESS.2020-01-01_1200.router-5.conf
│   └── MY-ACCESS.2020-01-01_1200.router-6.conf
```

## Complete List of Variables

Playbook variables:

* `targets` (default value = `all`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name

Role Variables:

* [dana_junos_backup_config](/roles/dana_junos_topology_inspector/README.md)
