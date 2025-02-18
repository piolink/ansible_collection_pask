#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


class_map_match_inner_args = dict(
    any_traffic=dict(type='str'),
    dest_ip=dict(type='str'),
    dest_mac=dict(type='str'),
    dest_port=dict(type='str'),
    source_ip=dict(type='str'),
    source_mac=dict(type='str'),
    source_port=dict(type='str'),
    protocol=dict(type='str'),
    dscp=dict(type='str'),
    ether_type=dict(type='str'),
    port=dict(type='list', elements='str'),
    input_trunk_id=dict(type='str'),
    output_trunk_id=dict(type='str'),
    vlan=dict(type='str')
)
class_map_inner_args = dict(
    name=dict(type='str', required=True),
    match=dict(type='dict', options=class_map_match_inner_args)
)
policy_map_class_map_rate_limit_inner_args = dict(
    rate=dict(type='str', required=True),
    burst=dict(type='str', required=True)
)
policy_map_class_map_inner_args = dict(
    name=dict(type='str', required=True),
    precedence=dict(type='str'),
    dscp=dict(type='str'),
    priority=dict(type='str'),
    action=dict(type='str'),
    drop_precedence=dict(type='str'),
    priority_to_tos=dict(type='str'),
    tos_to_priority=dict(type='str'),
    rate_limit=dict(type='list', elements='dict',
                    options=policy_map_class_map_rate_limit_inner_args)
)
policy_map_inner_args = dict(
    name=dict(type='str', required=True),
    class_map=dict(type='list', elements='dict',
                   options=policy_map_class_map_inner_args)
)
service_policy_map_inner_args = dict(
    name=dict(type='str', required=True)
)
service_queue_output_rate_limit_inner_args = dict(
    rate=dict(type='str', required=True),
    burst=dict(type='str', required=True)
)
service_queue_input_cos_map_inner_args = dict(
    priority=dict(type='str', required=True),
    index=dict(type='str', required=True)
)
service_queue_output_queue_inner_args = dict(
    index=dict(type='str', required=True),
    min_rate=dict(type='str'),
    max_rate=dict(type='str'),
    weight=dict(type='str')
)
service_queue_inner_args = dict(
    port=dict(type='str', required=True),
    output_schedule_mode=dict(type='str'),
    output_rate_limit=dict(type='list', elements='dict',
                           options=
                           service_queue_output_rate_limit_inner_args),
    input_cos_map=dict(type='list', elements='dict',
                           options=service_queue_input_cos_map_inner_args),
    output_queue=dict(type='list', elements='dict',
                           options=service_queue_output_queue_inner_args)
)


module_args = dict(
    class_map=dict(type='list', elements='dict',
                   options=class_map_inner_args),
    policy_map=dict(type='list', elements='dict',
                    options=policy_map_inner_args),
    service_policy_map=dict(type='list', elements='dict',
                            options=service_policy_map_inner_args),
    service_queue=dict(type='list', elements='dict',
                       options=service_queue_inner_args)
)

name = 'qos'


class PaskQos(PaskModule):
    def __init__(self, name, module_args):
        super(PaskQos, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = self.make_data(self.module.params, include_inner=True)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            resp = self.prest.put(self.url, data)
        self.resp = resp


def main():
    qos = PaskQos(name, module_args)
    qos.set_param()
    qos.run()
    qos.set_result()


if __name__ == '__main__':
    main()