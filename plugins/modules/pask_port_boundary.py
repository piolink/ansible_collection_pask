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
    'promisc', 'include_mac', 'protocol', 'sip', 'dip', 'vid',
    'sport', 'dport', 'status', 'type', 'boundary', 'description'
]
module_args = dict(
    id=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["port"])
    ]

name = 'port-boundary'


class PaskPortBoundary(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskPortBoundary, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['id'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    port_boundary = PaskPortBoundary(name, module_args, required_if)
    port_boundary.set_param()
    port_boundary.run()
    port_boundary.set_result()


if __name__ == '__main__':
    main()