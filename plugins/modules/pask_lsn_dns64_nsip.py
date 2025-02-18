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
    nsip=dict(type='list', elements='str')
)


name = 'lsn'
subname = 'dns64-nsip'


class PaskLsnDns64Nsip(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLsnDns64Nsip, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(url, data)


def main():
    lsn_dns64_nsip = PaskLsnDns64Nsip(name, module_args)
    lsn_dns64_nsip.set_param()
    lsn_dns64_nsip.run()
    lsn_dns64_nsip.set_result()


if __name__ == '__main__':
    main()