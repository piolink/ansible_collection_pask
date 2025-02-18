#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


mirrored_inner_args = dict(
    direction=dict(type='str', required=True),
    mirrored=dict(type='str', required=True)
)

module_args = dict(
    description=dict(type='str'),
    monitor=dict(type='str', required=True),
    mirrored=dict(type='list', elements='dict', options=mirrored_inner_args)
)

required_if = [
    ("state", "present", ["mirrored"])
    ]

name = 'mirroring'


class PaskMirroring(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskMirroring, self).__init__(name, module_args, required_if)

    @try_except
    def run(self):
        data = dict()
        if self.module.params['state'] == "absent":
            data[name] = dict(monitor=self.module.params['monitor'])
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['monitor'])
            self.resp = self.prest.put(url, data)


def main():
    mirroring = PaskMirroring(name, module_args, required_if)
    mirroring.set_param()
    mirroring.run()
    mirroring.set_result()


if __name__ == '__main__':
    main()
