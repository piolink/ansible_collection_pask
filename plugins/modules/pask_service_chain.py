#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


filter_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str'),
    protocol=dict(type='str'),
    sip=dict(type='str'),
    dip=dict(type='str'),
    sport=dict(type='str'),
    dport=dict(type='str'),
    description=dict(type='str')
)
path_inner_args = dict(
    id=dict(type='str', required=True),
    name=dict(type='str', required=True),
    type=dict(type='str'),
    input_interface=dict(type='str'),
    description=dict(type='str')
)
module_args = dict(
    id=dict(type='str', required=True),
    filter=dict(type='list', elemenets='dict', options=filter_inner_args),
    path=dict(type='list', elemenets='dict', options=path_inner_args),
)

name = 'service-chain'


class PaskServiceChain(PaskModule):
    def __init__(self, name, module_args):
        super(PaskServiceChain, self).__init__(name, module_args)

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
    service_chain = PaskServiceChain(name, module_args)
    service_chain.set_param()
    service_chain.run()
    service_chain.set_result()


if __name__ == '__main__':
    main()