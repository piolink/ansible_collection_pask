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
    'load_balance', 'description',
]
module_args = dict(
    num=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["port"])
    ]

name = 'trunk'


class PaskTrunk(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskTrunk, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data['trunk'] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['num'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    trunk = PaskTrunk(name, module_args, required_if)
    trunk.set_param()
    trunk.run()
    trunk.set_result()


if __name__ == '__main__':
    main()