#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule, \
    make_module_args, try_except
import os


module_args = dict()

name = 'persist'


class PaskPersist(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPersist, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = dict()
        if self.module.params['state'] == "absent":
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.prest.delete(self.url, data)
        else:
            raise ValueError('only supports deletion. '
                            'state must be set absent.')


def main():
    persist = PaskPersist(name, module_args)
    persist.set_param()
    persist.run()
    persist.set_result()


if __name__ == '__main__':
    main()