#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule, \
    make_module_args, try_except
import os


ip_version_inner_args = dict(
    ip_version=dict(type='str', required=True),
)
ip_inner_args = dict(
    ip=dict(type='str', required=True),
)
sip_inner_args = dict(
    sip=dict(type='str', required=True),
)
dip_inner_args = dict(
    dip=dict(type='str', required=True),
)
port_inner_args = dict(
    port=dict(type='str', required=True),
)
sport_inner_args = dict(
    sport=dict(type='str', required=True),
)
dport_inner_args = dict(
    dport=dict(type='str', required=True),
)
protocol_inner_args = dict(
    protocol=dict(type='str', required=True),
)
service_inner_args = dict(
    service=dict(type='str', required=True),
    name=dict(type='str')
)
real_inner_args = dict(
    real=dict(type='str', required=True),
)
module_args = dict(
    ip_version=dict(type='list', elements='dict',
                    options=ip_version_inner_args),
    ip=dict(type='list', elements='dict',
                    options=ip_inner_args),
    sip=dict(type='list', elements='dict',
                    options=sip_inner_args),
    dip=dict(type='list', elements='dict',
                    options=dip_inner_args),
    port=dict(type='list', elements='dict',
                    options=port_inner_args),
    sport=dict(type='list', elements='dict',
                    options=sport_inner_args),
    dport=dict(type='list', elements='dict',
                    options=dport_inner_args),
    protocol=dict(type='list', elements='dict',
                    options=protocol_inner_args),
    service=dict(type='list', elements='dict',
                    options=service_inner_args),
    real=dict(type='list', elements='dict',
                    options=real_inner_args),
)

name = 'entry-l7'


class PaskEntryL7(PaskModule):
    def __init__(self, name, module_args):
        super(PaskEntryL7, self).__init__(name, module_args)

    @try_except
    def run(self):
        params = self.make_params_query_string(self.module.params)
        data = dict()
        if self.module.params['state'] == "absent":
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data, params=params)
        else:
            raise ValueError('only supports deletion. '
                            'state must be set absent.')


def main():
    entry_l7 = PaskEntryL7(name, module_args)
    entry_l7.set_param()
    entry_l7.run()
    entry_l7.set_result()


if __name__ == '__main__':
    main()