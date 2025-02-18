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
    'description', 'hostname'
]
module_args = dict(
    ip=dict(type='str', required=True),
    alias=dict(type='list', elements='str')
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["hostname"])
    ]

name = 'hosts'


class PaskHosts(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskHosts, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['ip'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    hosts = PaskHosts(name, module_args, required_if)
    hosts.set_param()
    hosts.run()
    hosts.set_result()


if __name__ == '__main__':
    main()