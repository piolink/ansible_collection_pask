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
    'location', 'interval', 'status', 'description', 'retry',
    'synchronize'
]
peer_inner_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str'),
    description=dict(type='str'),
)
module_args = dict(
    name=dict(type='str', required=True),
    peer=dict(type='list', elements='dict', options=peer_inner_args),
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["location", "peer"])
    ]

name = 'site'


class PaskSite(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskSite, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['name'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    site = PaskSite(name, module_args, required_if)
    site.set_param()
    site.run()
    site.set_result()


if __name__ == '__main__':
    main()