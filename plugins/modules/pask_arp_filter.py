#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_args = dict(
    id=dict(type='str',required=True),
    action=dict(type='str', required=False),
    sip=dict(type='str', required=False),
    dip=dict(type='str', required=False),
    description=dict(type='str', required=False),
    interface=dict(type='str', required=False)
)

module_args = dict(
    input=dict(type='list', elements='dict', option=inner_args),
    output=dict(type='list', elements='dict', option=inner_args),
)

name = 'arp-filter'


class PaskArpFilter(PaskModule):
    def __init__(self, name, module_args):
        super(PaskArpFilter, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    arp_filter = PaskArpFilter(name, module_args)
    arp_filter.set_param()
    arp_filter.run()
    arp_filter.set_result()


if __name__ == '__main__':
    main()
