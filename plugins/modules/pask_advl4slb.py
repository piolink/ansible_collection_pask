#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


timeout_inner_args = dict(
    session_timeout=dict(type='str')
)
real_inner_args = dict(
    id=dict(type='str', required=True)
)
protocol_inner_args = dict(
    protocol=dict(type='str', required=True),
    vport=dict(type='list', elements='str', required=True)
)
vip_inner_args = dict(
    ip=dict(type='str', required=True),
    protocol=dict(type='list', elements='dict', options=protocol_inner_args)
)
sticky_inner_args = dict(
    time=dict(type='str'),
    type=dict(type='str'),
    overmax=dict(type='str'),
    destination_subnet=dict(type='str'),
    destination_subnet6=dict(type='str'),
    source_subnet=dict(type='str'),
    source_subnet6=dict(type='str')
)
backend_ssl_inner_args = dict(
    status=dict(type='str'),
    profile=dict(type='str')
)
tcp_session_inner_args = dict(
    handshake=dict(type='str'),
    teardown=dict(type='str')
)
mirror_message_inner_args = dict(
    request=dict(type='str'),
    response=dict(type='str')
)
ssl_decrypt_mirroring_inner_args = dict(
    status=dict(type='str'),
    interface=dict(type='str'),
    dmac=dict(type='str'),
    dport=dict(type='str'),
    send_delay=dict(type='str'),
    tcp_session=dict(type='dict', options=tcp_session_inner_args),
    mirror_message=dict(type='dict', options=mirror_message_inner_args)
)
rts_real_inner_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str'),
    mac=dict(type='str'),
    interface=dict(type='str')
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    priority=dict(type='str'),
    pattern=dict(type='str'),
    bandwidth=dict(type='str'),
    direction=dict(type='str')
)
rate_limiting_common_inner_args = dict(
    read_timeout=dict(type='str'),
    rule=dict(type='list', elements='dict', options=rule_inner_args)
)
snat_addr_inner_args = dict(
    network=dict(type='str', required=True),
    nat_ip=dict(type='str')
)
param_list = [
    'ip_version', 'priority', 'status', 'connection_log', 'preserve_src_port',
    'nat_mode', 'lb_method', 'fail_action', 'backup', 'max_connection', 'session_reuse',
    'return_to_sender', 'ssl_detection', 'ssl', 'vdi_support', 'sni_port'
]

module_args = dict(
    name=dict(type='str', required=True),
    health_check=dict(type='list', elements='str'),
    timeout=dict(type='dict', options=timeout_inner_args),
    real=dict(type='list', elements='dict', options=real_inner_args),
    vip=dict(type='list', elements='dict', options=vip_inner_args),
    sticky=dict(type='dict', options=sticky_inner_args),
    backend_ssl=dict(type='dict', options=backend_ssl_inner_args),
    ssl_decrypt_mirroring=dict(type='dict',
                               options=ssl_decrypt_mirroring_inner_args),
    rts_real=dict(type='list', elements='dict', options=rts_real_inner_args),
    rate_limiting=dict(type='dict', options=rate_limiting_common_inner_args),
    snat_addr=dict(type='list', elements='dict', options=snat_addr_inner_args),
)


module_args.update(make_module_args(param_list))

required_if = [
    ("state", "present", ["vip"])
    ]

name = 'advl4slb'


class PaskAdvl4slb(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskAdvl4slb, self).__init__(name, module_args, required_if)

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
    advl4slb = PaskAdvl4slb(name, module_args, required_if)
    advl4slb.set_param()
    advl4slb.run()
    advl4slb.set_result()


if __name__ == '__main__':
    main()