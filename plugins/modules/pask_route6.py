#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


network_inner_args = dict(
    dest=dict(type='str', required=True),
    interface=dict(type='str'),
    gateway=dict(type='str'),
    type=dict(type='str'),
    description=dict(type='str')
)
default_gateway_health_check_inner_args = dict(
    id=dict(type='str', required=True)
)
default_gateway_inner_args = dict(
    gateway=dict(type='str', required=True),
    health_check=dict(type='list', elemenets='dict',
                      options=default_gateway_health_check_inner_args),
    priority=dict(type='str')
    )

module_args = dict(
    network=dict(type='list', elemenets='dict', options=network_inner_args),
    default_gateway=dict(type='list', elemenets='dict',
                         options=default_gateway_inner_args)
)

name = 'route6'


class PaskRoute6(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRoute6, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    route6 = PaskRoute6(name, module_args)
    route6.set_param()
    route6.run()
    route6.set_result()


if __name__ == '__main__':
    main()