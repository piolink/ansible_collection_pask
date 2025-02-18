#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


group_inner_args = dict(
    name=dict(type='str', required=True),
    surge_protection=dict(type='str')
)
rule_inner_args = dict(
    id=dict(type='str', required=True),
    status=dict(type='str'),
    sure_connect=dict(type='str')
)

param_list = [
    'month', 'day', 'hour', 'minute', 'second', 'type', 'description',
    'service_type', 'service_name', 'service_status', 'email_alarm', 'status',
    'certificate'
]
module_args = dict(
    id=dict(type='str', required=True),
    week=dict(type='list', elements='str'),
    group=dict(type='list', elements='dict', options=group_inner_args),
    rule=dict(type='list', elements='dict', options=rule_inner_args)
)


module_args.update(make_module_args(param_list))

name = 'schedule-manager'


class PaskScheduleManager(PaskModule):
    def __init__(self, name, module_args):
        super(PaskScheduleManager, self).__init__(name, module_args)

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
    schedule_manager = PaskScheduleManager(name, module_args)
    schedule_manager.set_param()
    schedule_manager.run()
    schedule_manager.set_result()


if __name__ == '__main__':
    main()