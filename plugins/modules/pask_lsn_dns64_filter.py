#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


dns64_filter_include_filter_inner_args = dict(
    include=dict(type='str', required=True)
)
dns64_filter_exclude_filter_inner_args = dict(
    exclude=dict(type='str', required=True)
)

module_args = dict(
    id=dict(type='str', required=True),
    include_filter=dict(type='list', elements='dict',
                        options=dns64_filter_include_filter_inner_args),
    exclude_filter=dict(type='list', elements='dict',
                        options=dns64_filter_exclude_filter_inner_args),
)


name = 'lsn'
subname = 'dns64-filter'


class PaskLsnDns64Filter(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLsnDns64Filter, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, subname)
        if self.module.params['state'] == "absent":
            data = dict()
            data[subname] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(url, self.module.params['id'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    lsn_dns64_filter = PaskLsnDns64Filter(name, module_args)
    lsn_dns64_filter.set_param()
    lsn_dns64_filter.run()
    lsn_dns64_filter.set_result()


if __name__ == '__main__':
    main()