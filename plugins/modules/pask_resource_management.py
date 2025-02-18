#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


inner_mp_args = dict(
    cpus=dict(type='str'),
    memory=dict(type='str')
)

module_args = dict(
    mp=dict(type='dict', options=inner_mp_args)
)

name = 'resource-management'


class PaskResourceManagement(PaskModule):
    def __init__(self, name, module_args):
        super(PaskResourceManagement, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    resource_management = PaskResourceManagement(name, module_args)
    resource_management.set_param()
    resource_management.run()
    resource_management.set_result()


if __name__ == '__main__':
    main()