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
    'status', 'region', 'revision', 'priority', 'bridge_forward_delay',
    'bridge_hello_time', 'bridge_max_age', 'bpdu_guard'
]

port_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    path_cost=dict(type='str')
)
instance_port_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    path_cost=dict(type='str')
)
instance_inner_args = dict(
    id=dict(type='str', required=True),
    vlan=dict(type='list', elements='str', required=True),
    msti_priority=dict(type='str'),
    port=dict(type='list', elemenets='dict', options=instance_port_inner_args)
)
module_args = dict(
    port=dict(type='list', elements='dict', options=port_inner_args),
    instance=dict(type='list', elements='dict', options=instance_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'mstp'


class PaskMstp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskMstp, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    mstp = PaskMstp(name, module_args)
    mstp.set_param()
    mstp.run()
    mstp.set_result()


if __name__ == '__main__':
    main()