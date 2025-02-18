#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_server_facility_args = dict(
    facility=dict(type='str', required=True),
    level=dict(type='str'),
    agent_facility=dict(type='str')
)

inner_server_args = dict(
    ipaddr=dict(type='str', required=True),
    port=dict(type='str'),
    facility=dict(
        type='list', elements='dict', options=inner_server_facility_args),
    description=dict(type='str')
)

param_list = [
    'facility', 'level', 'buffer', 'server_status'
]
module_args = dict(
    server=dict(type='list', elements='dict', options=inner_server_args)
)


module_args.update(make_module_args(param_list))

name = 'logging'


class PaskLogging(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLogging, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    logging = PaskLogging(name, module_args)
    logging.set_param()
    logging.run()
    logging.set_result()


if __name__ == '__main__':
    main()