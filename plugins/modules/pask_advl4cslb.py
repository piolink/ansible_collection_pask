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
sticky_inner_args = dict(
    time=dict(type='str'),
    type=dict(type='str'),
    overmax=dict(type='str'),
    destination_subnet=dict(type='str'),
    destination_subnet6=dict(type='str'),
    source_subnet=dict(type='str'),
    source_subnet6=dict(type='str')
)
nat_sip_inner_args = dict(
    network=dict(type='str', required=True),
    nat_ip=dict(type='str')
)
nat_inner_args = dict(
    status=dict(type='str'),
    mode=dict(type='str'),
    sip=dict(type='list', elements='dict', options=nat_sip_inner_args),
    dip=dict(type='str'),
    dport=dict(type='str'),
    real=dict(type='str')
)
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
    id=dict(type='str'),
    ip=dict(type='str', required=True),
    mac=dict(type='str'),
    interface=dict(type='str')
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    priority=dict(type='str'),
    pattern=dict(type='str', required=True),
    bandwidth=dict(type='str'),
    direction=dict(type='str')
)
rate_limiting_common_inner_args = dict(
    read_timeout=dict(type='str'),
    rule=dict(type='list', elements='dict', options=rule_inner_args)
)
sni_filter_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    description=dict(type='str'),
    match=dict(type='str'),
    sni_string=dict(type='list', elements='str')
)
param_list = [
    'ip_version', 'priority', 'status', 'connection_log', 'preserve_src_port',
    'lb_method', 'backup', 'max_connection', 'session_reuse',
    'return_to_sender', 'sni_bypass', 'ssl_detection', 'lb_fail_safe', 'ssl',
    'sni_port'
]

module_args = dict(
    name=dict(type='str', required=True),
    health_check=dict(type='list', elements='str'),
    timeout=dict(type='dict', options=timeout_inner_args),
    real=dict(type='list', elements='dict', options=real_inner_args),
    sticky=dict(type='dict', options=sticky_inner_args),
    nat=dict(type='dict', options=nat_inner_args),
    filter=dict(type='list', elements='dict', options=filter_inner_args),
    backend_ssl=dict(type='dict', options=backend_ssl_inner_args),
    ssl_decrypt_mirroring=dict(type='dict',
                               options=ssl_decrypt_mirroring_inner_args),
    rts_real=dict(type='list', elements='dict', options=rts_real_inner_args),
    rate_limiting=dict(type='dict', options=rate_limiting_common_inner_args),
    sni_filter=dict(type='list', elements='dict',
                    options=sni_filter_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'advl4cslb'


class PaskAdvl4cslb(PaskModule):
    def __init__(self, name, module_args):
        super(PaskAdvl4cslb, self).__init__(name, module_args)

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
    advl4cslb = PaskAdvl4cslb(name, module_args)
    advl4cslb.set_param()
    advl4cslb.run()
    advl4cslb.set_result()


if __name__ == '__main__':
    main()