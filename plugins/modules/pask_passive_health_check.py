#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


failnext_inner_args = dict(
    time=dict(type='str'),
    count=dict(type='str'),
    client_error=dict(type='str'),
    request_data=dict(type='str')
)

param_list = [
    'type', 'failures', 'failures_interval', 'response_time', 'retry_time',
    'check_until_up', 'status', 'description'
]
module_args = dict(
    id=dict(type='str', required=True),
    check_type=dict(type='list', elements='str'),
    failnext=dict(type='dict', options=failnext_inner_args)
)

module_args.update(make_module_args(param_list))

name = 'passive-health-check'


class PaskPassiveHealthCheck(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPassiveHealthCheck, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['id'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    passive_health_check = PaskPassiveHealthCheck(name, module_args)
    passive_health_check.set_param()
    passive_health_check.run()
    passive_health_check.set_result()


if __name__ == '__main__':
    main()