#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


periodic_arp_inner_args = dict(
    src_ip=dict(type='str'),
    dst_ip=dict(type='str'),
    src_mac=dict(type='str'),
    dst_mac=dict(type='str'),
    interface=dict(type='str'),
    interval=dict(type='str'),
    status=dict(type='str')
)

module_args = dict(
    periodic_arp=dict(type='dict', options=periodic_arp_inner_args),
)

name = 'periodic-command'


class PaskPeriodicCommand(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPeriodicCommand, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    periodic_command = PaskPeriodicCommand(name, module_args)
    periodic_command.set_param()
    periodic_command.run()
    periodic_command.set_result()


if __name__ == '__main__':
    main()