#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


module_args = dict(
    host=dict(type='str', required=True)
)

name = 'rdate'


class PaskRdate(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRdate, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    rdate = PaskRdate(name, module_args)
    rdate.set_param()
    rdate.run()
    rdate.set_result()


if __name__ == '__main__':
    main()