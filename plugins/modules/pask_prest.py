#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    try_except
import json


module_args = dict(
    uri=dict(type='str', required=True),
    data=dict(type='str'),
    method=dict(type='str')
)

name = 'prest'


class PaskPrest(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPrest, self).__init__(name, module_args)

    @try_except
    def run(self):
        resp = None
        rest_method = ['get', 'post', 'put', 'delete']
        if self.module.params['method'] not in rest_method:
            return self.result
        url = 'https://{0}:{1}{2}'.format(self.module.params['prest_ip'],
                                          self.module.params['prest_port'],
                                          self.module.params['uri'])
        if self.module.params['data'] is not None:
            data = json.loads(self.module.params['data'])

        if self.module.params['method'] == 'get':
            resp = self.prest.get(url)
        elif self.module.params['method'] == 'post':
            resp = self.prest.post(url, data)
        elif self.module.params['method'] == 'put':
            resp = self.prest.put(url, data)
        elif self.module.params['method'] == 'delete':
            resp = self.prest.delete(url, data)

        if resp is not None:
            self.resp = resp


def main():
    prest = PaskPrest(name, module_args)
    prest.set_param()
    prest.run()
    prest.set_result()


if __name__ == '__main__':
    main()
