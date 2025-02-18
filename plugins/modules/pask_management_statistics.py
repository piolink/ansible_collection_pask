#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_default_args = dict(
    status=dict(type='str'),
    unit=dict(type='str'),
)

inner_client_ip_args = dict(
    status=dict(type='str'),
    interval=dict(type='str'),
    max_client=dict(type='str'),
)

module_args = dict(
    default=dict(type='dict', options=inner_default_args),
    client_ip=dict(type='dict', options=inner_client_ip_args),
)

name = 'management-statistics'

exclude_underscore_list = [
    'client_ip', 'max_client'
]


class PaskManagementStatistics(PaskModule):
    def __init__(self, name, module_args):
        super(PaskManagementStatistics, self).__init__(name, module_args)
        for exclude_underscore_param in exclude_underscore_list:
            self.exclude_underscore_params.add(exclude_underscore_param)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    management_statistics = PaskManagementStatistics(name, module_args)
    management_statistics.set_param()
    management_statistics.run()
    management_statistics.set_result()


if __name__ == '__main__':
    main()