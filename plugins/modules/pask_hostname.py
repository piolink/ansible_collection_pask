#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


module_args = dict(
    hostname=dict(type="str")
)

required_if = [
    ("state", "present", ["hostname"])
    ]

name = 'hostname'


class PaskHostname(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskHostname, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        resp = None
        data = self.make_data(self.module.params)
        resp = self.prest.put(self.url, data)
        self.resp = resp


def main():
    hostname = PaskHostname(name, module_args, required_if)
    hostname.set_param()
    hostname.run()
    hostname.set_result()


if __name__ == '__main__':
    main()
