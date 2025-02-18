#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Piolink Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type
from ansible_collections.piolink.pask.plugins.module_utils.pask_module import PaskModule,\
    make_module_args, try_except


inner_trap_host_args = dict(
    ip=dict(type='str', required=True),
    community=dict(type='str'),
    sha_passwd=dict(type='str', no_log=True),
    sha256_passwd=dict(type='str', no_log=True),
    aes_passwd=dict(type='str', no_log=True),
    engine_id=dict(type='str'),
    version=dict(type='str'),
    user=dict(type='str'),
    agent_addr=dict(type='str'),
    description=dict(type='str')
)

inner_trap_args = dict(
    host=dict(type='list', elements='dict', options=inner_trap_host_args),
    cold_start=dict(type='str'),
    failover=dict(type='str'),
    fan=dict(type='str'),
    dom_all=dict(type='str'),
    dom_temperature=dict(type='str'),
    dom_voltage=dict(type='str'),
    dom_current=dict(type='str'),
    dom_tx_power=dict(type='str'),
    dom_rx_power=dict(type='str'),
    health_check=dict(type='str'),
    link_down=dict(type='str'),
    link_up=dict(type='str'),
    management_cpu=dict(type='str'),
    management_memory=dict(type='str'),
    packet_cpu=dict(type='str'),
    packet_memory=dict(type='str'),
    power=dict(type='str'),
    temperature=dict(type='str'),
    log_storage=dict(type='str')
)

inner_user_args = dict(
    name=dict(type='str', required=True),
    policy=dict(type='str'),
    sha_passwd=dict(type='str', no_log=True),
    sha256_passwd=dict(type='str', no_log=True),
    aes_passwd=dict(type='str', no_log=True)
)

inner_community_args = dict(
    name=dict(type='str', required=True),
    limit_oid=dict(type='list'),
    policy=dict(type='str')
)

inner_system_args = dict(
    name=dict(type='str'),
    contact=dict(type='str'),
    location=dict(type='str')
)

inner_rmon_trap_host_args = dict(
    ip=dict(type='str', required=True),
    community=dict(type='str'),
)

inner_rmon_statistics_args = dict(
    id=dict(type='str', required=True),
    port=dict(type='str'),
    owner=dict(type='str')
)

inner_rmon_history_args = dict(
    id=dict(type='str', required=True),
    buckets=dict(type='str'),
    interval=dict(type='str'),
    port=dict(type='str'),
    owner=dict(type='str')
)

inner_rmon_event_args = dict(
    id=dict(type='str', required=True),
    type=dict(type='str'),
    owner=dict(type='str'),
    description=dict(type='str')
)

inner_rmon_alarm_rising_args = dict(
    threshold=dict(type='str', required=True),
    event=dict(type='str')
)

inner_rmon_alarm_falling_args = dict(
    threshold=dict(type='str', required=True),
    event=dict(type='str')
)

inner_rmon_alarm_args = dict(
    id=dict(type='str', required=True),
    rising=dict(type='dict', options=inner_rmon_alarm_rising_args),
    falling=dict(type='dict', options=inner_rmon_alarm_falling_args),
    interval=dict(type='str'),
    startup_alarm=dict(type='str'),
    sample_type=dict(type='str'),
    owner=dict(type='str'),
    variable_oid=dict(type='str')
)

inner_rmon_args = dict(
    trap_host=dict(type='list', elements='dict',
                   options=inner_rmon_trap_host_args),
    statistics=dict(type='list', elements='dict',
                    options=inner_rmon_statistics_args),
    history=dict(type='list', elements='dict',
                 options=inner_rmon_history_args),
    event=dict(type='list', elements='dict', options=inner_rmon_event_args),
    alarm=dict(type='list', elements='dict', options=inner_rmon_alarm_args),
)

module_args = dict(
    trap=dict(type='dict', options=inner_trap_args),
    community=dict(type='list', elements='dict',
                   options=inner_community_args),
    user=dict(type='list', elements='dict', options=inner_user_args),
    system=dict(type='dict', options=inner_system_args),
    rmon=dict(type='dict', options=inner_rmon_args),
    status=dict(type='str'),
    load_timeout=dict(type='str')
)

name = 'snmp'


class PaskSnmp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSnmp, self).__init__(name, module_args)
        self.exclude_underscore_params.add('log_storage')

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.prest.put(self.url, data)


def main():
    snmp = PaskSnmp(name, module_args)
    snmp.set_param()
    snmp.run()
    snmp.set_result()


if __name__ == '__main__':
    main()
