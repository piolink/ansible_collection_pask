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
    'server_type', 'path', 'user', 'interface',
    'description', 'host', 'port'
]
module_args = dict(
    id=dict(type='str', required=True),
    password=dict(type='str', no_log=True)
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["host"])
    ]

name = 'config-slot'


class PaskConfigSlot(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskConfigSlot, self).__init__(name, module_args, required_if)

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
    config_slot = PaskConfigSlot(name, module_args, required_if)
    config_slot.set_param()
    config_slot.run()
    config_slot.set_result()


if __name__ == '__main__':
    main()