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
    'status'
]
filter_inner_args = dict(
    id=dict(type='str', required=True),
    priority=dict(type='str'),
    type=dict(type='str'),
    status=dict(type='str'),
    protocol=dict(type='str'),
    sip=dict(type='str'),
    dip=dict(type='str'),
    snatip=dict(type='list', elements='str'),
    dnatip=dict(type='list', elements='str'),
    external_ip=dict(type='str'),
    internal_ip=dict(type='str'),
    description=dict(type='str')
)
module_args = dict(
    filter=dict(type='list', elements='dict', options=filter_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'nat'


class PaskNat(PaskModule):
    def __init__(self, name, module_args):
        super(PaskNat, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    nat = PaskNat(name, module_args)
    nat.set_param()
    nat.run()
    nat.set_result()


if __name__ == '__main__':
    main()