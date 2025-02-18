#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


firewall_content_inner_args = dict(
    name=dict(type='str', required=True),
    string=dict(type='str', required=True),
    case_sensitive=dict(type='str'),
    offset=dict(type='str'),
    depth=dict(type='str'),
)
firewall_content_group_inner_args = dict(
    name=dict(type='str', required=True),
    content=dict(type='list', elements='str', required=True),
    description=dict(type='str')
)
firewall_filter_source_port_inner_args = dict(
    operation=dict(type='str', required=True),
    port_num=dict(type='str')
)
firewall_filter_dest_port_inner_args = dict(
    operation=dict(type='str', required=True),
    port_num=dict(type='str')
)
firewall_filter_inner_args = dict(
    name=dict(type='str', required=True),
    action=dict(type='str'),
    source_port=dict(type='list', elements='dict',
                     options=firewall_filter_source_port_inner_args),
    dest_port=dict(type='list', elements='dict',
                   options=firewall_filter_dest_port_inner_args),
    log=dict(type='str'),
    tcp_flag=dict(type='list', elements='str'),
    tcp_flag_option=dict(type='list', elements='str'),
    length=dict(type='str'),
    protocol=dict(type='str'),
    source_ip=dict(type='str'),
    dest_ip=dict(type='str'),
    content=dict(type='list', elements='str'),
    content_group=dict(type='list', elements='str'),
    rate_limit_value=dict(type='str'),
    blacklist_type=dict(type='str'),
    blacklist_action=dict(type='str'),
    blacklist_timeout=dict(type='str'),
    white_timeout=dict(type='str'),
    icmp_type=dict(type='list', elements='str')
)
firewall_filter_group_inner_args = dict(
    name=dict(type='str', required=True),
    filter=dict(type='list', elements='str', required=True),
    description=dict(type='str')
)
firewall_policy_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    interface=dict(type='str'),
    status=dict(type='str'),
    filter=dict(type='list', elements='str'),
    filter_group=dict(type='list', elements='str'),
    description=dict(type='str')
)

firewall_inner_args = dict(
    content=dict(type='list', elements='dict',
                 options=firewall_content_inner_args),
    content_group=dict(type='list', elements='dict',
                       options=firewall_content_group_inner_args),
    filter=dict(type='list', elements='dict',
                options=firewall_filter_inner_args),
    filter_group=dict(type='list', elements='dict',
                      options=firewall_filter_group_inner_args),
    policy=dict(type='list', elements='dict',
                options=firewall_policy_inner_args),
)

firewall6_content_inner_args = dict(
    name=dict(type='str', required=True),
    string=dict(type='str'),
    case_sensitive=dict(type='str'),
    offset=dict(type='str'),
    depth=dict(type='str'),
)
firewall6_content_group_inner_args = dict(
    name=dict(type='str', required=True),
    content=dict(type='list', elements='str', required=True),
    description=dict(type='str')
)
firewall6_filter_action_inner_args = dict(
    act=dict(type='str'),
    rate_limit_value=dict(type='str')
)
firewall6_filter_source_port_inner_args = dict(
    operation=dict(type='str', required=True),
    port_num=dict(type='str')
)
firewall6_filter_dest_port_inner_args = dict(
    operation=dict(type='str', required=True),
    port_num=dict(type='str')
)
firewall6_filter_inner_args = dict(
    name=dict(type='str', required=True),
    action=dict(type='list', elements='dict',
                options=firewall6_filter_action_inner_args, required=True),
    source_port=dict(type='list', elements='dict',
                     options=firewall6_filter_source_port_inner_args),
    port_num=dict(type='str'),
    dest_port=dict(type='list', elements='dict',
                   options=firewall6_filter_dest_port_inner_args),
    log=dict(type='str'),
    tcp_flag=dict(type='list', elements='str'),
    tcp_flag_option=dict(type='list', elements='str'),
    length=dict(type='str'),
    protocol=dict(type='str'),
    source_ip=dict(type='str'),
    dest_ip=dict(type='str'),
    content=dict(type='list', elements='str'),
    content_group=dict(type='list', elements='str'),
    icmpv6_type=dict(type='list', elements='str'),
)
firewall6_filter_group_inner_args = dict(
    name=dict(type='str', required=True),
    filter=dict(type='list', elements='str', required=True),
    description=dict(type='str')
)
firewall6_policy_inner_args = dict(
    name=dict(type='str', required=True),
    priority=dict(type='str'),
    interface=dict(type='str'),
    status=dict(type='str'),
    filter=dict(type='list', elements='str'),
    filter_group=dict(type='list', elements='str'),
    description=dict(type='str')
)

firewall6_inner_args = dict(
    content=dict(type='list', elements='dict',
                 options=firewall6_content_inner_args),
    content_group=dict(type='list', elements='dict',
                       options=firewall6_content_group_inner_args),
    filter=dict(type='list', elements='dict',
                options=firewall6_filter_inner_args),
    filter_group=dict(type='list', elements='dict',
                      options=firewall6_filter_group_inner_args),
    policy=dict(type='list', elements='dict',
                options=firewall6_policy_inner_args),
)

access_rule_inner_args = dict(
    id=dict(type='str', required=True),
    description=dict(type='str'),
    status=dict(type='str'),
    interface=dict(type='str'),
    vlan_name=dict(type='str'),
    protocol=dict(type='str'),
    source_port=dict(type='list', elements='str'),
    destination_port=dict(type='list', elements='str'),
    policy=dict(type='str'),
    destination_ip=dict(type='str'),
    source_ip=dict(type='str'),
    mac_address=dict(type='str')
)
access_rule6_inner_args = dict(
    id=dict(type='str', required=True),
    description=dict(type='str'),
    status=dict(type='str'),
    interface=dict(type='str'),
    vlan_name=dict(type='str'),
    protocol=dict(type='str'),
    source_port=dict(type='list', elements='str'),
    destination_port=dict(type='list', elements='str'),
    policy=dict(type='str'),
    destination_ip=dict(type='str'),
    source_ip=dict(type='str'),
    mac_address=dict(type='str')
)
access_inner_args = dict(
    default_policy=dict(type='str'),
    rule=dict(type='list', elements='dict', options=access_rule_inner_args),
    rule6=dict(type='list', elements='dict', options=access_rule6_inner_args),
)
dos_protect_inner_args = dict(
    syn_cookies=dict(type='str'),
)

module_args = dict(
    firewall=dict(type='dict', options=firewall_inner_args),
    firewall6=dict(type='dict', options=firewall6_inner_args),
    access=dict(type='dict', options=access_inner_args),
    dos_protect=dict(type='dict', options=dos_protect_inner_args),
)


name = 'security'

class PaskSecurity(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSecurity, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    security = PaskSecurity(name, module_args)
    security.set_param()
    security.run()
    security.set_result()


if __name__ == '__main__':
    main()