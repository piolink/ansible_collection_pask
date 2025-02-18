#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except
import os


cpu_inner_args = dict(
    threshold=dict(type='str')
)

memory_inner_args = dict(
    threshold=dict(type='str')
)

log_storage_inner_args = dict(
    threshold=dict(type='str')
)

module_args = dict(
    cpu=dict(type='dict', options=cpu_inner_args),
    memory=dict(type='dict', options=memory_inner_args),
    log_storage=dict(type='dict', options=log_storage_inner_args),
)


name = 'watch-system'


class PaskWatchSystem(PaskModule):
    def __init__(self, name, module_args):
        super(PaskWatchSystem, self).__init__(name, module_args)
        self.exclude_underscore_params.add('log_storage')

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    watch_system = PaskWatchSystem(name, module_args)
    watch_system.set_param()
    watch_system.run()
    watch_system.set_result()


if __name__ == '__main__':
    main()