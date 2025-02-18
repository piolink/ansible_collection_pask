#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


ip_inner_args = dict(
    address=dict(type='str', required=True),
    broadcast=dict(type='str'),
    overlapped=dict(type='str')
)
ip6_inner_args = dict(
    address=dict(type='str', required=True),
    broadcast=dict(type='str'),
    adv_on_link=dict(type='str'),
    adv_autonomous=dict(type='str'),
    adv_router_addr=dict(type='str'),
    adv_valid_lifetime=dict(type='str'),
    adv_preferred_lifetime=dict(type='str')
)

param_list = [
    'status', 'adv_send_advert', 'adv_default_lifetime',
    'min_rtr_adv_interval', 'max_rtr_adv_interval', 'adv_cur_hop_limit',
    'adv_reachable_time', 'adv_retrans_timer', 'mtu', 'arp_ignore',
    'arp_announce', 'description', 'rpf'
]
module_args = dict(
    name=dict(type='str', required=True),
    ip=dict(type='list', elements='dict', options=ip_inner_args),
    ip6=dict(type='list', elements='dict', options=ip6_inner_args)
)

module_args.update(make_module_args(param_list))


name = 'interface'


class PaskInterface(PaskModule):
    def __init__(self, name, module_args):
        super(PaskInterface, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        url = os.path.join(self.url, self.module.params['name'])
        resp = self.prest.put(url, data)
        self.resp = resp


def main():
    interface = PaskInterface(name, module_args)
    interface.set_param()
    interface.run()
    interface.set_result()


if __name__ == '__main__':
    main()