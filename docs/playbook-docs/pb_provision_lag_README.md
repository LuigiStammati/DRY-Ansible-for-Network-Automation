
# Playbook - Provision LAG 

Playbook name: _pb_provision_lag.yml_

This playbook automatically generates the Junos configuration for one or more aggregated interfaces without 
requiring any interface name to be fed as input. 


## Requirements and Role Dependencies 

This Playbook relies on the following roles

* [dana_junos_lag](roles/dana_junos_lag/README.md)
* [dana_junos_push_config](roles/dana_junos_push_config/README.md)

## Playbook Variables

* `targets` (default value = `all`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name

## Playbook Tags

* `push_config`: with this tag, upon generating the configurations, the playbook also loads and commits them to the 
corresponding remote devices. 

Example:

```
ansible-playbook pb_provision_lag.yml -i invenotry/hosts.ini -t push_config

```

## Example 1 - Basic

You want to create a LAG interface on router-1 and router-2 to bundle together the interfaces over the links 
connecting them.


1. Create a group called `lag_bundle_0` in the inventory file whose members are the two devices involved:

```
# invenotry/hosts.ini 

[lag_bundle_0]
router-1
router-2
```
    
2. Run the playbook:

```
ansible-playbook pb_provision_lag.yml -i invenotry/hosts.ini
```


Result: 

The playbook discovers the interfaces connecting the devices and generate the configuration with an aggregate interface
called `ae0` that bundles together the physical interfaces. Configuration files are stored in a folder in the inventory
 file (`_lag_configs`):

```
inventory
├── _lag_configs
│   ├── lag.router-1.conf
│   ├── lag.router-2.conf
│   └── ip_underlay.router-3.conf
```

The folder can be customized by editing a role variables.


Example of output configuration generated:

```
# lag.router-1.conf

chassis {
    aggregated-devices {
        ethernet {
            device-count 1;
        }
    }
}


interfaces {
    xe-0/0/0 {
       ether-options {
           802.3ad ae0;
       }
    }
    
    xe-0/0/1 {
       ether-options {
           802.3ad ae0;
       }
    }
    
    ae0 {
        unit 0;
    }
}
```
The other device would have a similar configuration, with interface names possibly different.
 
Note that the aggregated interface `ae0` only contains an empty `unit 0`. The reason is that the major goal of the playbook 
is not to configure the aggregate itself, it is rather to automatically figure out which child interfaces must be 
bundle together and generate the corresponding configuration. 
  
After that, the aggregated interface will be available to be further configured either via CLI or using other playbooks.



## Example 2 - Multiple LAGs

In this example we have three devices and we want to create two LAG interfaces.

We can create a group in the inventory file for each LAG. Each group contains the pair of devices involved in that
 particular bundle and the number in the group name will be used as interface number.

```
# invenotry/hosts.ini 

[lag_bundle_0]
router-1
router-2

[lag_bundle_44]
router-1
router-3
```

In this example, the first group `lag_bundle_0` will be used to create an aggregate interface `ae0` on both router-1 
and router-2 that contains the physical interfaces connecting the routers. The group `lag_bundle_44` will instead create
an aggregate `ae44` on router-1 and router-2.


```
# lag.router-1.conf

chassis {
    aggregated-devices {
        ethernet {
            device-count 2;
        }
    }
}


interfaces {
    xe-0/0/0 {
       ether-options {
           802.3ad ae0;
       }
    }
    
    xe-0/0/1 {
       ether-options {
           802.3ad ae0;
       }
    }
    
    xe-0/0/2 {
       ether-options {
           802.3ad ae44;
       }
    }
    
    xe-0/0/3 {
       ether-options {
           802.3ad ae44;
       }
    }
    
    ae0 {
        unit 0;
    }
    
    ae44 {
        unit 0;
    }
}
```

The `device-count` under `chassis aggregated-devices ethernet` is automatically set to reflect the amount of aggregated 
interfaces configured. 


