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
    id=dict(type='str', required=True),
    type=dict(type='str'),
    pattern_repr=dict(type='str'),
    description=dict(type='str'),
    match=dict(type='str'),
    user_defined=dict(type='str'),
    length=dict(type='str'),
    offset=dict(type='str'),
    string=dict(type='str'),
    source_ip=dict(type='str'),
    dest_ip=dict(type='str'),
    source_port=dict(type='str'),
    dest_port=dict(type='str'),
    scheme=dict(type='str'),
    version=dict(type='str'),
    sni_string=dict(type='list', elements='str'),
    p2p_protocol=dict(type='str'),
)

name = 'layer7'
subname = 'pattern'

class PaskLayer7Pattern(PaskModule):
    def __init__(self, name, module_args):
        super(PaskLayer7Pattern, self).__init__(name, module_args)

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
    layer7pattern = PaskLayer7Pattern(name, module_args)
    layer7pattern.set_param()
    layer7pattern.run()
    layer7pattern.set_result()


if __name__ == '__main__':
    main()