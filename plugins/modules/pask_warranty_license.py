#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


warranty_license_inner_args = dict(
    license=dict(type="str", required=True),
    lvc=dict(type="str"),
)

module_args = dict(
    warranty_license=dict(type="list", elements='dict',
                          options=warranty_license_inner_args)
)

name = 'warranty-license'


class PaskWarrantyLicense(PaskModule):
    def __init__(self, name, module_args):
        super(PaskWarrantyLicense, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    warranty_license = PaskWarrantyLicense(name, module_args)
    warranty_license.set_param()
    warranty_license.run()
    warranty_license.set_result()


if __name__ == '__main__':
    main()