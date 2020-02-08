
# Playbook - Provision IP Underlay 

Playbook name: _pb_provision_ip_underlay.yml_

This playbook first discovers the network topology, then it generates the Junos configuration for underlay IP 
connectivity.

## Requirements and Role Dependencies 

This Playbook relies on the following roles

* [dana_junos_ip_underlay](roles/dana_junos_ip_underlay/README.md)
* [dana_junos_push_config](roles/dana_junos_push_config/README.md)
* [dana_junos_lag](roles/dana_junos_lag/README.md)


## Playbook Variables

* `targets` (default value = `ip_underlay`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name

## Playbook Tags

* `push_config`: with this tag, upon generating the configurations, the playbook also loads and commits them to the 
corresponding remote devices. 

Example:

```
ansible-playbook pb_provision_ip_underlay.yml -i invenotry/hosts.ini -t push_config

```

## Example 1 - Basic

We assume you have an inventory folder structured as following:

```
inventory
├── group_vars
├── host_vars
└── hosts.ini
```

Your `hosts.ini` initially looks like this

```
# invenotry/hosts.ini

router-1
router-2
router-3
router-4
router-5
router-6
```

1. Create a group called `ip_underlay` in the inventory file whose members are the devices you want to be part of 
the IP underaly:

    ```
    # invenotry/hosts.ini 
    
    router-4
    router-5
    router-6

    [ip_underlay]
    router-1
    router-2
    router-3
    ```
    
2. Run the playbook with no further inputs:

    ```
    ansible-playbook pb_provision_ip_underlay.yml -i invenotry/hosts.ini
    ```
    

Result: 

IP configurations are generated for all members of the ip_underlay group. 
Files are stored in the following autogenerated folder:

```
inventory
├── _ip_underlay_configs
│   ├── ip_underlay.router-1.conf
│   ├── ip_underlay.router-2.conf
│   └── ip_underlay.router-3.conf
```

IP addresses and all the other parameters are using the default values. Following examples shows how to customize.

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

## Example 2 - Customize Link IP Subnets

Each link will be configured with a different IP subnet. By default the first subnet employed is `10.100.0.0/31`. 
You can use a different subnet by modifying the variable `ip_subnet_start`. Example:

```yaml
# invenotry/group_vars/all.yml

ip_subnet_start: "20.20.0.0/24"
```

The network mask determines the step when selecting the next subnet. In the above example, the first link will be 
configured with the subnet `20.20.0.0/24`, the second link with `20.20.1.0/24` 
and so on. 


