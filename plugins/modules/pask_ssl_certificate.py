#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


import_inner_args = dict(
    protocol=dict(type='str'),
    tftp=dict(type='str'),
    sftp=dict(type='str'),
    scp=dict(type='str'),
    http=dict(type='str'),
    ssh_port=dict(type='str'),
    tftp_port=dict(type='str'),
    password=dict(type='str', no_log=True)
)
certificate_export_inner_args = dict(
    server_ip=dict(type='str', required=True),
    file_name=dict(type='str', required=True)
)

module_args = dict(
    name=dict(type='str', required=True),
    key=dict(type='str'),
    mode=dict(type='str'),
    cname=dict(type='str'),
    email=dict(type='str'),
    organization=dict(type='str'),
    organization_unit=dict(type='str'),
    country=dict(type='str'),
    # state 항목은 해당 이름을 예약어를 ansible에서 사용
    # certificate_state로 입력받아 state로 처리
    certificate_state=dict(type='str'),
    locality=dict(type='str'),
    expiration=dict(type='str'),
    ca_certificates=dict(type='str'),
    copy_crt=dict(type='str'),
    export_crt=dict(type='list', elements='dict',
                    options=certificate_export_inner_args),
    export_csr=dict(type='list', elements='dict',
                    options=certificate_export_inner_args),
    export_pfx=dict(type='list', elements='dict',
                    options=certificate_export_inner_args),
    export_pem=dict(type='list', elements='dict',
                    options=certificate_export_inner_args),
    export_der=dict(type='list', elements='dict',
                    options=certificate_export_inner_args),
)
module_args['import'] = {
    'type': 'dict',
    'options': import_inner_args
}

name = 'ssl'
subname = 'certificate'

command_list = ['export_crt', 'export_csr', 'export_pfx', 'export_pem',
                'export_der']

class PaskSslCertificate(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSslCertificate, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        if self.module.params['state'] == "absent":
            data = dict()
            data[subname] = self.make_data(self.module.params)
            if 'certificate-state' in data[subname]:
                data[subname]['state'] = data[subname].pop('certificate-state')
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            if 'certificate-state' in data:
                data['state'] = data.pop('certificate-state')
            url = os.path.join(url, self.module.params['name'])
            if self.check_command(self.module.params, command_list):
                resp = self.prest.post(url, data)
            else:
                resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_certificate = PaskSslCertificate(name, module_args)
    ssl_certificate.set_param()
    ssl_certificate.run()
    ssl_certificate.set_result()


if __name__ == '__main__':
    main()