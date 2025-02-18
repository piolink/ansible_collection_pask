#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_ssh_args = dict(
    status=dict(type='str'),
    port=dict(type='str'),
    security_level=dict(type='str'),
)

inner_telnet_args = dict(
    status=dict(type='str'),
    port=dict(type='str'),
)

inner_http_args = dict(
    status=dict(type='str'),
    port=dict(type='str'),
)

inner_https_args = dict(
    status=dict(type='str'),
    port=dict(type='str'),
    ssl=dict(type='str'),
)

inner_prest_api_args = dict(
    status=dict(type='str'),
    port=dict(type='str'),
    ssl=dict(type='str'),
    cipher_protocols=dict(type='str'),
)

module_args = dict(
    ssh=dict(type='dict', options=inner_ssh_args),
    telnet=dict(type='dict', options=inner_telnet_args),
    http=dict(type='dict', options=inner_http_args),
    https=dict(type='dict', options=inner_https_args),
    prest_api=dict(type='dict', options=inner_prest_api_args)
)


name = 'management-access'


class PaskManagementAccess(PaskModule):
    def __init__(self, name, module_args):
        super(PaskManagementAccess, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    management_access = PaskManagementAccess(name, module_args)
    management_access.set_param()
    management_access.run()
    management_access.set_result()


if __name__ == '__main__':
    main()