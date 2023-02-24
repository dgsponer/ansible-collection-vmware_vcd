# Ansible Collection - dholzer.vmware_vcd

Documentation for the collection.

# inventory
```
localhost ansible_connection=local

[vcd]
vcd001  ansible_connection=ssh  ansible_host=172.16.0.26  ansible_ssh_user=root  ansible_password=VMwareVCD1.
vcd002  ansible_connection=ssh  ansible_host=172.16.0.27  ansible_ssh_user=root  ansible_password=VMwareVCD1.
vcd003  ansible_connection=ssh  ansible_host=172.16.0.28  ansible_ssh_user=root  ansible_password=VMwareVCD1.
vcd004  ansible_connection=ssh  ansible_host=172.16.0.29  ansible_ssh_user=root  ansible_password=VMwareVCD1.
vcd005  ansible_connection=ssh  ansible_host=172.16.0.30  ansible_ssh_user=root  ansible_password=VMwareVCD1.

[vcd-primary]
vcd001

[vcd-nonprimary]
vcd002
vcd003
vcd004
vcd005

[vcd-db]
vcd001
vcd002
vcd003
```

# site.yml
```
---
# Day1 - Deployment
- hosts: localhost
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:
    - api_session   
    - deploy_primary
    - deploy_nonprimary



# Day2 - DB-nodes
- hosts: vcd-db
  gather_facts: false
  collections:
    - dholzer.vmware_vcd
 
  roles:   
    - config_db_backup
 
 

# Day2 - VCD settings with API
- hosts: localhost
  gather_facts: false
  collections:
    - dholzer.vmware_vcd
 
  roles:
    - api_session   
    - config_import_certificates
    - config_ir_vce
    - config_ir_nsxt
    - config_cr_network-pools
    - config_license
    - config_roles
 
 
# Day2 - VCD settings with SSH
- hosts: vcd
  gather_facts: false
  collections:
    - dholzer.vmware_vcd

  roles:
    - config_cmt_manage-config
    - config_cipher
    - config_proxy
    - config_syslog
    - config_trust-infra-certs
    - config_global-properties
    - config_java
```

