# Playbook - Push Config

Playbook name: pb_push_config.yml

This Playbook loads and commits one or more configuration files from a local folder to the corresponding remote devices,
 identified by the config file name.
 
It first attempts via NETCONF over SSH. If is fails, it automatically tries via TELNET.

## Requirements and Role Dependencies

The playbook relies on the following roles:

* [dana_junos_push_config](/roles/dana_junos_push_config/README.md)

You can check the requirements on roles' documentation.

## Playbook Variables

* `targets` (default value = `all`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name

## Example 1 - Basic

Suppose you need to load a configuration file on two devices whose hostnames are "my_qfx-1" and "my_qfx-2":

1. Name the configuration files so that it ends with "my_qfx-1.conf" and "my_qfx-2.conf" respectively 
(I.e. "my_qfx-1.conf", "2029_01_my_qfx-1.conf", "FINAL.my_qfx-1.conf", etc);
2. Place the files in the a folder called "_built_configs" inside the inventory folder. This is the default location, 
you can use a different folder by overriding the variables `built_configs_dir` 
3. Run the playbook

    ```
    ansible-playbook pb_push_config.yml -i invenotry/hosts.ini
    ```
    
The configurations will be loaded and committed on the remote devices. 
