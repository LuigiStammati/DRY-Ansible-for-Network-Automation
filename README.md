# DRY Ansible for Network Automation

__DRY Ansible for Network Automation (DANA)__ is a collection of Ansible roles and playbooks that allow you to provision,
 sketch and backup a network running Junos OS, without the need of manually feeding extra data to represent topology 
 links and interfaces.
 
This is achieved by leveraging a topology inspection role that automatically discovers every link, 
node and interface of a particular group in the inventory file. 


The primary goal of this project is to assist network engineers who need to deploy a testing environment 
quickly, reliably and with as few manual inputs as possible.

Another intent is to illustrate some examples of how open source building blocks such as Ansible, Python and Jinja2 
can be used in combination with Junos OS APIs.
 
 
Don't Repeat Yourself (DRY) is the core paradigm driving this project:

* __it is DRY__ : by breaking down atomic operations into Ansible roles that are then conveniently reused 
across easily consumable playbooks;
* __it keeps you DRY__: by freeing you from providing anything that can be automatically figured out about 
your network topology.


## Table of contents
* [Complete list of Features](#complete-list-of-features)
* [Quick Start Example](#quick-start-example---ebgp-underlay-provisioning)
* [Installation](#installation)
* [Usage](#usage)


## Complete List of Features

* Inspect a Junos OS network and automatically represent topology links and interfaces;
* Draw a sketch of the network topology and export it in PDF;
* Generate and provision OSPF underlay configuration;
* Generate and provision EBGP underlay configuration;
* Generate and provision multiple LAGs configuration;
* Backup all active configurations;
* Push multiple configuration files;


## Quick Start Example - EBGP Underlay Provisioning

Suppose you spent few hours in the lab cabling up the following network topology for testing purposes.

 ![test](docs/images/dana_quick_example_init_topology.png)
 
The switches only got your Lab default configuration, which includes management and loopback interfaces.  
 
Your ultimate goal is to configure an IP Fabric:

* Underlay IP connectivity on all fabric links, with a different IP subnet per link;
* EBGP as underlay routing protocol, with one private Autonomous System Number (ASN) per device to redistribute the 
loopback addresses across the fabric;
* Load balancing enabled in the control and forwarding plane.

The playbook _pb_provision_ebgp_underlay_ is what you need:

1. Create a group called `ip_underlay` in your inventory file (_hosts.ini_) in which you include the devices that must be 
part of the fabric (this will be the only input from your side):


```
# hosts.ini

[ip_underlay]
qfx5120-1
qfx5120-2 
qfx5120-3
qfx5120-4
qfx5200-1
qfx5200-2
```

2. Run the playbook:

```
ansible-playbook pb_provision_ebgp_underlay.yml -i hosts.ini -t push_config
```

The tag `push_config` tells the playbook to both generate and commit the configuration to the remote devices. 
You can omit this tag if you only want to generate the files locally. They will be stored in a folder 
_\_ebgp_underlay_config_ in your inventory directory.

3. Enjoy the final result!

![test](docs/images/dana_quick_example_final_topology.png)

A quick summary of what just happened:

1. Links and neighbours connecting the members of the ip_underlay group have been automatically discovered, while Links 
to devices outside the group (the EX switches in this example) have been safely ignored;
2. IP addresses, interfaces and ASNs have been automatically generated from default seed values (that can be customised);
3. A configuration file for each device involved has been generated accordingly, stored in a local folder and finally 
pushed to the remote devices.

You can find out more about how the discovery is carried out and how you can tune the default variables to suite your 
needs in the [Usage](#usage) section of the documentation below.

The leaf device qfx5120-1 in this example will be provisioned with the following configuration:

```
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
protocols {
    bgp {
        group ebgp-underlay {
                type external;
                family inet {
                unicast;
                }
                multipath {
                    multiple-as;
                }
                export pl-local_loopback;
                local-as 4200000101;
    
                neighbor 10.100.0.1 {
                    description qfx5200-1;
                    peer-as 4200000106;
                }
                neighbor 10.100.0.3 {
                    description qfx5200-2;
                    peer-as 4200000105;
                }
            }
        }
}
```


```

policy-options {
    policy-statement pl-local_loopback {
        term 1 {
            from {
                protocol direct;
                interface lo0.0;
            }
            then accept;
        }
    }

    policy-statement ECMP {
        then {
            load-balance per-packet;
        }
    }
}

routing-options {
    forwarding-table {
        export ECMP;
    }
}
```


## Installation 

On the machine that you want to use as Ansible controller 
(can be your laptop or a dedicated server/VM):

1. Clone or download this repository;
2. Make sure Python 3.7 (or above) is installed, or create and activate a Python 3
 [virtual environment](https://docs.python.org/3/tutorial/venv.html) (recommended);
3. Install the requirements 

    ```
    pip install -r requirements.txt
    ```
    
At this point you are ready to execute the playbooks. 


## Usage

Each individual operation is defined as a custom Ansible role. 
Roles are then imported across different ready-to-use playbooks.

You can use this project in two ways:

* Run one of the playbooks;
* Write your own playbook and import one or more custom roles.


### Playbooks

You can check each individual playbook documentation for more details and examples:

* [pb_backup_config.yml](/docs/playbook-docs/pb_backup_config_README.md): Backup all active configurations in a single 
folder;
* [pb_sketch_topology.yml](docs/playbook-docs/pb_sketch_topology_README.md): Discover the network topology 
(or a subset of it) and generate a PDF diagram with a sketch of nodes, links and interfaces; 
* [pb_provision_ip_underlay.yml](docs/playbook-docs/pb_provision_ip_underlay_README.md): Discover the network topology 
and then generate the Junos configuration for underlay IP connectivity.
* [pb_provision_ebgp_underlay.yml](/docs/playbook-docs/pb_provision_ebgp_underlay_README.md): Discover the network 
topology and then generate the Junos configuration for underlay IP connectivity and EBGP peering over the physical 
interfaces;
* [pb_provision_ospf_underlay.yml](/docs/playbook-docs/pb_provision_ospf_underlay_README.md): Discover the network 
topology and then generate the Junos configuration for underlay IP connectivity and OSPF over the physical interfaces;
* [pb_push_config.yml](/docs/playbook-docs/pb_push_config_README.md): Load and commit one or more configuration files 
from a local folder to the corresponding remote devices, identified by the config file name.
* [pb_provision_lag.yml](/docs/playbook-docs/pb_provision_lag_README.md): Automatically generates the Junos 
configuration for one or more aggregated interfaces without requiring any interface name to be fed as input.


### Roles

* [dana_junos_topology_inspector](roles/dana_junos_topology_inspector/README.md)
* [dana_junos_push_config](roles/dana_junos_push_config/README.md)
* [dana_junos_backup_config](roles/dana_junos_backup_config/README.md)
* [dana_topology_diagram](roles/dana_topology_diagram/README.md)
* [dana_junos_ip_underlay](roles/dana_junos_ip_underlay/README.md)
* [dana_junos_ebgp_underlay](roles/dana_junos_ebgp_underlay/README.md)
* [dana_junos_ospf_underlay](roles/dana_junos_ospf_underlay/README.md)
* [dana_junos_lag](roles/dana_junos_lag/README.md)