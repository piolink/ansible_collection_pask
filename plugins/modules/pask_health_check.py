#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


str_param_list = [
    'type', 'recover', 'timeout', 'interval', 'status', 'retry',
    'sip', 'tip', 'uri', 'host', 'user_agent', 'expect', 'unexpect',
    'content_length', 'increase_icmp_id', 'tolerance', 'sni',
    'update_delay', 'oid', 'half_open', 'send', 'filename', 'packets',
    'radius_auth_name', 'port', 'radius_auth_passwd', 'radius_auth_secret',
    'radius_acct_secret', 'version', 'validate', 'common_name', 'description',
    'source_port_min', 'source_port_max', 'mac', 'community', 'record_type',
    'query', 'dip', 'dscp', 'dscp_tip', 'graceful_shutdown', 'inner_tip'
]

module_args = dict(
    id=dict(type='str', required=True),
    status_code=dict(type='list', elements='str'),
    script=dict(type='list', elements='dict')
)

module_args.update(make_module_args(str_param_list))

name = 'health-check'


class PaskHealthcheck(PaskModule):
    def __init__(self, name, module_args):
        super(PaskHealthcheck, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            url = os.path.join(self.url, self.module.params['id'])
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['id'])
            self.resp = self.prest.put(url, data)


def main():
    hc = PaskHealthcheck(name, module_args)
    hc.set_param()
    hc.run()
    hc.set_result()


if __name__ == '__main__':
    main()
