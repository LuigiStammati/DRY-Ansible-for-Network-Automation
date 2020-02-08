Topology Diagram
=========

This role draws a sketch of the topology diagram and makes it available in a PDF file. 

It expects a variable representing the topology nodes and links as input.

Requirements and Role Dependencies
------------

You need to install [graphviz](http://www.graphviz.org/download/) on the Ansible controller.

Role Variables
--------------

* __topology_diagram_dir__ (default `"{{ inventory_dir }}/_topology_diagram"`): The path to
the directory in which the PDF file will be saved. If the folder specified does 
not exist, it will be automatically created.
* __topology_links__: a data structure representing the links of the topology to be drawn. 
An example in JSON format of the expected structure:

```
[
    {
        source: {
            node: {
                name: str
            }
            interface: {
                name: str,
            }
        },
        target: {
            node: {
                name: str
            }
            interface: {
                name: str
            }
        }
    },
    {
        source: {
            node: {
                name: str
            }
            interface: {
                name: str,
            }
        },
        target: {
            node: {
                name: str
            }
            interface: {
                name: str
            }
        }
    } 
        
]
```


Example Playbook
----------------

```
# my_playbook.yml

- name: Sketch topology diagram
  hosts: all
  connection: local
  gather_facts: no
  tasks:
    - name: Sketch topology diagram
      include_role:
        name: dana_topology_diagram
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

