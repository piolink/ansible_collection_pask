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
    id=dict(type='str', required=True)
)

name = 'user-session'


class PaskUserSession(PaskModule):
    def __init__(self, name, module_args):
        super(PaskUserSession, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = dict()
        if self.module.params['state'] == "absent":
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            url = os.path.join(self.url, self.module.params['id'])
            self.resp = self.prest.delete(url, data)
        else:
            raise ValueError('only supports deletion. '
                            'state must be set absent.')


def main():
    user_session = PaskUserSession(name, module_args)
    user_session.set_param()
    user_session.run()
    user_session.set_result()


if __name__ == '__main__':
    main()