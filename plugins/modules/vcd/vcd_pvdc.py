ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: vcd_pvdc
short_description: Manage Provider VDC's states/operations in vCloud Director
description:
    - Manage Provider VDC's states/operations in vCloud Director
options:
    user:
        description:
            - vCloud Director user name
        type: str
    password:
        description:
            - vCloud Director user password
        type: str
    org:
        description:
            - vCloud Director organization
        type: str
    host:
        description:
            - vCloud Director host address
        type: str
    api_version:
        description:
            - Pyvcloud API version, required as float i.e 34 => 34.0
        type: float
    verify_ssl_certs:
        description:
            - whether to use secure connection to vCloud Director host
        type: bool
    provider_vdc_name:
        description:
            - The name of the new provider vdc
        type: str
    description:
        description:
            - The description of the new provider vdc
        type: str
    vcenter_name:
        description:
            - The name of the registered vCenter providing the resources for the new PVDC
        type: str
    nsxt_manager_name:
        description:
            - The name of the registered NSXT manager providing the network pool for the new PVDC
        type: str
    resource_pool_cluster_name:
        description:
            - The name of the vCenter cluster providing the resource pool for the new PVDC
              If not specified, a resource pool with name defined in resource_pool_name will be used from any cluster (if found).
              One or both of resource_pool_cluster_name and resource_pool_name have to be provided.
        type: str
    resource_pool_name:
        description:
            - The name of the vCenter resource pool for the new PVDC.
              If not specified, the default resource pool of the cluster will be used.
              One or both of resource_pool_cluster_name and resource_pool_name have to be provided.
        type: str
    storage_profiles:
        description:
            - List of vCenter storage profiles to add to this Provider VDC.
              Each item must specify the of an existing vCenter storage profile.
        type: list
    network_pool_name:
        description:
            - Reference to a network pool in the provider VDC
        type: str
    is_enabled:
        description:
            - True if this provider VDC is enabled
              else False
        type: bool
        default: true
    force_delete:
        description:
            - True to force deleting the PVDC.
              otherwise, if PVDC cannot be removed if in use.
        type: bool
    state:
        description:
            - state of new provider VDC ('present'/'absent'/'update').
            - One of state or operation has to be provided.
        type: str
        choices: ['present', 'absent', 'update']
    operation:
        description:
            - operation to be performed on provider vdc
            - One of state or operation has to be provided.
        type: str
        choices: ['list_pvdcs']
author:
    - mgutjahr@vmware.com
'''

EXAMPLES = '''
- name: Test with a message
  vcd_pvdc:
    user: testuser
    password: abcd
    org: system
    host: test.vcd.org
    api_version: 34.0
    verify_ssl_certs: False
    provider_vdc_name: "PVDC_NAME"
    description: "DESCRIPTION"
    storage_profiles:
      - "Profile 1"
      - "Profile 2"
    resource_pool_cluster_name: "VC cluster"
    resource_pool_name: "VC Resource Pool"
    highest_hw_version: "vmx-17"
    is_enabled: True
    force_delete: False
    state: "present"
