#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except, make_module_args
import os


inner_nat_param = [
    'type', 'priority', 'sip', 'dip', 'protocol', 'status',
    'sport', 'dport'
]
inner_nat_args = dict(
    id=dict(type='str', required=True),
    external_ip=dict(type='str', required=True),
    internal_ip=dict(type='str', required=True),
    natip=dict(type='list', elements='str', required=True),
    natport=dict(type='list', elements='str')
)
inner_nat_args.update(make_module_args(inner_nat_param))

inner_hc_args = dict(
    id=dict(type='str', required=True),
)

inner_device_args = dict(
    port=dict(type='str', required=True),
    user=dict(type='str', required=True),
    passwd=dict(type='str', required=True),
    ip=dict(type='str', required=True)
)

module_args = dict(
    id=dict(type='str', required=True),
    rip=dict(type='str'),
    nat=dict(type='list', elements='dict', options=inner_nat_args),
    health_check=dict(type='list', elements='dict', options=inner_hc_args),
    device=dict(type='list', elements='dict', options=inner_device_args),
    sp_filter=dict(type='list', elements='str'),
    sp_filter_group=dict(type='list', elements='str'),
    domain_filter=dict(type='list', elements='str'),
    src_natip=dict(type='list', elements='str'),
)

param_list = [
    'name', 'rport', 'mac', 'interface', 'priority', 'weight',
    'graceful_shutdown', 'max_connection', 'upload_bandwidth',
    'download_bandwidth', 'pool_size',
    'pool_age', 'pool_reuse', 'pool_srcmask', 'backup',
    'status', 'description', 'manual_resume', 'preemption',
    'site', 'ssl_rport', 'surge_base_thr', 'surge_upper', 'svcip'
]
module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["rip"])
    ]

name = 'real'


class PaskReal(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskReal, self).__init__(
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
            url = os.path.join(self.url, self.module.params['id'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    real = PaskReal(name, module_args, required_if)
    real.set_param()
    real.run()
    real.set_result()


if __name__ == '__main__':
    main()
