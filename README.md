# Ansible Collection - dgsponer.vmware_vcd

Documentation for the collection.

# inventory
```
localhost ansible_connection=local

[vmw_vcd]
lab01-vcd-01.vcloud24.net  ansible_connection=ssh  ansible_host=172.16.1.7  ansible_ssh_user=root  ansible_password=VMwareVCD1.
lab01-vcd-02.vcloud24.net  ansible_connection=ssh  ansible_host=172.16.1.8  ansible_ssh_user=root  ansible_password=VMwareVCD1.
lab01-vcd-03.vcloud24.net  ansible_connection=ssh  ansible_host=172.16.1.9  ansible_ssh_user=root  ansible_password=VMwareVCD1.
lab01-vcd-04.vcloud24.net  ansible_connection=ssh  ansible_host=172.16.1.10  ansible_ssh_user=root  ansible_password=VMwareVCD1.
lab01-vcd-05.vcloud24.net  ansible_connection=ssh  ansible_host=172.16.1.11  ansible_ssh_user=root  ansible_password=VMwareVCD1.

[vmw_vcd_primary_db]
lab01-vcd-01.vcloud24.net

[vmw_vcd_db]
# lab01-vcd-01.vcloud24.net
lab01-vcd-02.vcloud24.net
lab01-vcd-03.vcloud24.net

[vmw_vcd_cell]
lab01-vcd-04.vcloud24.net
lab01-vcd-05.vcloud24.net
```

# site.yml
```
---
# Day1 - Deployment
# Primary
- hosts: vmw_vcd_db_primary
  vars:
    vcd_deployment_size: primary-small
  collections:
    - dgsponer.vmware_vcd

  roles:
    - vcd_deploy_primary

# Standby
- hosts: vmw_vcd_db:!vmw_vcd_db_primary
  vars:
    vcd_deployment_size: standby-small
  collections:
    - dgsponer.vmware_vcd

  roles:
    - vcd_deploy_primary

# Cell
- hosts: vmw_vcd_cell
  vars:
    vcd_deployment_size: cell
  collections:
    - dgsponer.vmware_vcd

  roles:
    - vcd_deploy_primary


# Day2 - Configure DB-Nodes
- hosts: vmw_vcd_db
  collections:
    - dgsponer.vmware_vcd
 
  roles:   
    - vcd_config_db_backup
  
  vars:
    ansible_ssh_user: root
    ansible_ssh_pass: "{{ vcd_root_password }}"

  
# Day2 - VCD settings 
- hosts: vmw_vcd[0]
  collections:
    - dgsponer.vmware_vcd
 
  roles:
    - vcd_api_session
    - vcd_config_feature-flag 
    - vcd_config_import_certificates
    - vcd_config_license
    - vcd_config_global-roles
    - vcd_config_cmt_manage-config
    - vcd_config_allowed-urls
    - vcd_config_ir_vce
    - vcd_config_ir_nsxt
    - vcd_config_pvdcs
    - vcd_config_placement-policy
    - vcd_config_cr_network-pools

  vars:
    ansible_ssh_user: root
    ansible_ssh_pass: "{{ vcd_root_password }}"


# Day2 - VCD settings 
- hosts: vmw_vcd
  collections:
    - dgsponer.vmware_vcd
 
  roles:
    - vcd_config_syslog
    - vcd_monitoring-vami
    - vcd_config_global-properties
    - vcd_config_trust-infra-certs
    - vcd_config_cipher
    - vcd_config_proxy
    - vcd_config_java

  vars:
    ansible_ssh_user: root
    ansible_ssh_pass: "{{ vcd_root_password }}"
```

# var vcd
```
vcd:
  api_version: 38.0
  license: '00000-00000-00000-00000-00000'

  allowed_urls:
    - "vcd.vcloud24.net"
    - "api-vcd.vcloud24.net"

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
    host: localhost
    chdir: /root/repository
    ova: 'VMware_Cloud_Director-10.5.0.9946-22080476_OVF10.ova'

    vce:
      hostname: 'base01-vce-01.vcloud24.net'
      username: 'administrator@vsphere.local'
      password: 'VMwareVCE1.'

    datacenter: 'base01'
    folder: '/vcd01'
    # to cluster 'base01'
    # to resource pool 'base01/Resources/vcd01'
    cluster: 'base01/Resources/vcd01'

    disk_provisioning: 'thin'
    datastore: 'ds-base01-nfs-01_vmw-vsphere_bkp'

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
    - name: OrgAdmin_RO
      description: customized read only role for Organization Administrators
      readonly: false
      publishAll: true
      rights:
        - 'Access All Organization VDCs'
        - 'Catalog: View ACL'
        - 'Catalog: View Private and Shared Catalogs'
        - 'Catalog: View Published Catalogs'
        - 'General: Administrator View'
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

    - name: OrgAdmin
      description: customized role for Organization Administrators
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

  feature_flag:
    - name: BRANDING_THEME
      enabled: true
    - name: FAST_CROSS_VC_INSTANTIATION
      enabled: true
    - name: K8S_UNIFIED
      enabled: true
    - name: THREE_PERSONAS
      enabled: true
    - name: TRANSFER_SESSION_API
      enabled: true

  pvdcs:
    - name: siteA
      description: siteA
      state: present
      is_enable: true
      clustername: lab01
      resourcepool: vcd_siteA
      hw_version: vmx-19
      network_pool_name: nsx-overlay-transportzone
      storage:
        - vmw_vsphere
        - vmw_vsphere_bkp

    - name: siteB
      description: siteB
      state: present
      is_enable: true
      clustername: lab01
      resourcepool: vcd_siteB
      hw_version: vmx-19
      network_pool_name: nsx-overlay-transportzone
      storage:
        - vmw_vsphere
        - vmw_vsphere_bkp

    - name: stretchedAB
      description: stretchedAB
      state: present
      is_enable: true
      clustername: lab01
      resourcepool: vcd_stretchedAB
      hw_version: vmx-19
      network_pool_name: nsx-overlay-transportzone
      storage:
        - vmw_vsphere
        - vmw_vsphere_bkp

    - name: stretchedBA
      description: stretchedBA
      state: present
      is_enable: true
      clustername: lab01
      resourcepool: vcd_stretchedBA
      hw_version: vmx-19
      network_pool_name: nsx-overlay-transportzone
      storage:
        - vmw_vsphere
        - vmw_vsphere_bkp

  vm_placement_policies:
    - name: wss-az1
      description: 'SingleSite AZ1'
      pvdc: vce-01-001
      vmgroups:
        - grp-vm-wss-az1

    - name: wss-az2
      description: 'SingleSite AZ2'
      pvdc: vce-01-001
      vmgroups:
        - grp-vm-wss-az2

    - name: wss-az3
      description: 'SingleSite AZ3'
      pvdc: vce-01-001
      vmgroups:
        - grp-vm-wss-az3

    - name: wms-az1
      description: 'MultiSite preferred AZ1'
      pvdc: vce-01-001
      vmgroups:
        - grp-vm-wms-az1

    - name: wms-az2
      description: 'MultiSite preferred AZ2'
      pvdc: vce-01-001
      vmgroups:
        - grp-vm-wms-az2
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
