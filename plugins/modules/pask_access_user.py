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

]
module_args = dict(
    status=dict(type='str'),
    max_user=dict(type='str')
)


module_args.update(make_module_args(param_list))

name = 'access-user'


class PaskAccessUser(PaskModule):
    def __init__(self, name, module_args):
        super(PaskAccessUser, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    access_user = PaskAccessUser(name, module_args)
    access_user.set_param()
    access_user.run()
    access_user.set_result()


if __name__ == '__main__':
    main()