#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


filter_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    type=dict(type='str'),
    command_type=dict(type='str', required=True),
    command_key=dict(type='str'),
    name_server_ip=dict(type='str'),
    name_server_ip6=dict(type='str')
)
peer_group_peer_inner_args = dict(
    ip=dict(type='str', required=True)
)
peer_group_interface_inner_args = dict(
    name=dict(type='str'),
    ip=dict(type='str')
)
peer_group_filter_inner_args = dict(
    id=dict(type='str', required=True)
)
peer_group_inner_args = dict(
    name=dict(type='str', required=True),
    status=dict(type='str'),
    mode=dict(type='str'),
    interval=dict(type='str'),
    peer=dict(type='list', elemenets='dict',
              options=peer_group_peer_inner_args),
    interface=dict(type='dict', options=peer_group_interface_inner_args),
    filter=dict(type='list', elemenets='dict',
                options=peer_group_filter_inner_args),
    interval_sync_type=dict(type='str'),
    description=dict(type='str')
)
sync_inner_args = dict(
    destination=dict(type='str', required=True),
    config_type=dict(type='str', required=True)
)
diff_inner_args = dict(
    destination=dict(type='str', required=True),
    config_type=dict(type='str', required=True)
)
module_args = dict(
    filter=dict(type='list', elements='dict', options=filter_inner_args),
    peer_group=dict(type='list', elements='dict',
                    options=peer_group_inner_args),
    sync=dict(type='list', elements='dict',
                        options=sync_inner_args),
    diff=dict(type='list', elements='dict',
                     options=diff_inner_args),
)

name = 'config-sync'

command_list = ['sync', 'diff']


class PaskConfigSync(PaskModule):
    def __init__(self, name, module_args):
        super(PaskConfigSync, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        if self.check_command(self.module.params, command_list):
            resp = self.prest.post(self.url, data)
        else:
            resp = self.prest.put(self.url, data)
        self.resp = resp


def main():
    config_sync = PaskConfigSync(name, module_args)
    config_sync.set_param()
    config_sync.run()
    config_sync.set_result()


if __name__ == '__main__':
    main()