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
    'oob', 'reply_with_stored_mac', 'checksum', 'mangle_arp_source_mac',
    'tcp_flag_validation', 'invalid_tcp_forwarding', 'ipv6_defrag_off',
    'ipv6_forwarding', 'update_timeout_unreplied_rst', 'jumbo_frame',
    'proper_sip_in_multipath_route',
    'forced_routing_with_specified_interface', 'sort_compare',
    'client_server_boundary', 'surge_dryrun_analysis', 'top10url_analysis',
    'tcpdump_timeout', 'mgmt_ingress_ratelimit', 'cert_validity', 'ip_acd',
    'l2switching_before_portboundary'
]
module_args = dict(
    authenticate_config_mode=dict(type='str')
)


module_args.update(make_module_args(param_list))

name = 'env'

exclude_underscore_list = [
    'reply_with_stored_mac', 'mangle_arp_source_mac', 'tcp_flag_validation',
    'invalid_tcp_forwarding', 'ipv6_defrag_off', 'ipv6_forwarding',
    'update_timeout_unreplied_rst', 'authenticate_config_mode',
    'proper_sip_in_multipath_route',
    'forced_routing_with_specified_interface', 'tcpdump_timeout',
]


class PaskEnv(PaskModule):
    def __init__(self, name, module_args):
        super(PaskEnv, self).__init__(name, module_args)
        for exclude_underscore_param in exclude_underscore_list:
            self.exclude_underscore_params.add(exclude_underscore_param)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    env = PaskEnv(name, module_args)
    env.set_param()
    env.run()
    env.set_result()


if __name__ == '__main__':
    main()