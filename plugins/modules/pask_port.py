#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os, json


flood_rate_inner_args = dict(
    broadcast=dict(type='str'),
    dlf=dict(type='str'),
    multicast=dict(type='str'),
)

param_list = [
    'auto_nego', 'speed', 'duplex', 'flow_ctrl', 'mdi_mdix', 'status',
    'sfp_mode', 'packet_buffer', 'jumbo_frame', 'description'
]
module_args = dict(
    name=dict(type='str', required=True),
    flood_rate=dict(type='dict', options=flood_rate_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'port'


class PaskPort(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPort, self).__init__(name, module_args)
        self.default_values = {
            "copper": {
                "sfp_mode": "--",
                "packet_buffer": "--"
            },
            "fiber": {
                "packet_buffer": "--",
                "duplex": "--",
                "mdi_mdix": "--"
            }
        }

    @try_except
    def run(self):
        url = os.path.join(self.url, self.module.params['name'])
        ret = json.loads(self.prest.get(url).text)
        if ret.get("cable"):
            default_values = self.default_values[ret["cable"]]

        for k, v in default_values.iteritems():
            if self.module.params.get(k) is None:
                self.module.params[k] = v
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(url, data)


def main():
    port = PaskPort(name, module_args)
    port.set_param()
    port.run()
    port.set_result()


if __name__ == '__main__':
    main()