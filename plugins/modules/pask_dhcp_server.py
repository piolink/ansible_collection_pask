#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


subnet_fixedaddr_inner_args = dict(
    hostname=dict(type='str', required=True),
    **make_module_args(
        ["client_mac", "client_ip"])
)

subnet_range_inner_args = dict(
    ip=dict(type='str'),
    id=dict(type='str', required=True)
)

subnet_inner_args = dict(
    fixedaddr=dict(type='list', elements='dict', options=subnet_fixedaddr_inner_args),
    range=dict(type='list', elements='dict', options=subnet_range_inner_args),
    dns=dict(type='list', elements='str'),
    id=dict(type='str', required=True),
    **make_module_args(
        ["subnet", "lease_time", "default_gateway"])
)

module_args = dict(
    status=dict(type='str'),
    interface=dict(type='list', elements='str'),
    subnet=dict(type='list', elements='dict', options=subnet_inner_args)
)

name = 'dhcp-server'


class PaskDhcpServer(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDhcpServer, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    dhcp_server = PaskDhcpServer(name, module_args)
    dhcp_server.set_param()
    dhcp_server.run()
    dhcp_server.set_result()


if __name__ == '__main__':
    main()
