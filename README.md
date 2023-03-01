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
    - config_global-roles
 
 
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
    - name: SCOrgAdmin_RO
      description: Swisscom customized read only role for Organization Administrators
      readonly: false
      publishAll: true
      rights:
        - 'Access All Organization VDCs'
        - 'Catalog: View ACL'
        - 'Catalog: View Private and Shared Catalogs'
        - 'Catalog: View Published Catalogs'
        - 'General: Administrator View'
        - 'Hybrid Cloud Operations: View from-the-cloud tunnel'
        - 'Hybrid Cloud Operations: View to-the-cloud tunnel'
        - 'Organization Network: View'
        - 'Organization vDC Compute Policy: View'
        - 'Organization vDC Distributed Firewall: View Rules'
        - 'Organization vDC Gateway: View BGP Routing'
        - 'Organization vDC Gateway: View DHCP'
        - 'Organization vDC Gateway: View DNS'
        - 'Organization vDC Gateway: View Firewall'
        - 'Organization vDC Gateway: View IPSec VPN'
        - 'Organization vDC Gateway: View L2 VPN'
        - 'Organization vDC Gateway: View Load Balancer'
        - 'Organization vDC Gateway: View NAT'
        - 'Organization vDC Gateway: View OSPF Routing'
        - 'Organization vDC Gateway: View Remote Access'
        - 'Organization vDC Gateway: View SSL VPN'
        - 'Organization vDC Gateway: View Static Routing'
        - 'Organization vDC Gateway: View'
        - 'Organization vDC Named Disk: View Properties'
        - 'Organization vDC Network: View Properties'
        - 'Organization vDC: View ACL'
        - 'Organization vDC: View CPU and Memory Reservation'
        - 'Organization vDC: View'
        - 'Organization: View'
        - 'UI Plugins: View'
        - 'vApp Template / Media: View'
        - 'vApp: View ACL'
        - 'vApp: View VM metrics'

    - name: SCOrgAdmin
      description: Swisscom customized role for Organization Administrators
      readonly: false
      publishall: true
      rights:
        - 'Access All Organization VDCs'
        - 'Catalog: Add vApp from My Cloud'
        - 'Catalog: Change Owner'
        - 'Catalog: CLSP Publish Subscribe'
        - 'Catalog: Create / Delete a Catalog'
        - 'Catalog: Edit Properties'
        - 'Catalog: Sharing'
        - 'Catalog: View ACL'
        - 'Catalog: View Private and Shared Catalogs'
        - 'Catalog: View Published Catalogs'
        - 'Certificate Library: View'
        - 'General: Administrator Control'
        - 'General: Administrator View'
        - 'General: Send Notification'
        - 'Group / User: View'
        - 'Hybrid Cloud Operations: Acquire control ticket'
        - 'Hybrid Cloud Operations: Acquire from-the-cloud tunnel ticket'
        - 'Hybrid Cloud Operations: Acquire to-the-cloud tunnel ticket'
        - 'Hybrid Cloud Operations: Create from-the-cloud tunnel'
        - 'Hybrid Cloud Operations: Create to-the-cloud tunnel'
        - 'Hybrid Cloud Operations: Delete from-the-cloud tunnel'
        - 'Hybrid Cloud Operations: Delete to-the-cloud tunnel'
        - 'Hybrid Cloud Operations: Update from-the-cloud tunnel endpoint tag'
        - 'Hybrid Cloud Operations: View from-the-cloud tunnel'
        - 'Hybrid Cloud Operations: View to-the-cloud tunnel'
        - 'Organization Network: Edit Properties'
        - 'Organization Network: View'
        - 'Organization vDC Compute Policy: View'
        - 'Organization vDC Distributed Firewall: Configure Rules'
        - 'Organization vDC Distributed Firewall: Enable/Disable'
        - 'Organization vDC Distributed Firewall: View Rules'
        - 'Organization vDC Gateway: Configure BGP Routing'
        - 'Organization vDC Gateway: Configure DHCP'
        - 'Organization vDC Gateway: Configure DNS'
        - 'Organization vDC Gateway: Configure Firewall'
        - 'Organization vDC Gateway: Configure IPSec VPN'
        - 'Organization vDC Gateway: Configure L2 VPN'
        - 'Organization vDC Gateway: Configure Load Balancer'
        - 'Organization vDC Gateway: Configure NAT'
        - 'Organization vDC Gateway: Configure OSPF Routing'
        - 'Organization vDC Gateway: Configure Remote Access'
        - 'Organization vDC Gateway: Configure SSL VPN'
        - 'Organization vDC Gateway: Configure Static Routing'
        - 'Organization vDC Gateway: Configure Syslog'
        - 'Organization vDC Gateway: Distributed Routing'
        - 'Organization vDC Gateway: View'
        - 'Organization vDC Gateway: View BGP Routing'
        - 'Organization vDC Gateway: View DHCP'
        - 'Organization vDC Gateway: View DNS'
        - 'Organization vDC Gateway: View Firewall'
        - 'Organization vDC Gateway: View IPSec VPN'
        - 'Organization vDC Gateway: View L2 VPN'
        - 'Organization vDC Gateway: View Load Balancer'
        - 'Organization vDC Gateway: View NAT'
        - 'Organization vDC Gateway: View OSPF Routing'
        - 'Organization vDC Gateway: View Remote Access'
        - 'Organization vDC Gateway: View SSL VPN'
        - 'Organization vDC Gateway: View Static Routing'
        - 'Organization vDC Named Disk: Change Owner'
        - 'Organization vDC Named Disk: Create'
        - 'Organization vDC Named Disk: Delete'
        - 'Organization vDC Named Disk: Edit Properties'
        - 'Organization vDC Named Disk: View Properties'
        - 'Organization vDC Network: Edit Properties'
        - 'Organization vDC Network: View Properties'
        - 'Organization vDC Storage Profile: Set Default'
        - 'Organization vDC: Manage Firewall'
        - 'Organization vDC: View'
        - 'Organization vDC: View ACL'
        - 'Organization vDC: View CPU and Memory Reservation'
        - 'Organization vDC: VM-VM Affinity Edit'
        - 'Organization: Edit Leases Policy'
        - 'Organization: View'
        - 'Quota Policy Capabilities: View'
        - 'SSL Settings: View'
        - 'SSL: Test Connection'
        - 'UI Plugins: View'
        - 'vApp Template / Media: Copy'
        - 'vApp Template / Media: Create / Upload'
        - 'vApp Template / Media: Edit'
        - 'vApp Template / Media: View'
        - 'vApp Template: Checkout'
        - 'vApp Template: Download'
        - 'vApp: Change Owner'
        - 'vApp: Copy'
        - 'vApp: Create / Reconfigure'
        - 'vApp: Delete'
        - 'vApp: Download'
        - 'vApp: Edit Properties'
        - 'vApp: Edit VM Compute Policy'
        - 'vApp: Edit VM CPU'
        - 'vApp: Edit VM Hard Disk'
        - 'vApp: Edit VM Memory'
        - 'vApp: Edit VM Network'
        - 'vApp: Edit VM Properties'
        - 'vApp: Manage VM Password Settings'
        - 'vApp: Power Operations'
        - 'vApp: Sharing'
        - 'vApp: Snapshot Operations'
        - 'vApp: Use Console'
        - 'vApp: View ACL'
        - 'vApp: View VM metrics'
        - 'vApp: VM Boot Options'
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