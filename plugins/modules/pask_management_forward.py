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
    'backup', 'dns', 'email_alarm', 'logging', 'ntp', 'snmp_trap', 'radius'
]
custom_inner_args = dict(
    id=dict(type='str', required=True),
    dip=dict(type='str', required=True),
    dport=dict(type='str'),
    description=dict(type='str')
)
module_args = dict(
    custom=dict(type='list', elements='dict', options=custom_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'management-forward'


class PaskManagementForward(PaskModule):
    def __init__(self, name, module_args):
        super(PaskManagementForward, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    management_forward = PaskManagementForward(name, module_args)
    management_forward.set_param()
    management_forward.run()
    management_forward.set_result()


if __name__ == '__main__':
    main()