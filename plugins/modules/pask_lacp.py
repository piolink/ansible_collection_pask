#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


port_inner_args = dict(
    priority=dict(type='str'),
    name=dict(type='str', required=True),
    mode=dict(type='str', required=True)
)

module_args = dict(
    port=dict(type='list', elements='dict', options=port_inner_args),
    num=dict(type='str', required=True),
    **make_module_args(
        ["description", "load_balance"])
)

required_if = [
    ("state", "present", ["port"])
    ]

name = 'lacp'


class PaskLacp(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskLacp, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        data = dict()
        if self.module.params['state'] == "absent":
            data[name] = dict(num=self.module.params['num'])
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['num'])
            self.resp = self.prest.put(url, data)


def main():
    lacp = PaskLacp(name, module_args, required_if)
    lacp.set_param()
    lacp.run()
    lacp.set_result()


if __name__ == '__main__':
    main()
