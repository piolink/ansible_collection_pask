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
    date=dict(type='str', required=True)
)

name = 'date'


class PaskDate(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDate, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    date = PaskDate(name, module_args)
    date.set_param()
    date.run()
    date.set_result()


if __name__ == '__main__':
    main()