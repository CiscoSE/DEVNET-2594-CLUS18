#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2018 Cisco and/or its affiliates.

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
# iCAM L2_table resource usage
###

l2_table_current = prometheus_client.Gauge('icam_l2_table_used',
                                           'Amount of space used in L2 Tables',
                                           None)
l2_table_max     = prometheus_client.Gauge('icam_l2_table_max',
                                           'Amount of space available in L2 Tables',
                                           None)
l2_table_time    = prometheus_client.Counter('icam_l2_table_time_seconds',
                                             'Timestamp of the current measurement',
                                             None)

def collect_l2_table(switch, time_delta = sleep_interval):

    payload = switch.payload()
    payload.add_command('show icam resource l2_table module 1 inst 0')
    response = switch.post(payload)
        
    table_data = response['result']['body']['TABLE_l2_table_resource']['ROW_l2_table_resource']

    # Update Prometheus objects
    l2_table_time.inc(time_delta)
    l2_table_current.set(int(table_data['Used_Entries']))
    l2_table_max.set(int(table_data['Total_Entries']))

    if verbose:
        print(int(time.time()))
        print(int(table_data['Used_Entries']))
        print(int(table_data['Total_Entries']))

###
# iCAM FIB TCAM usage
###

fib_tcam_ipv4_hosts  = prometheus_client.Gauge(
                        'icam_fib_tcam_ipv4_hosts_used',
                        'Used TCAM entries for IPv4 FIB',
                        None
                        )

fib_tcam_ipv4_routes = prometheus_client.Gauge(
                        'icam_fib_tcam_ipv4_routes_used',
                        'Used TCAM entries for IPv4 routes',
                        None
                        )

fib_tcam_ipv4_lpm    = prometheus_client.Gauge(
                        'icam_fib_tcam_ipv4_lpm_routes_used',
                        'Used TCAM entries for IPv4 LPM routes',
                        None
                        )

def collect_fib_tcam(switch, time_delta=sleep_interval):
    payload = switch.payload()
    payload.add_command('show icam resource fib_tcam module 1 inst 0')
    response = switch.post(payload)

    table_data = response['result']['body']['TABLE_fib_resource']['ROW_fib_resource']

    fib_tcam_ipv4_hosts.set(
        table_data[0]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries']
        )

    fib_tcam_ipv4_routes.set(
        table_data[1]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries']
        )
        
    fib_tcam_ipv4_lpm.set(
        table_data[2]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries']
        )
        
    if verbose:
        print(table_data[0]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries'])
        print(table_data[1]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries'])
        print(table_data[2]['TABLE_fib_stats']['ROW_fib_stats']['Used_Entries'])

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
    prometheus_client.start_http_server(8888)

    # Prime the time counter
    l2_table_time.inc(int(time.time()))

    while True:

        # Collect the MAC table usage info
        collect_l2_table(switch, sleep_interval)

        # Collect the FIB TCAM usage info
        collect_fib_tcam(switch, sleep_interval)

        # Sleep until next collection
        time.sleep(sleep_interval)
