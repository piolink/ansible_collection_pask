#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


clear_statistics_inner_args = dict(
    type=dict(type='str', required=True),
    name=dict(type='str')
)
module_args = dict(
    clear_statistics=dict(type='list', elements='dict',
                     options=clear_statistics_inner_args)
)

name = 'clear-statistics'


class PaskClearStatistics(PaskModule):
    def __init__(self, name, module_args):
        super(PaskClearStatistics, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = dict()
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    clear_statistics = PaskClearStatistics(name, module_args)
    clear_statistics.set_param()
    clear_statistics.run()
    clear_statistics.set_result()


if __name__ == '__main__':
    main()