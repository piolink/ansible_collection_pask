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
    monitor_port=dict(type='list', elements='str'),
    sync_port=dict(type='list', elements='str'),
    id=dict(type='str', required=True),
    **make_module_args(
        ["status", "link_check_delay", "sync_delay_time", "mode"])
)

name = 'link-sync'


class PaskLinkSync(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLinkSync, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data[name] = dict(id=self.module.params['id'])
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['id'])
            self.resp = self.prest.put(url, data)


def main():
    link_sync = PaskLinkSync(name, module_args)
    link_sync.set_param()
    link_sync.run()
    link_sync.set_result()


if __name__ == '__main__':
    main()