'''

RETURN = '''
msg: success/failure message corresponding to pvdc state/operation
changed: true if resource has been changed else false
'''

import uuid
import time

from pyvcloud.vcd.client import NSMAP
from pyvcloud.vcd.platform import Platform
from pyvcloud.vcd.pvdc import PVDC
from pyvcloud.vcd.system import System
from pyvcloud.vcd.client import E
from pyvcloud.vcd.client import E_VMEXT
from pyvcloud.vcd.client import EntityType
from pyvcloud.vcd.client import RelationType
from pyvcloud.vcd.client import ResourceType

from ansible.module_utils.vcd import VcdAnsibleModule
from pyvcloud.vcd.exceptions import EntityNotFoundException
from pyvcloud.vcd.exceptions import BadRequestException
from pyvcloud.vcd.exceptions import OperationNotSupportedException


PVDC_STATES = ['present', 'absent', 'update']
PVDC_OPERATIONS = ['list_pvdcs']
MAX_RETRIES_CHECK_STORAGE_PROFILES = 6
RETRY_DELAY_CHECK_STORAGE_PROFILES = 10.0


def pvdc_argument_spec():
    return dict(
        provider_vdc_name=dict(type='str', required=False),
        description=dict(type='str', required=False, default=''),
        nsxt_manager_name=dict(type='str', required=False),
        vcenter_name=dict(type='str', required=False),
        storage_profiles=dict(type='list', required=False, default=[]),
        network_pool_name=dict(type='str', required=False),
        resource_pool_cluster_name=dict(type='str', required=False),
        resource_pool_name=dict(type='str', required=False),
        highest_hw_version=dict(type='str', required=False, default='vmx-17'),
        is_enabled=dict(type='bool', required=False, default=True),
        force_delete=dict(type='bool', required=False, default=False),
        state=dict(choices=PVDC_STATES, required=False),
        operation=dict(choices=PVDC_OPERATIONS, required=False)
    )


class Pvdc(VcdAnsibleModule):
    def __init__(self, **kwargs):
        super(Pvdc, self).__init__(**kwargs)
        sys_admin_resource = self.client.get_admin()
        self.system = System(self.client, admin_resource=sys_admin_resource)
        self.platform = Platform(self.client)

    def manage_states(self):
        state = self.params.get('state')
        if state == 'present':
            return self.create()

        if state == 'absent':
            return self.delete()

        if state == 'update':
            return self.update()

    def manage_operations(self):
        operation = self.params.get('operation')
        if operation == 'list_pvdcs':
            return self.list_pvdcs()

    def create(self):
        provider_vdc_name = self.params.get('provider_vdc_name')
        description = self.params.get('description')
        is_enabled = self.params.get('is_enabled')
        storage_profiles = self.params.get('storage_profiles')
        network_pool_name = self.params.get('network_pool_name')
        resource_pool_cluster_name = self.params.get('resource_pool_cluster_name')
        resource_pool_name = self.params.get('resource_pool_name')
        nsxt_manager_name = self.params.get('nsxt_manager_name')
        vcenter_name = self.params.get('vcenter_name')
        highest_hw_version = self.params.get('highest_hw_version')

        response = dict()
        response['changed'] = False

        try:
            pvdc = self.system.get_provider_vdc(provider_vdc_name)
        except EntityNotFoundException:
            self.wait_for_storage_profiles(vcenter_name, storage_profiles)

            pvdc = self.create_provider_vdc(vim_server_name=vcenter_name,
                                         resource_pool_name=resource_pool_name,
                                         resource_pool_cluster_name=resource_pool_cluster_name,
                                         storage_profiles=storage_profiles,
                                         pvdc_name=provider_vdc_name,
                                         is_enabled=is_enabled,
                                         description=description,
                                         highest_hw_vers=highest_hw_version,
                                         network_pool=network_pool_name,
                                         nsxt_manager_name=nsxt_manager_name)

            create_pvdc_task = pvdc.find('vcloud:Tasks', NSMAP).Task[0]
            self.execute_task(create_pvdc_task)

            response['msg'] = 'PVDC {} has been created'.format(provider_vdc_name)
            response['changed'] = True
        else:
            response['warnings'] = 'PVDC {} is already present'.format(provider_vdc_name)

        return response

    def wait_for_storage_profiles(self, vcenter_name, storage_profiles):
        all_profiles_exist = False
        retry_count = 0
        while not all_profiles_exist and retry_count < MAX_RETRIES_CHECK_STORAGE_PROFILES:
            vc_record = self.platform.get_vcenter(vcenter_name)
            vc_storage_profiles = self.client.get_linked_resource(
                vc_record,
                RelationType.DOWN,
                EntityType.VMW_STORAGE_PROFILES.value
            )
            vc_profile_list = []
            if vc_storage_profiles is not None and hasattr(vc_storage_profiles, '{' + NSMAP['vmext'] + '}VMWStorageProfile'):
                vc_profile_list = list(map(lambda p: p.attrib['name'], vc_storage_profiles.VMWStorageProfile))
            all_profiles_exist = True
            for profile_name in storage_profiles:
                if profile_name not in vc_profile_list:
                    all_profiles_exist = False

            if not all_profiles_exist:
                time.sleep(RETRY_DELAY_CHECK_STORAGE_PROFILES)
                retry_count += 1
            else:
                return True
        return False

    def create_provider_vdc(self,
                            vim_server_name,
                            resource_pool_name,
                            resource_pool_cluster_name,
                            storage_profiles,
                            pvdc_name,
                            is_enabled=None,
                            description=None,
                            highest_hw_vers=None,
                            network_pool=None,
                            nsxt_manager_name=None):
        """Create a Provider Virtual Datacenter.
        Fork of pyvcloud.platform.create_provider_vdc supporting nsxt network pool

        :param str vim_server_name: vim_server_name (VC name).
        :param str resource_pool_name: resource_pool_name for PVDC fresource pool.
        :param str resource_pool_cluster_name: name of the vc cluster providing the resource pool.
        :param list storage_profiles: (list): list of storageProfile names.
        :param str pvdc_name: name of PVDC to be created.
        :param bool is_enabled: flag, True to enable and False to disable.
        :param str description: description of pvdc.
        :param str highest_hw_vers: highest supported hw version number.
        :param str network_pool: name of network_pool.
        :param str nsxt_manager_name: name of nsx-t manager.

        :return: an object containing vmext:VMWProviderVdc XML element that
            represents the new provider VDC.

        :rtype: lxml.objectify.ObjectifiedElement
        """
        if (resource_pool_cluster_name is None or resource_pool_cluster_name != '') and \
          (resource_pool_name is None or len(resource_pool_name) <= 0):
          raise BadRequestException(
                        'One or both of resource_pool_cluster_name or resource_pool_name have to be specified.')

        vc_record = self.platform.get_vcenter(vim_server_name)
        vc_href = vc_record.get('href')
        rp_morefs = []
        if resource_pool_name is not None and resource_pool_name != '':
          rp_morefs = self.platform.get_resource_pool_morefs(vc_href,
                                                  [resource_pool_name])
        elif resource_pool_cluster_name is not None and resource_pool_cluster_name != '':
          rp_morefs = self.platform.get_resource_pool_morefs(vc_href,
                                                  [resource_pool_cluster_name])

        vmw_prov_vdc_params = E_VMEXT.VMWProviderVdcParams(name=pvdc_name)
        if description is not None:
            vmw_prov_vdc_params.append(E.Description(description))
        resource_pool_refs = E_VMEXT.ResourcePoolRefs()
        for rp_moref in rp_morefs:
            vim_object_ref = E_VMEXT.VimObjectRef()
            vim_object_ref.append(E_VMEXT.VimServerRef(href=vc_href))
            vim_object_ref.append(E_VMEXT.MoRef(rp_moref))
            vim_object_ref.append(E_VMEXT.VimObjectType('RESOURCE_POOL'))
            resource_pool_refs.append(vim_object_ref)
        vmw_prov_vdc_params.append(resource_pool_refs)
        vmw_prov_vdc_params.append(E_VMEXT.VimServer(href=vc_href))
        if nsxt_manager_name is not None:
            nsxt_manager_rec = self.platform.get_ref_by_name(ResourceType.NSXT_MANAGER,
                                                    nsxt_manager_name)
            nsxt_href = nsxt_manager_rec.get('href')
            vmw_prov_vdc_params.append(
                E_VMEXT.NsxTManagerReference(href=nsxt_href))
        if network_pool is not None:
            network_pool_rec = self.platform.get_ref_by_name(ResourceType.NETWORK_POOL,
                                                    network_pool)
            vx_href = network_pool_rec.get('href')
            vmw_prov_vdc_params.append(E_VMEXT.NetworkPool(href=vx_href))
        if highest_hw_vers is not None:
            vmw_prov_vdc_params.append(
                E_VMEXT.HighestSupportedHardwareVersion(highest_hw_vers))
        if is_enabled is not None:
            vmw_prov_vdc_params.append(E_VMEXT.IsEnabled(is_enabled))
        for storage_profile in storage_profiles:
            vmw_prov_vdc_params.append(E_VMEXT.StorageProfile(storage_profile))
        random_username_suffix = uuid.uuid4().hex
        default_user = 'USR' + random_username_suffix[:8]
        default_pwd = 'PWD' + random_username_suffix[:8]
        vmw_prov_vdc_params.append(E_VMEXT.DefaultPassword(default_pwd))
        vmw_prov_vdc_params.append(E_VMEXT.DefaultUsername(default_user))

        return self.client.post_linked_resource(
            self.platform.extension.get_resource(),
            rel=RelationType.ADD,
            media_type=EntityType.PROVIDER_VDC_PARAMS.value,
            contents=vmw_prov_vdc_params)

    def update(self):
        provider_vdc_name = self.params.get('provider_vdc_name')
        is_enabled = self.params.get('is_enabled')
        response = dict()
        response['changed'] = False

        try:
            pvdc_resource = self.system.get_provider_vdc(provider_vdc_name)

            pvdc_admin_resource = self.client.get_resource(pvdc_resource.admin_resource)
            if is_enabled:
                rel = RelationType.ENABLE
            else:
                rel = RelationType.DISABLE

            self.client.post_linked_resource(pvdc_admin_resource, rel, None, None)

            response['msg'] = 'PVDC {} has been updated'.format(provider_vdc_name)
            response['changed'] = True
        except OperationNotSupportedException:
            m = "PVDC {} may already in desired state"
            response['warnings'] = m.format(provider_vdc_name)

        return response

    def delete(self):
        provider_vdc_name = self.params.get('provider_vdc_name')
        response = dict()
        response['changed'] = False

        try:
            pvdc_resource = self.system.get_provider_vdc(provider_vdc_name)
        except EntityNotFoundException:
            response['warnings'] = 'PVDC {} is not present.'.format(provider_vdc_name)
            return
        except OperationNotSupportedException:
            pass

        delete_pvdc_task = self.client.delete_resource(pvdc_resource.get('href'), self.params.get('force_delete'))
        self.execute_task(delete_pvdc_task)
        response['msg'] = 'PVDC {} has been deleted.'.format(provider_vdc_name)
        response['changed'] = True

        return response

    def list_pvdcs(self):
        response = dict()
        response['changed'] = False
        response['msg'] = [pvdc.get('name') for pvdc in self.system.list_provider_vdcs()]

        return response


def main():
    argument_spec = pvdc_argument_spec()
    response = dict(msg=dict(type='str'))
    module = Pvdc(argument_spec=argument_spec, supports_check_mode=True)

    try:
        if module.check_mode:
            response = dict()
            response['changed'] = False
            response['msg'] = "skipped, running in check mode"
            response['skipped'] = True
        elif module.params.get('state'):
            response = module.manage_states()
        elif module.params.get('operation'):
            response = module.manage_operations()
        else:
            raise Exception('Please provide state/operation for resource')

    except Exception as error:
        response['msg'] = error.__str__()
        module.fail_json(**response)
    else:
        module.exit_json(**response)


if __name__ == '__main__':
    main()