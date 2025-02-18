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
    'next_boot'
]
module_args = dict(
    name=dict(type='str', required=True)
)


module_args.update(make_module_args(param_list))

name = 'port-breakout'


class PaskPortBreakout(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPortBreakout, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        url = os.path.join(self.url, self.module.params['name'])
        resp = self.prest.put(url, data)
        self.resp = resp


def main():
    port_breakout = PaskPortBreakout(name, module_args)
    port_breakout.set_param()
    port_breakout.run()
    port_breakout.set_result()


if __name__ == '__main__':
    main()