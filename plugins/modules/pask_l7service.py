#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


vip_protocol_inner_args = dict(
    protocol=dict(type='str', required=True),
    vport=dict(type='list', required=True)
)
vip_inner_args = dict(
    ip=dict(type='str', required=True),
    protocol=dict(type='list', elements='dict',
                  options=vip_protocol_inner_args, required=True)
)
filter_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    type=dict(type='str'),
    sip=dict(type='str'),
    sport=dict(type='str'),
    dip=dict(type='str'),
    dport=dict(type='str'),
)
group_real_inner_args = dict(
    id=dict(type='str', required=True)
)
group_lb_method_rtt_inner_args = dict(
    base=dict(type='str'),
    mode=dict(type='str'),
    active_conns=dict(type='str'),
)
group_lb_method_urlhash_inner_args = dict(
    length=dict(type='str'),
    offset=dict(type='str'),
    starter=dict(type='str'),
    terminator=dict(type='str'),
    algorithm=dict(type='str')
)
group_lb_method_inner_args = dict(
    type=dict(type='str'),
    rtt=dict(type='dict', options=group_lb_method_rtt_inner_args),
    urlhash=dict(type='dict', options=group_lb_method_urlhash_inner_args),
)
group_connection_pooling_inner_args = dict(
    status=dict(type='str'),
    mode=dict(type='str'),
    max_reuse=dict(type='str'),
    pool_size=dict(type='str'),
    timeout=dict(type='str')
)
group_persist_cookie_hash_inner_args = dict(
    name=dict(type='str', required=True),
    offset=dict(type='str', required=True),
    length=dict(type='str', required=True),
)
group_persist_cookie_inner_args = dict(
    type=dict(type='str', required=True),
    name=dict(type='str'),
    info_header=dict(type='str'),
    hash=dict(type='dict', options=group_persist_cookie_hash_inner_args),
    update_interval=dict(type='str'),
    domain=dict(type='str'),
    path=dict(type='str'),
    flags=dict(type='list', elements='str'),
    source=dict(type='str'),
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
    session_key=dict(type='str'),
    field=dict(type='dict', options=group_persist_field_inner_args),
    destination_subnet=dict(type='str'),
    destination_subnet6=dict(type='str'),
    source_subnet=dict(type='str'),
    source_subnet6=dict(type='str'),
    overmax=dict(type='str')
)
group_inner_args = dict(
    name=dict(type='str', required=True),
    real=dict(type='list', elements='dict', options=group_real_inner_args,
              required=True),
    lb_method=dict(type='dict', options=group_lb_method_inner_args),
    connection_pooling=dict(type='dict',
                            options=group_connection_pooling_inner_args),
    persist=dict(type='dict', options=group_persist_inner_args),
    surge_protection=dict(type='str')
)
rule_snat_addr_inner_args = dict(
    network=dict(type='str', required=True),
    nat_ip=dict(type='str', required=True)
)
rule_connection_pooling_inner_args = dict(
    status=dict(type='str'),
    mode=dict(type='str'),
    max_reuse=dict(type='str'),
    pool_size=dict(type='str'),
    timeout=dict(type='str')
)
rule_nat_sip_inner_args = dict(
    network=dict(type='str', required=True),
    nat_ip=dict(type='str', required=True)
)
rule_nat_inner_args = dict(
    status=dict(type='str'),
    mode=dict(type='str'),
    sip=dict(type='list', elements='dict', options=rule_nat_sip_inner_args),
    dip=dict(type='str'),
    dport=dict(type='str'),
    real=dict(type='str'),
)
rule_ssl_decrypt_mirroring_tcp_session_inner_args = dict(
    handshake=dict(type='str'),
    teardown=dict(type='str')
)
rule_ssl_decrypt_mirroring_mirror_message_inner_args = dict(
    request=dict(type='str'),
    response=dict(type='str')
)
rule_ssl_decrypt_mirroring_inner_args = dict(
    status=dict(type='str'),
    interface=dict(type='str'),
    dmac=dict(type='str'),
    dport=dict(type='str'),
    send_delay=dict(type='str'),
    tcp_session=dict(type='dict',
        options=rule_ssl_decrypt_mirroring_tcp_session_inner_args),
    mirror_message=dict(type='dict',
        options=rule_ssl_decrypt_mirroring_mirror_message_inner_args),
)
rule_rewrite_sub_domains_inner_args = dict(
    status=dict(type='str'),
    sub_domains=dict(type='list', elements='dict',
                     options=rule_nat_sip_inner_args)
)
rule_backend_ssl_inner_args = dict(
    profile=dict(type='str'),
    sni=dict(type='str')
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    priority=dict(type='str'),
    status=dict(type='str'),
    pattern=dict(type='str'),
    action=dict(type='str'),
    real=dict(type='str'),
    fail_skip=dict(type='str'),
    group=dict(type='str'),
    backup_group=dict(type='str'),
    http_status=dict(type='str'),
    request_scheme=dict(type='str'),
    specific_dest=dict(type='str'),
    name_resolver=dict(type='str'),
    error_action=dict(type='str'),
    snat_addr_type=dict(type='str'),
    snat_addr=dict(type='list', elements='dict',
                   options=rule_snat_addr_inner_args),
    sure_connect=dict(type='str'),
    surge_protection=dict(type='str'),
    backend_timeout=dict(type='str'),
    adapt_location_scheme=dict(type='str'),
    response_buffering=dict(type='str'),
    url=dict(type='str'),
    send_complete_request=dict(type='str'),
    wait_complete_response=dict(type='str'),
    connection_pooling=dict(type='dict',
                            options=rule_connection_pooling_inner_args),
    preserve_http_version=dict(type='str'),
    urlmanip=dict(type='list', elements='str'),
    headermanip=dict(type='list', elements='str'),
    resource_cloaking=dict(type='list', elements='str'),
    icap=dict(type='str'),
    nat=dict(type='dict', options=rule_nat_inner_args),
    cache=dict(type='str'),
    compression=dict(type='str'),
    ssl_decrypt_mirroring=dict(type='dict',
                               options=rule_ssl_decrypt_mirroring_inner_args),
    backend_ssl=dict(type='dict',
                               options=rule_backend_ssl_inner_args),
)
snat_addr_inner_args = dict(
    network=dict(type='str', required=True),
    nat_ip=dict(type='str', required=True)
)
return_to_sender_rts_real_inner_args = dict(
    id=dict(type='str', required=True),
    ip=dict(type='str', required=True),
    mac=dict(type='str'),
    interface=dict(type='str'),
)
return_to_sender_inner_args = dict(
    status=dict(type='str'),
    rts_real=dict(type='list', elements='dict',
                  options=return_to_sender_rts_real_inner_args)
)
timeout_inner_args = dict(
    status=dict(type='str'),
    keepalive_timeout=dict(type='str'),
    request_header_timeout=dict(type='str'),
    request_body_interval=dict(type='str')
)
request_buffering_inner_args = dict(
    status=dict(type='str'),
    header_buffer_size=dict(type='str'),
    body_temp_size=dict(type='str'),
    body_max_size=dict(type='str'),
    preserve_chunked=dict(type='str')
)
html_inner_args = dict(
    name=dict(type='str', required=True),
    mode=dict(type='str'),
    type=dict(type='str'),
    description=dict(type='str'),
    title=dict(type='str'),
    body=dict(type='str'),
    url=dict(type='str'),
    code=dict(type='str'),
    interval=dict(type='str')
)
sure_connect_inner_args = dict(
    id=dict(type='str', required=True),
    response_code=dict(type='str'),
    ignore_server_error=dict(type='str'),
    rps_check_mode=dict(type='str'),
    rps=dict(type='str'),
    concurr_req=dict(type='str'),
    first_priority=dict(type='str'),
    timeout_correction=dict(type='str'),
    html=dict(type='str'),
    url=dict(type='str'),
    cookie_expire=dict(type='str')
)
surge_protection_syslog_logging_inner_args = dict(
    status=dict(type='str'),
    interval=dict(type='str')
)
surge_protection_inner_args = dict(
    id=dict(type='str', required=True),
    base_threshold=dict(type='str'),
    upper=dict(type='str'),
    throttle_burst=dict(type='str'),
    throttle_burst_delay=dict(type='str'),
    queue_size=dict(type='str'),
    wait_timeout=dict(type='str'),
    throttle=dict(type='str'),
    target=dict(type='str'),
    rps=dict(type='str'),
    dry_run=dict(type='str'),
    syslog_logging=dict(type='dict',
                        options=surge_protection_syslog_logging_inner_args),
)
backend_timeout_inner_args = dict(
    id=dict(type='str', required=True),
    response_timeout=dict(type='str')
)
response_buffering_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    header_buffer_size=dict(type='str'),
    body_temp_size=dict(type='str'),
    body_max_size=dict(type='str'),
    ignore_header=dict(type='str')
)
error_management_custom_response_inner_args = dict(
    status=dict(type='str'),
    error_code=dict(type='list', elements='str'),
    response_code=dict(type='str'),
    response_html=dict(type='str'),
    redirect_uri=dict(type='str')
)
error_management_inner_args = dict(
    status=dict(type='str'),
    default_error_code=dict(type='str'),
    custom_response=dict(type='dict',\
        options=error_management_custom_response_inner_args),
)
ssl_decrypt_mirroring_tcp_session_inner_args = dict(
    handshake=dict(type='str'),
    teardown=dict(type='str')
)
ssl_decrypt_mirroring_mirror_message_inner_args = dict(
    request=dict(type='str'),
    response=dict(type='str')
)
ssl_decrypt_mirroing_inner_args = dict(
    status=dict(type='str'),
    interface=dict(type='str'),
    dmac=dict(type='str'),
    dport=dict(type='str'),
    send_delay=dict(type='str'),
    tcp_session=dict(type='dict',
                     options=ssl_decrypt_mirroring_tcp_session_inner_args),
    mirror_message=dict(type='dict',
        options=ssl_decrypt_mirroring_mirror_message_inner_args),
)
rewrite_sub_domains_inner_args = dict(
    status=dict(type='str'),
    sub_domains=dict(type='list', elements='str')
)
log_inner_args = dict(
    access_log=dict(type='str'),
    connection_log=dict(type='str')
)
top10url_inner_args = dict(
    status=dict(type='str'),
    sort=dict(type='str'),
    time=dict(type='str')
)
user_auth_inner_args = dict(
    status=dict(type='str'),
    auth_url=dict(type='str'),
    client_id=dict(type='str'),
    client_secret=dict(type='str'),
    redirect_uri=dict(type='str'),
    grant_type=dict(type='str'),
    token_url=dict(type='str'),
    jwks_url=dict(type='str'),
    jwt_alg=dict(type='str'),
    jwt_authkey=dict(type='str')
)
cookie_encryption_inner_args = dict(
    status=dict(type='str'),
    algorithm=dict(type='str'),
    mode=dict(type='str'),
    server_cookies=dict(type='list', elements='str'),
    protection_action=dict(type='str'),
    passphrase=dict(type='str')
)
urlmanip_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    priority=dict(type='str'),
    manip_type=dict(type='str'),
    https_for_redirect=dict(type='str'),
    method=dict(type='str'),
    match=dict(type='str'),
    replace=dict(type='str'),
    value=dict(type='str', required=True)
)
headermanip_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    header=dict(type='str', required=True),
    value=dict(type='str'),
)
resource_cloaking_inner_args = dict(
    id=dict(type='str', required=True),
    mode=dict(type='str'),
    header=dict(type='str', required=True),
    match=dict(type='str'),
    pattern=dict(type='str'),
    replace=dict(type='str'),
    http_response_status=dict(type='str'),
    value=dict(type='str'),
    cookie_path=dict(type='str'),
    cookie_secure_mode=dict(type='str'),
    cookie_httponly_mode=dict(type='str'),
    cookie_samesite_mode=dict(type='str'),
    cookie_samesite_value=dict(type='str')
)

