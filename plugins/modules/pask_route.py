#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible.module_utils.basic import missing_required_lib
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
try:
    import netaddr
    HAS_NETADDR = True
except ImportError:
    HAS_NETADDR = False
import json


network_gateway_health_check_inner_args = dict(
    id=dict(type='str', required=True)
)
network_gateway_inner_args = dict(
    gateway=dict(type='str', required=True),
    priority=dict(type='str'),
    health_check=dict(type='list', elements='dict',
                   options=network_gateway_health_check_inner_args)
)
network_interface_inner_args = dict(
    interface=dict(type='str', required=True),
    priority=dict(type='str'),
    health_check=dict(type='list', elements='dict',
                   options=network_gateway_health_check_inner_args)
)

network_inner_args = dict(
    dest=dict(type='str', required=True),
    gateway=dict(type='list', elements='dict',
                 options=network_gateway_inner_args),
    interface=dict(type='list', elements='dict',
                   options=network_interface_inner_args),
    description=dict(type='str')
)
default_gateway_health_check_inner_args = dict(
    id=dict(type='str', required=True)
)

default_gateway_inner_args = dict(
    gateway=dict(type='str', required=True),
    health_check=dict(type='list', elements='dict',
                 options=default_gateway_health_check_inner_args),
    priority=dict(type='str')
)

module_args = dict(
    network=dict(type='list', elements='dict', options=network_inner_args),
    default_gateway=dict(type='list', elements='dict',
                         options=default_gateway_inner_args)
)

name = 'route'


class PaskRoute(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRoute, self).__init__(name, module_args)

        if not HAS_NETADDR:
            self.module.fail_json(msg=missing_required_lib('netaddr'))

    @try_except
    def run(self):
        interface_url = self.url.replace(name, 'interface')
        resp = self.prest.get(interface_url)
        resp_dict = json.loads(resp.text)

        if_list = self.get_if_and_ip(resp_dict['interface'])

        route_data = self.make_route_data_from_interface(if_list)
        data = self.make_data(self.module.params, include_inner=True)

        if data.get('network') is None:
            data['network'] = route_data
        else:
            data['network'].extend(route_data)

        self.resp = self.prest.put(self.url, data)

    def get_if_and_ip(self, data):
        """
            return value example
        [
            {'interface': 'mgmt', 'ip': '192.168.214.145/24'},
            {'interface': 'v2933', 'ip': '10.10.10.100/24'},
            {'interface': 'v2933', 'ip': '10.10.10.100/28'}
        ]
        """
        if_list = list()
        for interface in data:
            if interface.get('status') == 'down':
                continue
            if interface.get('ip') is None:
                continue

            if isinstance(interface['ip'], list):
                for ip in interface['ip']:
                    d = {
                        'ip': ip['address'],
                        'interface': interface['name']
                    }
                    if_list.append(d)
            else:
                d = {
                    'ip': interface['ip']['address'],
                    'interface': interface['name']
                }
                if_list.append(d)
        return if_list

    def make_route_data_from_interface(self, if_list):
        network = list()
        for _if in if_list:
            net = netaddr.IPNetwork(_if['ip'])
            dest = str(net.network) + "/" + str(net.prefixlen)
            d = {
                "dest": dest,
                "interface": {
                    "interface": _if['interface']
                }
            }
            network.append(d)
        return network


def main():
    route = PaskRoute(name, module_args)
    route.set_param()
    route.run()
    route.set_result()


if __name__ == '__main__':
    main()
