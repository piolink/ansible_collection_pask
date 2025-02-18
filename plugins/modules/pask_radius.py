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
    'primary_server', 'secondary_server', 'port', 'secret', 'retry',
    'timeout', 'console', 'ssh', 'telnet', 'web', 'prest_api'
]
module_args = dict(
    status=dict(type='str'),
)


module_args.update(make_module_args(param_list))

name = 'radius'


class PaskRadius(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRadius, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        if self.module.params['state'] == "absent":
            # secret 삭제 Validation을 회피(secret 항목을 제외하고 삭제)
            data['secret'] = '********'
        self.resp = self.prest.put(self.url, data)


def main():
    radius = PaskRadius(name, module_args)
    radius.set_param()
    radius.run()
    radius.set_result()


if __name__ == '__main__':
    main()