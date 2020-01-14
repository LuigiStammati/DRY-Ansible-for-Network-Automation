# DANA - DRY Ansible for Network Automation

Inspect, sketch, provision and backup your Junos OS network 

Ansible is cool for Network Automation! However... very often before running a playbook you are requested to manually 
write down long YAML files to represent every single link of your topology...Alternatively, you usually must pre-enable
 some sort of discovery protocol on the box, such as LLDP, on every device involved... 
is that really the best Automation we can perform?

__DRY Ansible for Network Automation (DANA)__ is a collection of Ansible roles and playbooks that allow you to carry out 
complex network provisioning operations on devices running Junos OS, without requiring you to manually describe the 
details of your topology, or pre-enable any discovery protocol by yourself.

This is achieved by leveraging a core topology inspection custom role that automatically discovers and represents your 
network while only requiring you to specify a target group name in the inventory file. 


Don't Repeat Yourself (DRY) is the core paradigm driving this project:
* __it is DRY__ : by breaking down atomic operations into Ansible roles that are then conveniently combined and reused 
across easily consumable playbooks;
* __it keeps you DRY__: by freeing you from providing anything that can be automatically figured out about 
your network topology.

Complete list of Features:

* Sketch topology diagram and export as PDF
* Generate and provision OSPF underlay configuration 
* Generate and provision EBGP underlay configuration 
* Generate and provision LAG configuration 
* Backup all active configurations

For further details, please check the usage section below


## Quick Example - EBGP Underlay

Suppose you spent few hours in the lab cabling up the following network 
(a typical Data Center _Clos_ topology in this example).

 ![test](docs/images/dana_quick_example_init_topology.png)
 
The devices only got the default configuration, which includes management and loopback interfaces.  
 
Your ultimate goal is to configure an IP Fabric by provisioning:
* the underlay IP connectivity on all fabric links, 
* EBGP as underlay routing protocol with one private ASN per device to redistribute the loopback addresses across 
the fabric,
* load balancing 

The playbook _pb_provision_ebgp_underlay_ is what you need:

1. Create a group called `ip_underlay` in your inventory file (_hosts.ini_) in which you include the devices that are 
part of the fabric

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
2. Run the playbook `pb_provision_ebgp_underlay.yml`
    ```
    ansible-playbook pb_provision_ebgp_underlay.yml -i hosts.ini -t push_config"
    ```
    Note: The tag `push_config` just tells the playbook to both generate and commit the configuration to the remote devices. 
    You can omit this tag if you only want to generate the files locally. They will be stored in a folder 
    _\_ebgp_underlay_config_ in your inventory directory.

3. Enjoy the final result!

![test](docs/images/dana_quick_example_final_topology.png)

The playbook automatically inspects the topology to find out interfaces and neighbours for each device of 
the ip_underlay group. For more details about how the discovery is performed, you can check the documentation
 [dana_junos_topology_inspector](roles/dana_junos_topology_inspector/README.md). 

You don't need to enable LLDP: to carry out the discovery, the role configures it automatically and rollbacks the changes
after retrieving all the information needed.
 
Finally, it generates the IP and EBGP configuration for each device, stores the 
files in the _\_ebgp_underlay_config_ folder in your inventory directory and performs a _load merge + commit_ operation
 on the remote targets.


In this example, the first leaf device qfx5120-1 will be automatically provisioned with the following configuration:

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

### Virtualenv
To execute the playbooks locally it is recommended to run the project in a virtual environment. The following steps
describe the installation using Anaconda: 

1. Clone the repository 
2. Install Python 3.7
3. Install [Anaconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) 
4. Create a virtual environment with the requested Python version

    ```buildoutcfg
    conda create --name dry_ansible_venv python=3.7
    ```
5. Activate the virtual environment 
    
    ```buildoutcfg
    conda activate dry_ansible_venv
    ```

6. Install the requirements 
    
    ```buildoutcfg
    pip install -r requirements.txt
    ```

## Usage

Each individual operation is defined as an Ansible role and can be easily reused and combined
across different playbooks. The project already exposes a variety of playbooks.

In the following sections, we describe the operations available and the corresponding playbook to employ.

### Sketch Topology Diagram

This playbook first carries out a topology inspection using the role 
[dana_junos_topology_inspection](roles/dana_junos_topology_inspector/README.md). 
You can check the role documentation for more details.

Finally, it uses the results of the inspection as input to the role [dana_topology_diagram](roles/dana_topology_diagram/README.md). 

Make sure to install the requirements specified for the above roles.


Example of usage:
```
ansible-playbook pb_draw_topology.yml -i invenotry/hosts.ini 
```


This generates a PDF file with a draft of your topology diagram that displays all nodes, links and interface names.

The PDF is stored in a folder _topology_diagram created in your inventory directory:
```
inventory
├── _topology_diagram
│   ├── topology_diagram.dot
│   └── topology_diagram.pdf
```

The topology_diagram.pdf will display a sketch of the topology like this:
![test](docs/images/dana_topology_diagram_pdf_output_example.png)

To target a subset of devices:

1. Create a group in your inventory file

    ```
    # invenotry/hosts.ini 
    
    [my_subset]
    router-1
    router-2
    router-3
    
    ```

2. Set the variable `grouo_to_inspect` to the group name just created. 
This will make sure that only links connecting the members of the group will be discovered:

    ```yaml
    # invenotry/group_vars/all.yml
    
    group_to_inspect: my_subset
    
    ```
3. Run the playbook targeting the desired group
    
    ```
    ansible-playbook pb_draw_topology.yml -i inventory/hosts.ini -e "targets=my_subset"
    ```

### Provision IP Underlay 

This playbook generates underlay IP connectivity and EBGP peering over the physical interfaces to redistribute the 
loopback addresses.

Minimal Example

```
ansible-playbook pb_provision_ebgp_underlay.yml -i inventory/hosts.ini
```

Result:

Generate IP and EBGP configuration in the following folder

```
inventory
├── _ebgp_underlay_configs
│   ├── ebgp_underlay.router-1.conf
│   ├── ebgp_underlay.router-2.conf
│   ├── ebgp_underlay.router-3.conf
│   ├── ip_underlay.router-1.conf
│   ├── ip_underlay.router-2.conf
│   └── ip_underlay.router-3.conf
```





### Provision OSPF Underlay 

### Provision LAG interfaces

### Backup Active Configurations 
Backup active configurations and save the files in a folder. 
File names contain the corresponding device name, a timestamp and an optional label.

```
ansible-playbook pb_backup_config.yml -i inventory/hosts.ini 
```
