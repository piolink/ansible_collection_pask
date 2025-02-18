#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


import_inner_args = dict(
    protocol=dict(type='str'),
    tftp=dict(type='str'),
    sftp=dict(type='str'),
    scp=dict(type='str'),
    http=dict(type='str'),
    ssh_port=dict(type='str'),
    tftp_port=dict(type='str'),
    password=dict(type='str', no_log=True)
)
module_args = dict(
    name=dict(type='str', required=True),
    mode=dict(type='str'),
    copy_crt=dict(type='str'),
)
module_args['import'] = {
    'type': 'dict',
    'options': import_inner_args
}

name = 'ssl'
subname = 'ca-certificate'


class PaskSslCaCertificate(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSslCaCertificate, self).__init__(name, module_args)

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
            url = os.path.join(url, self.module.params['name'])
            resp = self.prest.put(url, data)
        self.resp = resp


def main():
    ssl_ca_certificate = PaskSslCaCertificate(name, module_args)
    ssl_ca_certificate.set_param()
    ssl_ca_certificate.run()
    ssl_ca_certificate.set_result()


if __name__ == '__main__':
    main()