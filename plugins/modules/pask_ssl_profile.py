#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


profile_sni_inner_args = dict(
    server_name=dict(type='str'),
    status=dict(type='str')
)
profile_hsts_inner_args = dict(
    status=dict(type='str'),
    max_age=dict(type='str'),
    subdomain=dict(type='str')
)
profile_session_resumption_inner_args = dict(
    status=dict(type='str'),
    pool_size=dict(type='str'),
    timeout=dict(type='str')
)

module_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str'),
    certificate=dict(type='str'),
    sni=dict(type='dict', options=profile_sni_inner_args),
    hsts=dict(type='dict', options=profile_hsts_inner_args),
    session_resumption=dict(type='dict',
                            options=profile_session_resumption_inner_args),
    ciphers=dict(type='str'),
    prefer_server_cipher=dict(type='str'),
    cipher_protocols=dict(type='list', elements='str'),
    client_authentication=dict(type='str'),
    server_authentication=dict(type='str'),
    ocsp_stapling=dict(type='str'),
    dhparam=dict(type='str'),
    curve=dict(type='list', elements='str'),
    description=dict(type='str'),
)


name = 'ssl'
subname= 'profile'

class PaskSslProfile(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSslProfile, self).__init__(name, module_args)

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
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_profile = PaskSslProfile(name, module_args)
    ssl_profile.set_param()
    ssl_profile.run()
    ssl_profile.set_result()


if __name__ == '__main__':
    main()