#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


user_inner_args = dict(
    name=dict(type='str', required=True),
    password=dict(type='str', no_log=True),
    config_password=dict(type='str', no_log=True),
    level=dict(type='str'),
    description=dict(type='str'),
    log=dict(type='str')
)
strong_password_inner_args = dict(
    status=dict(type='str'),
    minimum_length=dict(type='str'),
    required_character=dict(
        lowercase=dict(type='str'),
        uppercase=dict(type='str'),
        numeric=dict(type='str'),
        special=dict(type='str')
    )
)
lockout_inner_args=dict(
    maximum_login_failures=dict(type='str'),
    failed_login_timeout=dict(type='str')
)
password_duration_inner_args=dict(
    maximum_duration=dict(type='str'),
    expiration_warning=dict(type='str')
)
password_policy_inner_args = dict(
    strong_password=dict(type='dict', options=strong_password_inner_args),
    lockout=dict(type='dict', options=lockout_inner_args),
    password_duration=dict(
        type='dict', options=password_duration_inner_args
    )
)
module_args = dict(
    user=dict(type='list', elements='dict', options=user_inner_args),
    password_policy=dict(type='dict', options=password_policy_inner_args)
)

name = 'auth'


class PaskAuth(PaskModule):
    def __init__(self, name, module_args):
        super(PaskAuth, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    auth = PaskAuth(name, module_args)
    auth.set_param()
    auth.run()
    auth.set_result()


if __name__ == '__main__':
    main()
