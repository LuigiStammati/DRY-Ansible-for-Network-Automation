# Playbook - Sketch Topology Diagram

Playbook: pb_sketch_topology.yml

This playbook discovers the network topology (or a subset of it) and sketches nodes, links and interfaces which are 
drawn in a topology diagram exported as PDF.
 
## Requirements and Role Dependencies

The playbook relies on the following roles:

* [dana_junos_topology_inspector](/roles/dana_junos_topology_inspector/README.md)
* [dana_topology_diagram](/roles/dana_topology_diagram/README.md)

You can check the requirements on roles' documentation.

## Playbook Variables

* `targets` (default value = `all`): it is the _hosts_ parameter of the playbook, used to set the target hosts. 
It can be a group name or a device name


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

You can run the playbook with no input variables:

```
ansible-playbook pb_sketch_topology.yml -i invenotry/hosts.ini 
```


The output is a PDF file with a draft of your topology diagram that displays all nodes, links and interface names.

The PDF is stored in a folder _topology_diagram automatically created  in your inventory directory:
```
inventory
├── _topology_diagram
│   ├── topology_diagram.dot
│   └── topology_diagram.pdf
```

The topology_diagram.pdf will display a sketch of the topology like this:
![topo_diagram](/docs/images/dana_topology_diagram_pdf_output_example.png)

## Example 2

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
    ansible-playbook pb_sketch_topology.yml -i inventory/hosts.ini -e "targets=my_subset"
    ```
    
The topology_diagram.pdf will display a sketch of the selected subset of the topology like this:

![topo_diagram_sub](/docs/images/dana_topology_diagram_pdf_output_subset.png)
