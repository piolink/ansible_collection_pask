#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


congestion_control_inner_args = dict(
    window_scaling=dict(type='str'),
    ecn=dict(type='str'),
    timestamps=dict(type='str')
)

recovery_inner_args = dict(
    sack=dict(type='str'),
    dsack=dict(type='str'),
    frto=dict(type='str'),
    retransmission=dict(type='str'),
    reordering=dict(type='str')
)

socket_buffer_inner_args = dict(
    receive_buffer=dict(type='str'),
    send_buffer=dict(type='str'),
    dynamic_receive=dict(type='str')
)

module_args = dict(
    congestion_control=dict(
        type='dict', options=congestion_control_inner_args),
    recovery=dict(type='dict', options=recovery_inner_args),
    socket_buffer=dict(type='dict', options=socket_buffer_inner_args),
)

name = 'tcp-tuning'


class PaskTcpTuning(PaskModule):
    def __init__(self, name, module_args):
        super(PaskTcpTuning, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    tcp_tuning = PaskTcpTuning(name, module_args)
    tcp_tuning.set_param()
    tcp_tuning.run()
    tcp_tuning.set_result()


if __name__ == '__main__':
    main()