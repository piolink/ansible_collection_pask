#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except
import json


name = 'port-statistics'

module_args = dict()


class PaskPortStatistics(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPortStatistics, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = dict()
        resp = self.prest.get(self.url)
        resp_dict = json.loads(resp.text)
        data = resp_dict
        self.resp = self.prest.delete(self.url, data)


def main():
    port_statistics = PaskPortStatistics(name, module_args)
    port_statistics.set_param()
    port_statistics.run()
    port_statistics.set_result()


if __name__ == '__main__':
    main()