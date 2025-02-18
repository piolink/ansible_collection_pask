#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


urlmanip_inner_args = dict(
    id=dict(type='str', required=True),
    priority=dict(type='str'),
    rule=dict(type='list', elements='str'),
    match=dict(type='str'),
    replace=dict(type='str'),
    https_for_redirect=dict(type='str'),
    status=dict(type='str')
)
vip_inner_args = dict(
    ip=dict(type='str', required=True),
    vport=dict(type='list', elements='str', required=True)
)
group_real_inner_args = dict(
    id=dict(type='str', required=True)
)
group_persist_cookie_hash_inner_args = dict(
    name=dict(type='str'),
    offset=dict(type='str'),
    length=dict(type='str')
)
group_persist_cookie_inner_args = dict(
    type=dict(type='str'),
    hash=dict(type='dict', options=group_persist_cookie_hash_inner_args),
    update_interval=dict(type='str')
)
group_persist_field_inner_args = dict(
    name=dict(type='str', required=True),
    length=dict(type='str'),
    offset=dict(type='str'),
    starter=dict(type='str'),
    terminator=dict(type='str')
)
group_persist_inner_args = dict(
    type=dict(type='str'),
    timeout=dict(type='str'),
    cookie=dict(type='dict', options=group_persist_cookie_inner_args),
    field=dict(type='dict', options=group_persist_field_inner_args),
    overmax=dict(type='str'),
    destination_subnet=dict(type='str'),
    source_subnet=dict(type='str')
)
group_lb_method_urlhash_inner_args = dict(
    length=dict(type='str'),
    offset=dict(type='str'),
    starter=dict(type='str'),
    terminator=dict(type='str')
)
group_lb_method_inner_args = dict(
    type=dict(type='str'),
    urlhash=dict(type='dict', options=group_lb_method_urlhash_inner_args)
)
group_inner_args = dict(
    name=dict(type='str', required=True),
    real=dict(type='list', elements='dict', options=group_real_inner_args),
    persist=dict(type='dict', options=group_persist_inner_args),
    lb_method=dict(type='dict', options=group_lb_method_inner_args)
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    priority=dict(type='str'),
    pattern=dict(type='str'),
    group=dict(type='str'),
    backup_group=dict(type='str'),
    http_status=dict(type='str'),
    real=dict(type='str'),
    status=dict(type='str'),
    action=dict(type='str')
)
param_list = [
    'status', 'keep_backup', 'connection_pooling', 'server_min_mtu',
    'age_refresh', 'x_header', 'priority', 'fail_action'
]
module_args = dict(
    name=dict(type='str', required=True),
    health_check=dict(type='list', elements='str'),
    urlmanip=dict(type='list', elements='dict', options=urlmanip_inner_args),
    vip=dict(type='list', elements='dict', options=vip_inner_args),
    group=dict(type='list', elements='dict', options=group_inner_args),
    rule=dict(type='list', elements='dict', options=rule_inner_args),
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["vip"])
    ]

name = 'l7slb'


class PaskL7slb(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskL7slb, self).__init__(name, module_args, required_if)

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
    l7slb = PaskL7slb(name, module_args, required_if)
    l7slb.set_param()
    l7slb.run()
    l7slb.set_result()


if __name__ == '__main__':
    main()