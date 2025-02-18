#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


failover_inner_args = dict(
    ha=dict(type='str'),
    vrrp6=dict(type='str'),
    vrrp=dict(type='str')
)

module_args = dict(
    failover=dict(type="dict", options=failover_inner_args, required=True)
)

name = 'restart'


class PaskRestart(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRestart, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    restart = PaskRestart(name, module_args)
    restart.set_param()
    restart.run()
    restart.set_result()


if __name__ == '__main__':
    main()
