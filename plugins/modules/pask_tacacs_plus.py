#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_server_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str'),
    status=dict(type='str'),
    description=dict(type='str')
)

param_list = [
    'authentication', 'authorization', 'accounting',
    'timeout', 'service', 'ssh', 'telnet', 'console', 'web', 'prest_api',
    'root_authentication', 'status', 'log'
]
module_args = dict(
    server=dict(type='list', elements='dict', options=inner_server_args),
    secret=dict(type='str', no_log=True)
)


module_args.update(make_module_args(param_list))


name = 'tacacs-plus'


class PaskTacacsPlus(PaskModule):
    def __init__(self, name, module_args):
        super(PaskTacacsPlus, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    tacacs_plus = PaskTacacsPlus(name, module_args)
    tacacs_plus.set_param()
    tacacs_plus.run()
    tacacs_plus.set_result()


if __name__ == '__main__':
    main()