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
    'description'
]
port_inner_args = dict(
    port=dict(type='str', required=True),
    weight=dict(type='str')
)
module_args = dict(
    channel_group=dict(type='str', required=True),
    port=dict(type='list', elements='dict', options=port_inner_args)
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["port"])
    ]

name = 'trunk-active-backup'


class PaskTrunkActiveBackup(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskTrunkActiveBackup, self).__init__(
            name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['channel_group'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    trunk_active_backup = PaskTrunkActiveBackup(name, module_args, required_if)
    trunk_active_backup.set_param()
    trunk_active_backup.run()
    trunk_active_backup.set_result()


if __name__ == '__main__':
    main()