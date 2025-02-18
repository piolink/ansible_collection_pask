#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


server_authentication_export_inner_args = dict(
    server_ip=dict(type='str', required=True),
    file_name=dict(type='str', required=True)
)

module_args = dict(
    id=dict(type='str', required=True),
    server_name=dict(type='str'),
    verify_depth=dict(type='str'),
    import_crt=dict(type='str'),
    export_crt=dict(type='list', elements='dict',
                    options=server_authentication_export_inner_args),
    import_crl=dict(type='str'),
    export_crl=dict(type='list', elements='dict',
                    options=server_authentication_export_inner_args),
)

required_if = [
    ("state", "present", ["server_name", "import_crt"])
    ]

name = 'ssl'
subname = 'server-authentication'

command_list = ['export_crt', 'import_crl', 'export_crl']

class PaskSslServerAuthentication(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskSslServerAuthentication, self).__init__(
            name, module_args, required_if)

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
            url = os.path.join(url, self.module.params['id'])
            if self.check_command(self.module.params, command_list):
                resp = self.prest.post(url, data)
            else:
                resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_server_authentication = PaskSslServerAuthentication(
        name, module_args, required_if)
    ssl_server_authentication.set_param()
    ssl_server_authentication.run()
    ssl_server_authentication.set_result()


if __name__ == '__main__':
    main()