#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


import_from_tftp_inner_args = dict(
    tftp=dict(type='str', required=True),
    interface=dict(type='str'),
)
import_from_sftp_inner_args = dict(
    sftp=dict(type='str', required=True),
    interface=dict(type='str'),
)
import_from_scp_inner_args = dict(
    scp=dict(type='str', required=True),
    interface=dict(type='str'),
)
import_from_inner_args = dict(
    file=dict(type='str', required=True),
    tftp=dict(type='list', elements='dict',
              options=import_from_tftp_inner_args),
    sftp=dict(type='list', elements='dict',
              options=import_from_sftp_inner_args),
    scp=dict(type='list', elements='dict',
             options=import_from_scp_inner_args),
)
module_args = dict(
    import_from=dict(type='list', elements='dict',
                     options=import_from_inner_args)
)

name = 'import-from'


class PaskImportFrom(PaskModule):
    def __init__(self, name, module_args):
        super(PaskImportFrom, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    import_from = PaskImportFrom(name, module_args)
    import_from.set_param()
    import_from.run()
    import_from.set_result()


if __name__ == '__main__':
    main()