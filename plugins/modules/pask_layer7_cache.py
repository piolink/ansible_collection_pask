#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


cache_max_age_inner_args = dict(
    resp_code=dict(type='str', required=True),
    time=dict(type='str', required=True)
)
cache_lock_inner_args = dict(
    status=dict(type='str'),
    age=dict(type='str')
)

module_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    size=dict(type='str'),
    expire=dict(type='str'),
    max_age=dict(type='list', elements='dict',
                 options=cache_max_age_inner_args),
    min_use=dict(type='str'),
    method=dict(type='list', elements='str'),
    ignore_header=dict(type='str'),
    content_type=dict(type='list', elements='str'),
    exclude_uri=dict(type='list', elements='str'),
    lock=dict(type='dict', options=cache_lock_inner_args),
    purge_cache=dict(type='str'),
)

required_if = [
    ("state", "present", ["max_age"])
    ]

name = 'layer7'
subname = 'cache'


command_list = ['purge_cache']

class PaskLayer7Cache(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskLayer7Cache, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        if self.module.params['state'] == "absent":
            data = dict()
            data[subname] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(url, self.module.params['id'])
            if self.check_command(self.module.params, command_list):
                resp = self.prest.post(url, data)
            else:
                resp = self.prest.put(url, data)
        self.resp = resp


def main():
    layer7cache = PaskLayer7Cache(name, module_args, required_if)
    layer7cache.set_param()
    layer7cache.run()
    layer7cache.set_result()


if __name__ == '__main__':
    main()