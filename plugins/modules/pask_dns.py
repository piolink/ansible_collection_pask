#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except


id_inner_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str', required=True),
    description=dict(type='str', required=False),
)

outermost_param_str = [
    'retry', 'timeout'
]
module_args = dict(
    id=dict(type='list', elements='dict', options=id_inner_args)
)
module_args.update(make_module_args(outermost_param_str))

name = 'dns'


class PaskDns(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDns, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    dns = PaskDns(name, module_args)
    dns.set_param()
    dns.run()
    dns.set_result()


if __name__ == '__main__':
    main()
