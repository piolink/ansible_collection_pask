# Piolink PAS-K Ansible Collection
The Collection is the Piolink PAS-K Ansible Automation project.
It includes the modules that are able to configure PAS-K machine's settings.

# Installation
This collection is distributed via [ansible-galaxy](https://galaxy.ansible.com/), the installation steps are as follows:

1. Install or upgrade to Ansible 2.9+
2. Download this collection from galaxy: `ansible-galaxy collection install piolink.pask`

# Requirements
* Ansible 2.9+ is required to support the newer Ansible Collections format
* requests module
* netaddr module

# Usage
The following example is used to configure DNS setting of the PAS-K.

playbook example(pask_dns.yml):
```yaml
---
- name: Dns Test
  hosts: all
  connection: local
  collections:
  - piolink.pask

  tasks:
  - name: create dns ip
    pask_dns:
      prest_ip: "{{ansible_host}}"
      prest_port: "{{ansible_port}}"
      user_id: "{{user_id}}"
      user_pw: "{{user_pw}}"
      retry: "5"
      timeout: "10"
      id:
        - { id: "1", ip: "192.168.203.100" }
        - { id: "2", ip: "8.8.8.8" }
```
Run the playbook command:
```bash
ansible-playbook pask_dns.yml
```