param_list = [
    'priority', 'status', 'keep_backup', 'server_min_mtu', 'age_refresh',
    'allow_nonhttp', 'direct_connect', 'no_cache',
    'passive_health_check', 'x_forwarded_for', 'preserve_src_addr',
    'preserve_src_port', 'proxy_protocol','snat_addr_type', 'prescript',
    'connection_pooling', 'default_server_header', 'fail_action', 'cache',
    'ssl', 'ssl_detection', 'front_end_optimize', 'http2', 'websocket',
    'max_rps', 'get_flooding_protection', 'cc_attack_protection',
    'slowloris_protection', 'slowpost_protection', 'ssl_session_cache_sync'
]
module_args = dict(
    name=dict(type='str', required=True),
    vip=dict(type='list', elements='dict', options=vip_inner_args),
    filter=dict(type='list', elements='dict', options=filter_inner_args),
    group=dict(type='list', elements='dict', options=group_inner_args),
    rule=dict(type='list', elements='dict', options=rule_inner_args),
    health_check=dict(type='list', elements='str'),
    host=dict(type='list', elements='str'),
    snat_addr=dict(type='list', elements='dict',
                   options=snat_addr_inner_args),
    return_to_sender=dict(type='dict', options=return_to_sender_inner_args),
    timeout=dict(type='dict', options=timeout_inner_args),
    request_buffering=dict(type='dict', options=request_buffering_inner_args),
    html=dict(type='list', elements='dict', options=html_inner_args),
    sure_connect=dict(type='list', elements='dict',
                      options=sure_connect_inner_args),
    surge_protection=dict(type='list', elements='dict',
                          options=surge_protection_inner_args),
    backend_timeout=dict(type='list', elements='dict',
                         options=backend_timeout_inner_args),
    response_buffering=dict(type='list', elements='dict',
                            options=response_buffering_inner_args),
    error_management=dict(type='dict',
                            options=error_management_inner_args),
    ssl_decrypt_mirroring=dict(type='dict',
                            options=ssl_decrypt_mirroing_inner_args),
    rewrite_sub_domains=dict(type='dict',
                            options=rewrite_sub_domains_inner_args),
    log=dict(type='dict', options=log_inner_args),
    top10url=dict(type='dict', options=top10url_inner_args),
    user_auth=dict(type='dict', options=user_auth_inner_args),
    cookie_encryption=dict(type='dict', options=cookie_encryption_inner_args),
    urlmanip=dict(type='list', elements='dict',
                  options=urlmanip_inner_args),
    headermanip=dict(type='list', elements='dict',
                  options=headermanip_inner_args),
    resource_cloaking=dict(type='list', elements='dict',
                  options=resource_cloaking_inner_args)
)

module_args.update(make_module_args(param_list))

name = 'l7service'


class PaskL7service(PaskModule):
    def __init__(self, name, module_args):
        super(PaskL7service, self).__init__(name, module_args)
        self.exclude_underscore_params.add('concurr_req')

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
    l7service = PaskL7service(name, module_args)
    l7service.set_param()
    l7service.run()
    l7service.set_result()


if __name__ == '__main__':
    main()