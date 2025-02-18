#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except


mostouter_params = [
    'status', 'primary_server', 'secondary_server', 'minpoll',
    'maxpoll'
]

module_args = make_module_args(mostouter_params)

name = 'ntp'


class PaskNtp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskNtp, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params)
        self.resp = self.prest.put(self.url, data)


def main():

    ntp = PaskNtp(name, module_args)
    ntp.set_param()
    ntp.run()
    ntp.set_result()


if __name__ == '__main__':
    main()
