# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

import os
import json
from functools import wraps
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six import iteritems
from ansible_collections.piolink.pask.plugins.module_utils.pask_prestapi import PrestApi


def make_module_args(param):
    d = dict()
    for p in param:
        d[p] = dict(type='str')
    return d


def try_except(func):
    @wraps(func)
    def applicator(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except ValueError as e:
            result = dict()
            result['failed'] = True
            result['message'] = e.message
            self.module.exit_json(**result)
        except Exception:
            result = dict()
            result['failed'] = True
            result['message'] = 'pask module error'
            self.module.exit_json(**result)

    return applicator


class PaskModule(object):
    def __init__(self, name, module_args, required_if=None):
        self.module_args = module_args
        self.basic_module_args = dict(
            prest_ip=dict(type='str', required=True),
            prest_port=dict(type='str', required=True),
            user_id=dict(type='str', required=True),
            user_pw=dict(type='str', required=True, no_log=True),
            state=dict(type='str', default="present",
                       choices=['present', 'absent', 'command'])
        )
        self.param = None
        self.path_name = name
        self.data_name = name
        self.init_ansible(required_if)
        self.prest = PrestApi(self.module)
        self.set_param()
        self.exclude_params = [
            'prest_ip', 'prest_port', 'state', 'user_id', 'user_pw'
        ]
        self.resp = None
        self.user_id = 'root'
        self.user_pw = 'admin'
        self.ok_error_msg = dict()
        self.exclude_underscore_params = set()

    def init_ansible(self, required_if=None):
        self.module_args.update(self.basic_module_args)
        result = dict(
            original_message='',
            message='',
            debug=''
        )

        module = AnsibleModule(
            argument_spec=self.module_args,
            supports_check_mode=True,
            required_if=required_if
        )
        self.result = result
        self.module = module

        if self.module.check_mode:
            return self.result

    def set_param(self):
        self.user_id = self.module.params['user_id']
        self.user_pw = self.module.params['user_pw']
        self.prest.set_headers(self.user_id, self.user_pw)
        self.prefix_url = 'https://{0}:{1}/prestapi/v2/conf/'.format(
            self.module.params['prest_ip'], self.module.params['prest_port'])

        self.url = os.path.join(self.prefix_url, self.path_name.replace('_','-'))

    def make_delete_data(self, module_name, key, value):
        d = {
            module_name: {key: value}
        }
        return d

    def make_data(self, params, include_inner=False):
        data = dict()
        for k, v in iteritems(params):
            if k in self.exclude_params:
                continue
            if k not in self.exclude_underscore_params:
                k = k.replace('_', '-')
            if type(v) is dict:
                if include_inner:
                    inner_dict = self.make_data(v, include_inner)
                    data[k] = inner_dict
                else:
                    pass
            elif type(v) is list:
                if include_inner:
                    inner_list = list()
                    for _v in v:
                        if type(_v) is dict:
                            inner_dict = self.make_data(_v, include_inner)
                            inner_list.append(inner_dict)
                        else:
                            inner_list.append(_v)
                    data[k] = inner_list
            elif v is not None and v != "None":
                data.update({k: v})
        return data

    def make_params_query_string(self, params):
        '''아래 예시와 같이 하위 param 명이 같은 경우는
        고려되지 않아 검토가 필요합니다.
        ex) params 값 예시(하위 param - threshold 이름이 같음)
        {
            'memory' : [{'threshold' : '1'},{'test' : '1'}]
            'log_storage' : [{'threshold' : '3'}, {'test1' : '2'}]
        }
        '''
        params_dict = {}

        for parameter, values in params.iteritems():
            if parameter in self.exclude_params or values is None:
                continue
            if isinstance(values, list) and all(
                isinstance(item, dict) for item in values):
                for value in values:
                    params_dict.update(value)
            elif isinstance(values, dict):
                raise ValueError(
                    'Cannot include dict type in params \
                    that create query string.')
            else:
                params_dict[parameter] = values

        return params_dict

    def check_command(self, params, command_list):
        if isinstance(params, dict):
            for param, value in params.iteritems():
                if value is None or param in self.exclude_params:
                    continue
                if param in command_list:
                    return True
                if isinstance(value, dict):
                    if self.check_command(value, command_list):
                        return True
                elif isinstance(value, list):
                    for item in value:
                        if self.check_command(item, command_list):
                            return True
        elif isinstance(params, list):
            for item in params:
                if self.check_command(item, command_list):
                    return True
        return False

    def run(self):
        resp = None
        if self.module.params['state'] == "absent":
            data = self.make_data(self.module.params)
            resp = self.prest.delete(self.url, data)
        else:
            data = dict()
            if self.prest.is_exist(self.url, self.module.params['id']):
                data[self.data_name] = self.make_data(self.module.params)
                resp = self.prest.put(self.url, data)
            else:
                data[self.data_name] = self.make_data(self.module.params)
                resp = self.prest.post(self.url, data)
        if resp is not None:
            self.result['message'] = resp.text
        else:
            self.result['message'] = 'Fail'
        self.resp = resp

    def is_ok_error_msg(self, msg):
        if len(self.prest.used_method) < 0:
            return False
        if len(self.ok_error_msg.keys()) <= 0:
            return False

        for method, is_ok_msg in iteritems(self.ok_error_msg):
            if method == self.prest.used_method[-1]:
                for ok_msg in is_ok_msg:
                    if ok_msg in msg:
                        return True
        return False

    def set_result(self):
        if self.resp is None:
            self.result['failed'] = True
            self.result['message'] = 'Prest request is failed'
            self.module.exit_json(**self.result)
            return

        resp_dic = json.loads(self.resp.text)
        if 'header' in resp_dic.keys():
            self.result['message'] = resp_dic['header']['resultMessage']
            if resp_dic['header']['resultCode'] > 0:
                self.result['changed'] = True
            elif resp_dic['header']['resultCode'] < 0:
                if not self.is_ok_error_msg(self.result['message']):
                    self.result['failed'] = True
        else:
            if self.resp.status_code // 100 != 2:
                self.result['failed'] = True
            self.result['message'] = str(resp_dic)
        self.module.exit_json(**self.result)

    def make_real_backup_data(self, data, get_real_data):
        if len(get_real_data) == 0:
            return data
        # real id 값이 key, real의 정보가 value인 dict 생성
        real_dict = {str(real['id']): real for real in get_real_data['real']}
        # backup 값이 있는 경우 해당 id의 항목을 data의 real에 추가
        for real in get_real_data['real']:
            backup_id = real.get('backup')
            if backup_id is not None:
                data.setdefault('real', []).append(real_dict[str(backup_id)])
        return data

    def get_filter_template(self, ip, protocol=None, vport=None):
        filter_template = {
            'type': 'include',
            'sip': '0.0.0.0/0',
            'dip': ip + "/32",
            'protocol': 'all',
            'status': 'enable'
        }

        if protocol is not None:
            filter_template["protocol"] = protocol

        if vport is not None:
            filter_template["dport"] = vport

        return filter_template

    def make_filter_by_vip(self, vips):
        # make filter without id
        filter_list = list()
        for vip in vips:
            ip = vip.get('ip')
            protocols = vip.get('protocol', [])

            # Protocol이 없을 때
            if len(protocols) == 0:
                filter_list.append(self.get_filter_template(ip))

            # Protocol이 있을 때
            for protocol in protocols:
                protocol_name = protocol.get('protocol')
                vports = protocol.get('vport', [])

                # Vport가 없을 때
                if len(vports) == 0:
                    filter_list.append(
                        self.get_filter_template(ip, protocol_name))

                # Vport가 있을 때
                for vport in vports:
                    filter_list.append(
                        self.get_filter_template(ip, protocol_name, vport))
        return filter_list

    def make_filter_data(self, data):
        # module do not have filter data in playbook script
        vip_filter = self.make_filter_by_vip(data['vip'])

        if data.get('filter') is None:
            for _id, vip in enumerate(vip_filter, start=1):
                vip['id'] = str(_id)
            return vip_filter

        # module have filter data in playbook script
        filter_data = list()
        used_filter_id = list()
        for param in data['filter']:
            used_filter_id.append(param['id'])

        f_compare_list = [
            'type', 'dip', 'sip', 'protocol', 'dport'
        ]

        append = False
        for vf in vip_filter:
            for df in data['filter']:
                for p in f_compare_list:
                    if vf.get(p) is None:
                        continue
                    if df.get(p) is None:
                        append = True
                    if vf[p] != df[p]:
                        append = True
            if append:
                for _id in range(1, 255):
                    if str(_id) not in used_filter_id:
                        vf['id'] = str(_id)
                        filter_data.append(vf)
                        used_filter_id.append(str(_id))
                        break

        return filter_data + data['filter']
