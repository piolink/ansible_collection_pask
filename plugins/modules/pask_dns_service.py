#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


param_list = [
    'clear_cache'
]
zone_soa_inner_args = dict(
    mname=dict(type='str'),
    rname=dict(type='str'),
    ttl=dict(type='str'),
    refresh=dict(type='str'),
    retry=dict(type='str'),
    expire=dict(type='str'),
    negative_ttl=dict(type='str'),
)
zone_record_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str', required=True),
    host=dict(type='str', required=True),
    ttl=dict(type='str'),
    service_ip=dict(type='str'),
    service_ip6=dict(type='str'),
    preference=dict(type='str'),
    cname=dict(type='str'),
    dname=dict(type='str'),
    text=dict(type='str'),
    spf=dict(type='str'),
    ns=dict(type='str'),
    mx=dict(type='str'),
    key_tag=dict(type='str'),
    algorithm=dict(type='str'),
    digest_type=dict(type='str'),
    digest=dict(type='str'),
    cpu=dict(type='str'),
    os=dict(type='str'),
    priority=dict(type='str'),
    weight=dict(type='str'),
    port=dict(type='str'),
    target=dict(type='str'),
    order=dict(type='str'),
    flag=dict(type='str'),
    service=dict(type='str'),
    regexp=dict(type='str'),
    replacement=dict(type='str'),
    create_reverse_record=dict(type='str'),
    status=dict(type='str')
)
zone_inner_args = dict(
    zone=dict(type='str', required=True),
    masters=dict(type='list', elements='str'),
    allow_notify_ip=dict(type='list', elements='str'),
    transfer_src_ip=dict(type='str'),
    status=dict(type='str'),
    soa=dict(type='dict', options=zone_soa_inner_args),
    description=dict(type='str'),
    zone_transfer=dict(type='str'),
    zone_type=dict(type='str'),
    record=dict(type='list', elements='dict', options=zone_record_inner_args),
    transparent_mode=dict(type='str'),
    forwarders=dict(type='list', elements='str'),
    reverse_zone_name=dict(type='str'),
)
reverse_zone_soa_inner_args = dict(
    mname=dict(type='str'),
    rname=dict(type='str'),
    ttl=dict(type='str'),
    refresh=dict(type='str'),
    retry=dict(type='str'),
    expire=dict(type='str'),
    negative_ttl=dict(type='str'),
)
reverse_zone_record_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str', required=True),
    domain_name=dict(type='str', required=True),
    ttl=dict(type='str'),
    service_ip=dict(type='str'),
    service_ip6=dict(type='str'),
    host=dict(type='str'),
    ns=dict(type='str'),
    key_tag=dict(type='str'),
    algorithm=dict(type='str'),
    digest_type=dict(type='str'),
    digest=dict(type='str'),
    status=dict(type='str'),
)
reverse_zone_inner_args = dict(
    zone=dict(type='str', required=True),
    masters=dict(type='list', elements='str'),
    allow_notify_ip=dict(type='list', elements='str'),
    transfer_src_ip=dict(type='str'),
    status=dict(type='str'),
    soa=dict(type='dict', options=reverse_zone_soa_inner_args),
    description=dict(type='str'),
    zone_transfer=dict(type='str'),
    zone_type=dict(type='str'),
    record=dict(type='list', elements='dict',
                options=reverse_zone_record_inner_args),
)
options_inner_args = dict(
    minimal_response=dict(type='str'),
    lookup_mode=dict(type='str'),
    allow_transfer_mode=dict(type='str'),
    forwarder=dict(type='list', elements='str'),
    allow_transfer_ip=dict(type='list', elements='str'),
    transfer_src_ip=dict(type='str')
)
dnssec_dnssec_key_inner_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str'),
    algorithm=dict(type='str'),
    bit=dict(type='str'),
    ttl=dict(type='str'),
    expiration_period=dict(type='str'),
    notification_period=dict(type='str'),
    description=dict(type='str')
)
dnssec_zone_dnssec_key_inner_args = dict(
    id=dict(type='str', required=True),
    description=dict(type='str')
)
dnssec_zone_inner_args = dict(
    name=dict(type='str', required=True),
    status=dict(type='str'),
    dnssec_key=dict(type='list', elements='dict',
                    options=dnssec_zone_dnssec_key_inner_args)
)
dnssec_inner_args = dict(
    dnssec_key=dict(type='list', elements='dict',
                    options=dnssec_dnssec_key_inner_args),
    zone=dict(type='list', elements='dict',
                    options=dnssec_zone_inner_args)
)
zone_transfer_inner_args = dict(
    type=dict(type='str')
)
log_inner_args = dict(
    query=dict(type='str'),
    response=dict(type='str'),
    lb_decision=dict(type='str')
)
name_server_ip_inner_args = dict(
    ip=dict(type='str', required=True),
    status=dict(type='str')
)
name_server_ip6_inner_args = dict(
    ip=dict(type='str', required=True),
    status=dict(type='str')
)
module_args = dict(
    name_server_ip=dict(
        type='list', elements='dict', options=name_server_ip_inner_args),
    name_server_ip6=dict(
        type='list', elements='dict', options=name_server_ip6_inner_args),
    zone=dict(type='list', elements='dict', options=zone_inner_args),
    reverse_zone=dict(type='list', elements='dict',
                      options=reverse_zone_inner_args),
    options=dict(type='dict', options=options_inner_args),
    dnssec=dict(type='dict', options=dnssec_inner_args),
    zone_transfer=dict(type='dict', options=zone_transfer_inner_args),
    log=dict(type='dict', options=log_inner_args),
)


module_args.update(make_module_args(param_list))

name = 'dns-service'


class PaskDnsService(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDnsService, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    dns_service = PaskDnsService(name, module_args)
    dns_service.set_param()
    dns_service.run()
    dns_service.set_result()


if __name__ == '__main__':
    main()