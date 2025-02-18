#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


proxy_dest_inner_args = dict(
    type=dict(type='str'),
    name=dict(type='str'),
    id=dict(type='str'),
    ip=dict(type='str'),
    port=dict(type='str'),
)
proxy_filter_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    type=dict(type='str'),
    sip=dict(type='str'),
    sport=dict(type='str'),
    dip=dict(type='str'),
    dport=dict(type='str'),
)

module_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    ip_version=dict(type='str'),
    profile=dict(type='str'),
    status=dict(type='str'),
    dest=dict(type='dict', options=proxy_dest_inner_args),
    filter=dict(type='list', elements='dict', options=proxy_filter_inner_args),
)


required_if = [
    ("state", "present", ["profile"])
    ]

name = 'ssl'
subname = 'proxy'


class PaskSslProxy(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSslProxy, self).__init__(name, module_args)

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
            url = os.path.join(url, self.module.params['name'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_proxy = PaskSslProxy(name, module_args)
    ssl_proxy.set_param()
    ssl_proxy.run()
    ssl_proxy.set_result()


if __name__ == '__main__':
    main()