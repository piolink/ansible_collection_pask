#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except


inner_save_args = dict(
    anonymize=dict(type='str')
)
inner_tftp_args = dict(
    tftp=dict(type='str', required=True),
    interface=dict(type='str')
)

inner_ftp_args = dict(
    ftp=dict(type='str', required=True),
    interface=dict(type='str')
)

inner_sftp_args = dict(
    sftp=dict(type='str', required=True),
    interface=dict(type='str')
)

inner_scp_args = dict(
    scp=dict(type='str', required=True),
    interface=dict(type='str')
)

inner_copy_to_args = dict(
    tftp=dict(type='list', elements='dict',
                   options=inner_tftp_args),
    ftp=dict(type='list', elements='dict',
                    options=inner_ftp_args),
    sftp=dict(type='list', elements='dict', options=inner_sftp_args),
    scp=dict(type='list', elements='dict', options=inner_scp_args),
)


module_args = dict(
    save=dict(type="dict", options=inner_save_args),
    clear=dict(type="str"),
    copy_to=dict(type="dict", options=inner_copy_to_args),
)

name = 'tech-assist'


class PaskTechAssist(PaskModule):
    def __init__(self, name, module_args):
        super(PaskTechAssist, self).__init__(name, module_args)

    def run(self):
        data = dict()
        save = self.module.params.get('save')
        if save is not None and save.get('anonymize') is None:
            data['save'] = "true"
        else:
            data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.post(self.url, data)


def main():
    tech_assist = PaskTechAssist(name, module_args)
    tech_assist.set_param()
    tech_assist.run()
    tech_assist.set_result()


if __name__ == '__main__':
    main()
