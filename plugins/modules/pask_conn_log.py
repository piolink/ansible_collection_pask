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
    line_length=dict(type='str')
)

name = 'conn-log'


class PaskConnLog(PaskModule):
    def __init__(self, name, module_args):
        super(PaskConnLog, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.prest.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            if data.get('line-length') == "":
                data = {'line-length' : None}
            resp = self.prest.post(self.url, data)
        self.resp = resp



def main():
    conn_log = PaskConnLog(name, module_args)
    conn_log.set_param()
    conn_log.run()
    conn_log.set_result()


if __name__ == '__main__':
    main()