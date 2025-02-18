#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


static_inner_args = dict(
    ipaddr=dict(type='str', required=True),
    hwaddr=dict(type='str', required=True),
    description=dict(type='str')
)
param_list = [
    'proxy_arp', 'proxy_delay', 'locktime', 'timeout'
]
module_args = dict(
    static=dict(type='list', elements='dict', options=static_inner_args),
)


module_args.update(make_module_args(param_list))

name = 'arp'


class PaskArp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskArp, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    arp = PaskArp(name, module_args)
    arp.set_param()
    arp.run()
    arp.set_result()


if __name__ == '__main__':
    main()