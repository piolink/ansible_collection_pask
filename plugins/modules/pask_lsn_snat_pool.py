#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


module_args = dict(
    id=dict(type='str', required=True),
    pool=dict(type='str'),
    proxy_arp_interface=dict(type='str')
)

required_if = [
    ("state", "present", ["pool"])
    ]

name = 'lsn'
subname = 'snat-pool'


class PaskLsnSnatPool(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskLsnSnatPool, self).__init__(name, module_args, required_if)

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
    lsn_snat_pool = PaskLsnSnatPool(name, module_args, required_if)
    lsn_snat_pool.set_param()
    lsn_snat_pool.run()
    lsn_snat_pool.set_result()


if __name__ == '__main__':
    main()