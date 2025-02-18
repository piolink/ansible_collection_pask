#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


param_list = [
    'status', 'mode', 'bridge_forward_delay', 'bridge_hello_time',
    'bridge_max_age', 'priority', 'bpdu_guard'
]
port_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    path_cost=dict(type='str'),
    portfast=dict(type='str'),
    bpdu_guard=dict(type='str'),
    bpdu_filter=dict(type='str'),
    root_guard=dict(type='str')
)
vlan_port_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    path_cost=dict(type='str')
)
vlan_inner_args = dict(
    vlan_name=dict(type='str', required=True),
    instance=dict(type='str', required=True),
    bridge_forward_delay=dict(type='str'),
    bridge_hello_time=dict(type='str'),
    bridge_max_age=dict(type='str'),
    priority=dict(type='str'),
    port=dict(type='list', elements='dict', options=vlan_port_inner_args)
)
module_args = dict(
    port=dict(type='list', elements='dict', options=port_inner_args),
    vlan=dict(type='list', elements='dict', options=vlan_inner_args)
)


module_args.update(make_module_args(param_list))


name = 'pvstp'


class PaskPvstp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPvstp, self).__init__(name, module_args)
        self.exclude_underscore_params.add('vlan_name')

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    pvstp = PaskPvstp(name, module_args)
    pvstp.set_param()
    pvstp.run()
    pvstp.set_result()


if __name__ == '__main__':
    main()