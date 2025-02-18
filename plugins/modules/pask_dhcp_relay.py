#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


ip_inner_args = dict(
    serverip=dict(type='str', required=True)
)

interface_inner_args = dict(
    name=dict(type='str', required=True)
)

module_args = dict(
    ip=dict(type='list', elements='dict', options=ip_inner_args),
    interface=dict(type='list', elements='dict', options=interface_inner_args),
    **make_module_args(
        ["status", "option"])
)

name = 'dhcp-relay'


class PaskDhcpRelay(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDhcpRelay, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    dhcp_relay = PaskDhcpRelay(name, module_args)
    dhcp_relay.set_param()
    dhcp_relay.run()
    dhcp_relay.set_result()


if __name__ == '__main__':
    main()
