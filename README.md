# Ansible Collection - dholzer.vmware_vcd

Documentation for the collection.
```
---
- hosts: localhost
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:   
    - deploy_primary
    - deploy_nonprimary


- hosts: vcd
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:   
    - config_cmt_manage-config
    - config_global-properties
    - config_cipher
    - config_proxy
    - config_syslog
    - config_trust-infra-certs
    - config_java


- hosts: vcd-db
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:   
    - config_db_backup


- hosts: localhost
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:   
    - config_import_certificates
    - config_ir_vce
    - config_ir_nsxt
    - config_cr_network-pools
```