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
    'status', 'agent_ip', 'polling_interval'
]
collector_inner_args = dict(
    ip=dict(type='str', required=True),
    port=dict(type='str'),
)
sampling_inner_args = dict(
    port=dict(type='str', required=True),
    sampling_rate=dict(type='str'),
)
module_args = dict(
    collector=dict(type='list', elements='dict', options=collector_inner_args),
    sampling=dict(type='list', elements='dict', options=sampling_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'sflow'


class PaskSflow(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSflow, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    sflow = PaskSflow(name, module_args)
    sflow.set_param()
    sflow.run()
    sflow.set_result()


if __name__ == '__main__':
    main()