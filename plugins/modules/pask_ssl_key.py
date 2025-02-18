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
key_export_pem_inner_args = dict(
    server_ip=dict(type='str', required=True),
    file_name=dict(type='str', required=True)
)
key_export_der_inner_args = dict(
    server_ip=dict(type='str', required=True),
    file_name=dict(type='str', required=True)
)

module_args = dict(
    name=dict(type='str', required=True),
    mode=dict(type='str'),
    type=dict(type='str'),
    length=dict(type='str'),
    curve=dict(type='str'),
    encryption=dict(type='str'),
    passphrase=dict(type='str', no_log=True),
    copy_key=dict(type='str'),
    export_pem=dict(type='list', elements='dict',
                    options=key_export_pem_inner_args),
    export_der=dict(type='list', elements='dict',
                    options=key_export_der_inner_args)
)
module_args['import'] = {
    'type': 'dict',
    'options': import_inner_args
}

name = 'ssl'
subname = 'key'


command_list = ['export_pem', 'export_der']


class PaskSslKey(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSslKey, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        if self.module.params['state'] == "absent":
            data = dict()
            data[subname] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(url, self.module.params['name'])
            if self.check_command(self.module.params, command_list):
                resp = self.prest.post(url, data)
            else:
                resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_key = PaskSslKey(name, module_args)
    ssl_key.set_param()
    ssl_key.run()
    ssl_key.set_result()


if __name__ == '__main__':
    main()