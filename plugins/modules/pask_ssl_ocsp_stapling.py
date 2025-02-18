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
    uri=dict(type='str'),
    import_crt=dict(type='str'),
    verify=dict(type='str'),
    resolver=dict(type='str'),
)

required_if = [
    ("state", "present", ["import_crt"])
    ]

name = 'ssl'
subname = 'ocsp-stapling'

class PaskSslOcspStapling(PaskModule):
    def __init__(self, name, module_args, required_if):
        super(PaskSslOcspStapling, self).__init__(
            name, module_args, required_if)

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
    ssl_ocsp_stapling = PaskSslOcspStapling(name, module_args, required_if)
    ssl_ocsp_stapling.set_param()
    ssl_ocsp_stapling.run()
    ssl_ocsp_stapling.set_result()


if __name__ == '__main__':
    main()