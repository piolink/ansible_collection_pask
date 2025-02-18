#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


session_sync_interface_inner_args = make_module_args(
        ["ip", "hc_retry", "name", "peer_ip"])

session_sync_inner_args = dict(
    interface=dict(type='dict', options=session_sync_interface_inner_args),
    **make_module_args(
        ["status", "full_interval", "interval", "update", "peer"])
)

active_active_failover_health_check_inner_args = dict(
    id=dict(type='str', required=True)
)

active_active_failover_inner_args = dict(
    health_check=dict(type='list', elements='dict',
                      options=active_active_failover_health_check_inner_args),
    **make_module_args(
        ["vlan", "method"])
)

vrrp6_track_real_inner_args = dict(
    priority=dict(type='str'),
    id=dict(type='str', required=True)
)

vrrp6_track_member_port_inner_args = dict(
    priority=dict(type='str'),
    id=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)

vrrp6_track_single_port_inner_args = dict(
    priority=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)

vrrp6_track_inner_args = dict(
    real=dict(type='list', elements='dict',
              options=vrrp6_track_real_inner_args),
    member_port=dict(type='list', elements='dict',
                     options=vrrp6_track_member_port_inner_args),
    single_port=dict(type='list', elements='dict',
                     options=vrrp6_track_single_port_inner_args)
)

vrrp6_interface_inner_args = dict(
    vip=dict(type='list', elements='str'),
    name=dict(type='str', required=True),
    **make_module_args(
        ["advertise_send", "vllip"])
)

vrrp6_inner_args = dict(
    track=dict(type='dict', options=vrrp6_track_inner_args),
    id=dict(type='str', required=True),
    svip=dict(type='list', elements='str'),
    port_block=dict(type='list', elements='str'),
    interface=dict(type='list', elements='dict',
                   options=vrrp6_interface_inner_args, required=True),
    port_boundary=dict(type='list', elements='str'),
    **make_module_args(
        ["status", "mc_retry", "retry", "description", "priority", "vmac",
         "mode", "advertise_interval", "preemption"])
)

vrrp_interface_inner_args = dict(
    advertise_send=dict(type='str'),
    vip=dict(type='list', elements='str', required=True),
    name=dict(type='str', required=True),
    overlapped=dict(type='str'),
)

vrrp_track_real_inner_args = dict(
    priority=dict(type='str'),
    id=dict(type='str', required=True)
)

vrrp_track_member_port_inner_args = dict(
    priority=dict(type='str'),
    id=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)

vrrp_track_single_port_inner_args = dict(
    priority=dict(type='str', required=True),
    port=dict(type='list', elements='str')
)

vrrp_track_inner_args = dict(
    real=dict(type='list', elements='dict', options=vrrp_track_real_inner_args),
    member_port=dict(type='list', elements='dict',
                     options=vrrp_track_member_port_inner_args),
    single_port=dict(type='list', elements='dict',
                     options=vrrp_track_single_port_inner_args)
)

vrrp_inner_args = dict(
    interface=dict(type='list', elements='dict',
                   options=vrrp_interface_inner_args, required=True),
    track=dict(type='dict', options=vrrp_track_inner_args),
    port_boundary=dict(type='list', elements='str'),
    id=dict(type='str', required=True),
    port_block=dict(type='list', elements='str'),
    svip=dict(type='list', elements='str'),
    **make_module_args(
        ["status", "retry", "description", "advertise_interval",
         "send_garp_all_svip", "priority", "arp_count", "vmac", "mode",
         "preemption"])
)

ha_node_inner_args = dict(
    name=dict(type='str', required=True),
    **make_module_args(
        ["ip", "description"])
)

ha_interface_inner_args = dict(
    heartbeat_send=dict(type='str'),
    vip=dict(type='list', elements='str'),
    name=dict(type='str', required=True)
)

ha_inner_args = dict(
    node=dict(type='list', elements='dict', options=ha_node_inner_args),
    interface=dict(type='list', elements='dict',
                   options=ha_interface_inner_args),
    svip=dict(type='list', elements='str'),
    **make_module_args(
        ["status", "heartbeat_interval", "retry", "vmac", "default_state"])
)
ssl_session_cache_sync_interface_inner_args = dict(
    name=dict(type='str'),
    ip=dict(type='str'),
    peer_ip=dict(type='str')
)
ssl_session_cache_sync_inner_args = dict(
    status=dict(type='str'),
    interface=dict(type='dict',
                   options=ssl_session_cache_sync_interface_inner_args)
)

module_args = dict(
    delay_time=dict(type='str'),
    session_sync=dict(type='dict', options=session_sync_inner_args),
    active_active_failover=dict(type='dict',
                                options=active_active_failover_inner_args),
    vrrp6=dict(type='list', elements='dict', options=vrrp6_inner_args),
    vrrp=dict(type='list', elements='dict', options=vrrp_inner_args),
    ha=dict(type='dict', options=ha_inner_args),
    ssl_session_cache_sync=dict(type='dict',
                                options=ssl_session_cache_sync_inner_args),
)

name = 'failover'


class Failover(PaskModule):
    def __init__(self, name, module_args):
        super(Failover, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    failover = Failover(name, module_args)
    failover.set_param()
    failover.run()
    failover.set_result()


if __name__ == '__main__':
    main()
