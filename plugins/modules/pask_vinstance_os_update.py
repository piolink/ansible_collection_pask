#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


module_args = dict(
    profile=dict(type="str", required=True)
)

name = 'vinstance-os-update'


class PaskVinstanceOsUpdate(PaskModule):
    def __init__(self, name, module_args):
        super(PaskVinstanceOsUpdate, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    vinstance_os_update = PaskVinstanceOsUpdate(name, module_args)
    vinstance_os_update.set_param()
    vinstance_os_update.run()
    vinstance_os_update.set_result()


if __name__ == '__main__':
    main()