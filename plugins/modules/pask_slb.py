#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os, json


filter_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str'),
    protocol=dict(type='str'),
    sip=dict(type='str'),
    dip=dict(type='str'),
    sport=dict(type='str'),
    dport=dict(type='str'),
    status=dict(type='str'),
    description=dict(type='str')
)
dynamic_filter_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str')
)
keep_backup_inner_args = dict(
    service=dict(type='str'),
    real=dict(type='str')
)
real_inner_args = dict(
    id=dict(type='str', required=True),
    rport=dict(type='str'),
    backup=dict(type='str'),
    status=dict(type='str'),
    graceful_shutdown=dict(type='str'),
    description=dict(type='str')
)
session_timeout_inner_args = dict(
    generic=dict(type='str'),
    icmp=dict(type='str'),
    icmpv6=dict(type='str'),
    udp=dict(type='str'),
    udp_stream=dict(type='str'),
    tcp_syn_sent=dict(type='str'),
    tcp_syn_recv=dict(type='str'),
    tcp_established=dict(type='str'),
    tcp_fin_wait=dict(type='str'),
    tcp_close_wait=dict(type='str'),
    tcp_last_ack=dict(type='str'),
    tcp_wait=dict(type='str'),
    tcp_close=dict(type='str'),
    tcp_unassured=dict(type='str')
)
sticky_inner_args = dict(
    time=dict(type='str'),
    source_subnet=dict(type='str'),
    source_subnet6=dict(type='str'),
    destination_subnet=dict(type='str'),
    destination_subnet6=dict(type='str')
)
dynamic_proximity_inner_args = dict(
    name=dict(type='str', required=True),
    ratio=dict(type='str')
)
backup_inner_args = dict(
    backup=dict(type='str', required=True),
    partial_threshold=dict(type='str'),
    back_inservice=dict(type='str')
)
vip_protocol_inner_args = dict(
    protocol=dict(type='str', required=True),
    vport=dict(type='list', elements='str')
)
vip_inner_args = dict(
    ip=dict(type='str', required=True),
    protocol=dict(type='list', elements='dict',
                  options=vip_protocol_inner_args),
    dscp=dict(type='str')
)
slow_start_inner_args = dict(
    rate=dict(type='str'),
    timer=dict(type='str')
)

param_list = [
    'session_sync', 'status', 'description', 'hc_condition',
    'session_timeout_mode', 'session_reset', 'active_nodest', 'ip_version',
    'fail_skip', 'fail_action', 'priority', 'lb_method', 'nat_mode'
]

module_args = dict(
    name=dict(type='str', required=True),
    filter=dict(type='list', elements='dict', options=filter_inner_args),
    dynamic_filter=dict(type='list', elements='dict',
                        options=dynamic_filter_inner_args),
    keep_backup=dict(type='dict', options=keep_backup_inner_args),
    real=dict(type='list', elements='dict', options=real_inner_args),
    health_check=dict(type='list', elements='str'),
    passive_health_check=dict(type='list', elements='str'),
    session_timeout=dict(type='dict', options=session_timeout_inner_args),
    sticky=dict(type='dict', options=sticky_inner_args),
    dynamic_proximity=dict(type='list', elements='dict',
                           options=dynamic_proximity_inner_args),
    backup=dict(type='list', elements='dict', options=backup_inner_args),
    vip=dict(type='list', elements='dict', options=vip_inner_args),
    lan_to_lan=dict(type='list', elements='str'),
    slow_start=dict(type='dict', options=slow_start_inner_args),
    snatip=dict(type='list', elements='str')
)

module_args.update(make_module_args(param_list))

name = 'slb'

required_if = [
    ("state", "present", ["vip"])
    ]

class PaskSlb(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskSlb, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            filter_data = self.make_filter_data(data)
            data['filter'] = filter_data
            url = os.path.join(self.url, self.module.params['name'])
            resp = self.prest.get(url)
            resp_dict = json.loads(resp.text)
            self.make_real_backup_data(data, resp_dict)
            self.resp = self.prest.put(url, data)


def main():
    slb = PaskSlb(name, module_args, required_if)
    slb.set_param()
    slb.run()
    slb.set_result()


if __name__ == '__main__':
    main()