# var vcd
```
vcd:
  api_version: 37.1
  license: '00000-00000-00000-00000-00000'

  java_opts:
    xms: 2048
    xmx: 8192

  cipher:
    - TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
    - TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
    - TLS_RSA_WITH_AES_128_GCM_SHA256
    - TLS_RSA_WITH_AES_256_CBC_SHA256
    - TLS_ECDH_RSA_WITH_AES_256_CBC_SHA
    - TLS_RSA_WITH_AES_256_CBC_SHA
    - TLS_RSA_WITH_AES_128_CBC_SHA256
    - TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA
    - TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA
    - TLS_ECDH_RSA_WITH_AES_128_CBC_SHA
    - TLS_RSA_WITH_AES_128_CBC_SHA

  deployment:
    vce:
      hostname: 'base01-vce-01.vcloud24.net'
      username: 'administrator@vsphere.local'
      password: 'VMwareVCE1.'

    ova: 'VMware_Cloud_Director-10.4.1.9057-20912720_OVF10.ova'

    datacenter: 'base01'
    folder: '/vcd01'
    # to cluster 'base01'
    # to resource pool 'base01/Resources/vcd01'
    cluster: 'base01/Resources/vcd01'

    disk_provisioning: 'thin'
    datastore: 'qnap-ts879 vmw_vsphere'

    eth0:
      network: 'base01-0101mgmt'
      netmask: 255.255.255.192
      static_routes: ''
    
    eth1:
      network: 'base01-0101mgmt'
      netmask: 255.255.255.192
      static_routes: ''
    
    ntp_server: 172.16.0.1
    expire_root: false
    enable_ssh: true

    gateway: 172.16.0.1
    dns: 172.16.0.1
    domain: 'vcloud24.net'
    search: 'vcloud24.net'

    nfs_mount: '172.16.1.8:/nfsdata/test'
    db_password: 'VMwareVCD1.'
    instance_id: 1
    ceip: false
    admin:
      email: 'admin@mycompany.com'
      fullname: 'vCD Admin'
  password: 'VMwareVCD1.'
  username: 'administrator'

  cell:
    primary:
      - size: 'primary-extralarge'
        vm_name: 'psrv01vcd001.vcloud24.net'
        system_name: 'psrv01vcd001.vcloud24.net'
        root_password: 'VMwareVCD1.'
        eth0:
          ip: 172.16.0.26
        eth1:
          ip: 10.10.10.1

    nonprimary:
      - size: 'standby-extralarge'
        vm_name: 'psrv01vcd002.vcloud24.net'
        system_name: 'psrv01vcd002.vcloud24.net'
        root_password: 'VMwareVCD1.'
        eth0:
          ip: 172.16.0.27
        eth1:
          ip: 10.10.10.2

      - size: 'standby-extralarge'
        vm_name: 'psrv01vcd003.vcloud24.net'
        system_name: 'psrv01vcd003.vcloud24.net'
        root_password: 'VMwareVCD1.'
        eth0:
          ip: 172.16.0.28
        eth1:
          ip: 10.10.10.3

      - size: 'cell'
        vm_name: 'psrv01vcd004.vcloud24.net'
        system_name: 'psrv01vcd004.vcloud24.net'
        root_password: 'VMwareVCD1.'
        eth0:
          ip: 172.16.0.29
        eth1:
          ip: 10.10.10.4

      - size: 'cell'
        vm_name: 'psrv01vcd005.vcloud24.net'
        system_name: 'psrv01vcd005.vcloud24.net'
        root_password: 'VMwareVCD1.'
        eth0:
          ip: 172.16.0.30
        eth1:
          ip: 10.10.10.5

  # CMT Advanced Parameter
  advanced_settings:
    - parameter: ui.baseHttpUri
      value: 'http://psrv01vcd001.vcloud24.net'

    - parameter: ui.baseUri
      value: 'https://psrv01vcd001.vcloud24.net'

    - parameter: restapi.baseHttpUri
      value: 'http://psrv01vcd001.vcloud24.net'

    - parameter: restapi.baseUri
      value: 'https://psrv01vcd001.vcloud24.net'

    - parameter: managed-vapp.discovery.retry-delay-sec
      value: 300

    - parameter: VM_DISCOVERY_MIN_AGE_SEC
      value: 300

    - parameter: fabric.storage.placement.algorithm.existing.item.attempt.single.container.placement
      value: true

    - parameter: vdc.storageProfile.metrics.useCache
      value: false

    - parameter: backend.cloneBiosUuidOnVmCopy
      value: 0

    - parameter: extensibility.timeout
      value: 60

    - parameter: restapi.queryservice.maxPageSize
      value: 64

  # /opt/vmware/vcloud-director/etc/global.properties
  global_properties:
    - parameter: database.defaultQueryTimeout
      value: 300

    - parameter: database.pool.abandonWhenPercentageFull
      value: 0

    - parameter: database.pool.logAbandoned
      value: true

    - parameter: database.pool.maxActive
      value: 200

    - parameter: database.pool.maxIdle
      value: 75

    - parameter: database.pool.removeAbandoned
      value: true

    - parameter: database.pool.removeAbandonedTimeout
      value: 28800

    - parameter: database.pool.suspectTimeout
      value: 21600

    - parameter: inventory.cache.maxElementsInMemory
      value: 25000

    - parameter: vcloud.activities.fifoActivityQueueService.threadCount
      value: 64

    - parameter: vcloud.activities.taskActivityQueueRetentionMs
      value: 3600000

    - parameter: vcloud.activities.taskActivityQueueService.threadCount
      value: 64

    - parameter: vcloud.activities.valFabricActivityQueueService.threadCount
      value: 64

    - parameter: vcloud.http.maxThreads
      value: 200

    - parameter: vcloud.http.maxQueuedHttpRequests
      value: 200

    - parameter: vcloud.http.requestsBaseLine
      value: 100

    - parameter: vcloud.val.inventory.updateTimeout
      value: 120

    - parameter: vcloud.val.maxConcurrentValActivities
      value: 128

  roles:
    - name: Admin Role
      rights:
        #-
        #-
    - name: App Launchpad Role
      rights:
        #-
        #-

```

# var components
```
nsx:
  - hostname: 'lab01-ntm-01.vcloud24.net'
    username: 'admin'
    password: 'VMwareNSX1..'
    ip: 172.16.1.11

vce:
  - hostname: 'lab01-vce-01.vcloud24.net'
    username: 'administrator@vsphere.local'
    password: 'VMwareVCE1.'

syslog:
  hostname: psrv01log001.vcloud24.net
  port: 514

proxy:
  java_useSystemProxy: "false"
  enabled: "no"
  http_proxy: "http://psrvcm02pro0002.vcloud24.net"
  http_port: 8080
  https_proxy: "http://psrvcm02pro0002.vcloud24.net"
  https_port: 8080
  no_proxy: "localhost, 127.0.0.1, *.vcloud24.net"
```