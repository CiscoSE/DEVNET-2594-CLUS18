#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

# http://python-future.org/quickstart.html
from __future__ import absolute_import, division, print_function

__author__ = "Timothy E Miller, PhD <timmil@cisco.com>"
__contributors__ = [
]
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

import argparse
import requests
import json
import copy
import time
import os

import isodate
import prometheus_client

import connection

# How often to poll switch in seconds (should match collection frequency)
sleep_interval = 15

# Track whether we want output
verbose = False

###
# IP Route Metrics
###

ip_prefix_path_count = prometheus_client.Gauge(
                        'ip_prefix_path_count',
                        'Track number of ECMP entries for given prefix',
                        ('vrf', 'prefix')
                        )

ip_prefix_path_uptime = prometheus_client.Gauge(
                        'ip_prefix_path_uptime',
                        'Track uptime in seconds for nexthop of given prefix',
                        ('vrf', 'prefix', 'nexthop')
                        )

ip_prefix_path_traffic = prometheus_client.Gauge(
                        'ip_prefix_path_traffic',
                        'Report on traffic sent over each path',
                        ('interface', 'family')
                        )

def collect_ip_routes(switch, vrf='default'):
    payload = switch.payload()
    payload.add_command('show ip route vrf {0}'.format(vrf))
    response = switch.post(payload)

    if response['result'] is 'null':
        raise Exception('VRF {0} not configured on switch'.format(vrf))

    if response['result'] is None:
        raise Exception('No results returned')

    vrf_data = response['result']['body']['TABLE_vrf']['ROW_vrf']
    if vrf_data['vrf-name-out'] != vrf:
        raise Exception('VRF requested not in output')

    if vrf_data['TABLE_addrf']['ROW_addrf']['addrf'] != 'ipv4':
        raise Exception('Was expecting IPv4 but failed')

    route_data = vrf_data['TABLE_addrf']['ROW_addrf']['TABLE_prefix']['ROW_prefix']

    if isinstance(route_data, dict):
        route_data = [ route_data ]

    # Track interfaces that have been published
    interfaces = []

    for block in route_data:
        prefix = block['ipprefix']

        # This example isn't interested in connected routes
        if block['attached'] == 'true':
            continue

        paths = block['ucast-nhops']
        ip_prefix_path_count.labels(vrf=vrf, prefix=prefix).set(paths)

        if verbose:
            print(vrf, prefix, paths)

        # Trick to account for snowflake behavior
        if isinstance(block['TABLE_path']['ROW_path'], list):
            block_data = block['TABLE_path']['ROW_path']
        else:
            block_data = [ block['TABLE_path']['ROW_path'] ]

        for path in block_data:
            # Account for I6 bug
            if 'ipnexthop' not in path:
                continue

            nexthop = path['ipnexthop']
            uptime = int(isodate.parse_duration(path['uptime']).total_seconds())

            ip_prefix_path_uptime.labels(vrf=vrf,
                                         prefix=prefix,
                                         nexthop=nexthop).set(uptime)
        
            ifname = path['ifname']

            if ifname not in interfaces:
                interfaces.append(ifname)
                
                intf_payload = switch.payload()
                intf_payload.add_command('show ip interface {0}'.format(ifname))
                intf_response = switch.post(intf_payload)

                if intf_response['result'] in [ 'null', None ]:
                    raise Exception('Interface {0} show failure'.format(ifname))
                
                intf_data = intf_response['result']['body']['TABLE_intf']['ROW_intf']

                ip_prefix_path_traffic.labels(interface=ifname,
                                              family='unicast').set(intf_data['ubyte-sent'])

                ip_prefix_path_traffic.labels(interface=ifname,
                                              family='multicast').set(intf_data['mbyte-sent'])

                ip_prefix_path_traffic.labels(interface=ifname,
                                              family='labeled').set(intf_data['lbyte-sent'])

                if verbose:
                    print(ifname, intf_data['ubyte-sent'], 
                          intf_data['mbyte-sent'], intf_data['lbyte-sent'])
                
            if verbose:
                print(vrf, prefix, nexthop, uptime)

if __name__ == '__main__':
    # Command line arguments to flag Docker environment
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--container', 
                        help='Flag container operation', 
                        action='store_true',
                        )

    parser.add_argument('-t', '--target', 
                        help='Provide remote hostname/IP for NXAPI',
                        )

    parser.add_argument('-p', '--port', 
                        help='Provide remote port for NXAPI',
                        )

    parser.add_argument('-u', '--user', 
                        help='Provide remote username for NXAPI',
                        )

    parser.add_argument('-w', '--password', 
                        help='Provide remote password for NXAPI',
                        )

    parser.add_argument('-v', '--verbose',
                        help='Enable verbose output',
                        action='store_true'
                        )

    args = parser.parse_args()

    host = 'localhost'
    port = '23456'

    # Enable output - can be overriden by Docker flag
    if args.verbose:
        verbose = True

    # Credentials
    if args.user:
        user = args.user
    else:
        user = 'admin'

    if args.password:
        password = args.password
    else:
        password = 'admin'

    # Running against a remote NX-OS system (not local VM)
    if args.target:
        host = args.target

    # Change from the (project historical) default port
    if args.port:
        port = str(args.port)

    # Running in a Docker container
    if args.container:
        host     = os.getenv('NXAPI_HOST', 'host.docker.internal')
        port     = os.getenv('NXAPI_PORT', port)
        user     = os.getenv('NXAPI_USER', 'admin')
        password = os.getenv('NXAPI_PASS', 'admin')
        verbose = False

    # Create a connection object
    switch = connection.nxapi(
                protocol='http',
                host=host, port=port,
                user=user, password=password,
                message_format='json-rpc',
                command_type='cli'
                )

    # Start the Prometheus client library web service
    if not verbose:
        prometheus_client.start_http_server(8888)

    while True:

        # Collect data on IP routes
        collect_ip_routes(switch)

        # Sleep until next collection
        time.sleep(sleep_interval)
