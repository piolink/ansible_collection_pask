#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


icap_reqmod_inner_args = dict(
    status=dict(type='str'),
    ip=dict(type='str'),
    port=dict(type='str'),
    uri=dict(type='str'),
    failure_action=dict(type='str'),
    timeout=dict(type='str'),
    send_client_ip=dict(type='str'),
)
icap_respmod_inner_args = dict(
    status=dict(type='str'),
    ip=dict(type='str'),
    port=dict(type='str'),
    uri=dict(type='str'),
    failure_action=dict(type='str'),
    timeout=dict(type='str'),
    send_server_ip=dict(type='str'),
)

module_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str'),
    port=dict(type='str'),
    reqmod=dict(type='dict', options=icap_reqmod_inner_args),
    respmod=dict(type='dict', options=icap_respmod_inner_args),
)

name = 'layer7'
subname = 'icap'

class PaskLayer7Icap(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLayer7Icap, self).__init__(name, module_args)

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
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    layer7icap = PaskLayer7Icap(name, module_args)
    layer7icap.set_param()
    layer7icap.run()
    layer7icap.set_result()


if __name__ == '__main__':
    main()