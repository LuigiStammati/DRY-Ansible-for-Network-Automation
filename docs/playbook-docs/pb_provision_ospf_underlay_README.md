
# Provision OSPF Underlay 

Playbook: _pb_provision_ospf_underlay.yml_

This playbook first discovers the network topology, then generates the Junos configuration for underlay IP connectivity 
and OSPF over the physical interfaces to redistribute the loopback addresses.

## Requirements and Role Dependencies 

The playbook relies on the following roles:

* [dana_junos_ospf_underlay](/roles/dana_junos_ospf_underlay/README.md)
* [dana_junos_push_config](/roles/dana_junos_push_config/README.md)


## Playbook Variables

* `targets` (default value = `ip_underlay`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name

## Playbook Tags

* `push_config`: with this tag, upon generating the configurations, the playbook also loads and commits them to the 
corresponding remote devices. 

Example:

```
ansible-playbook pb_provision_ebgp_underlay.yml -i invenotry/hosts.ini -t push_config

```

## Example 1 - Basic

1. Create a group called `ip_underlay` in your inventory file whose members are the devices you want to be part of 
the OSPF underaly:

    ```
    # invenotry/hosts.ini 
    
    [ip_underlay]
    router-1
    router-2
    router-3
    ```
2. Run the playbook 

    ```
    ansible-playbook pb_provision_ospf_underlay.yml -i invenotry/hosts.ini
    ```

Result: The interfaces connecting the devices are configured with IP and OSPF. Files are stored in the following folder:

```
inventory
├── _ospf_underlay_configs
│   ├── ospf_underlay.router-1.conf
│   ├── ospf_underlay.router-2.conf
│   ├── ospf_underlay.router-3.conf
│   ├── ip_underlay.router-1.conf
│   ├── ip_underlay.router-2.conf
│   └── ip_underlay.router-3.conf
```

Each link is automatically configured with a different IP subnet.

Example of output configuration:

```
# ip_underlay.router-1.conf

interfaces {
    xe-0/0/1 {
        mtu 9216;
        unit 0 {
            family inet {
                address 10.100.0.0/31;
            }
        }
    }
    xe-0/0/2 {
        mtu 9216;
        unit 0 {
            family inet {
                address 10.100.0.2/31;
            }
        }
    }
}
```
```
# ospf_underlay.router-1.conf

protocols {
    ospf {
        area 0.0.0.0 {
            interface lo0.0 passive;
            
            interface xe-0/0/1.0 {
            interface-type p2p;
            }
            interface xe-0/0/2.0 {
            interface-type p2p;
            }
        }
    }
}
```


If you also want to push the configuration to the remote devices, run the playbook with the tag `push_config`

```
ansible-playbook pb_provision_ospf_underlay.yml -i invenotry/hosts.ini -t push_config
```

This will load (with _replace_ mode) and commit the configurations on the respective devices.

## Example 2 - Target Group

Suppose you already have a group called `net_core` that you wish to provision:

```
# invenotry/hosts.ini 

[net_core]
router-1
router-2
router-3
```

You can modify the variable `underlay_group` to be the desired target group:

1. Edit the variable to match that name:

    ```yaml
    # invenotry/group_vars/all.yml
    
    underlay_group: net_core
    ```

2. Run the playbook targeting that group

    ```
    ansible-playbook pb_provision_ospf_underlay.yml -i invenotry/hosts.ini -e "targets=net_core"
    ```

The output is analogous to the previous example.
