#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


name_server_inner_args = dict(
    id=dict(type='str', required=True),
    name=dict(type='str', required=True),
    ip=dict(type='str'),
    ip6=dict(type='str'),
    ttl=dict(type='str'),
    status=dict(type='str'),
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    host=dict(type='list', elements='str', required=True),
    ttl=dict(type='str'),
    group=dict(type='str', required=True),
    status=dict(type='str'),
    description=dict(type='str'),
    failure_rcode_response=dict(type='str'),
    failure_rcode=dict(type='str'),
)
group_real_inner_args= dict(
    id=dict(type='str', required=True),
    rport=dict(type='str'),
    svcip=dict(type='str'),
    status=dict(type='str'),
)
group_inner_args = dict(
    id=dict(type='str', required=True),
    real=dict(type='list', elements='dict', options=group_real_inner_args,
              required=True),
    lb_method=dict(type='str'),
    description=dict(type='str'),
    geolocation=dict(type='str'),
)

param_list = [
    'zone', 'priority', 'status', 'inbound_lb_mode', 'max_answers',
    'description'
]
module_args = dict(
    name=dict(type='str', required=True),
    name_server=dict(type='list', elements='dict', options=name_server_inner_args),
    rule=dict(type='list', elements='dict', options=rule_inner_args),
    group=dict(type='list', elements='dict', options=group_inner_args),
    health_check=dict(type='list', elements='str'),
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["zone"])
    ]

name = 'gslb'


class PaskGslb(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskGslb, self).__init__(name, module_args, required_if)

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
    gslb = PaskGslb(name, module_args, required_if)
    gslb.set_param()
    gslb.run()
    gslb.set_result()


if __name__ == '__main__':
    main()