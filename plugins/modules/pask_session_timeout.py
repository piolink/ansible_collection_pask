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
    'icmp', 'icmpv6', 'udp', 'udp_stream', 'tcp_syn_sent',
    'tcp_syn_recv', 'tcp_established', 'tcp_fin_wait',
    'tcp_close_wait', 'tcp_last_ack', 'tcp_wait', 'tcp_close',
    'tcp_unassured'
]
module_args = dict(
    generic=dict(type='str'),
)


module_args.update(make_module_args(param_list))

name = 'session-timeout'


class PaskSessionTimeout(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSessionTimeout, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    session_timeout = PaskSessionTimeout(name, module_args)
    session_timeout.set_param()
    session_timeout.run()
    session_timeout.set_result()


if __name__ == '__main__':
    main()