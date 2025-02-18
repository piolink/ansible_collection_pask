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
    'default_mgmt_ip', 'socket', 'memory', 'disk', 'swap', 'status',
    'repair', 'rate_limit'
]
ssl_hw_accel_inner_args = dict(
    status=dict(type='str'),
    mode=dict(type='str'),
    dev=dict(type='str'),
)

module_args = dict(
    name=dict(type='str', required=True),
    profile=dict(type='str'),
    mcpu=dict(type='list', elements='str'),
    cpu=dict(type='list', elements='str'),
    vlan=dict(type='list', elements='str'),
    ssl_hw_accel=dict(type='dict', options=ssl_hw_accel_inner_args)
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["profile", "cpu"])
    ]

name = 'vinstance'

command_list = ['repair']


class PaskVinstance(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskVinstance, self).__init__(name, module_args, required_if)
        self.exclude_underscore_params.add('ssl_hw_accel')

    @try_except
    def run(self):
        url = os.path.join(self.url)
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
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
    vinstance = PaskVinstance(name, module_args, required_if)
    vinstance.set_param()
    vinstance.run()
    vinstance.set_result()


if __name__ == '__main__':
    main()