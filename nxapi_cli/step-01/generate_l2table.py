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

import requests
import json
import copy
import time

# NX-OS URL and credentials
url='http://127.0.0.1:23456/ins'
switchuser='admin'
switchpassword='admin'

# HTTP Post headers
myheaders={ 'content-type': 'application/json-rpc' }

# Template for the paylod
payload_template = {
    'jsonrpc': '2.0',
    'method': 'cli',
    'params': {
        'cmd': None,
        'version': 1,
    },
    'id': None,
}  

# How often to poll switch in seconds (should match collection frequency)
sleep_interval = 15

def collect_l2_table():
    command = copy.deepcopy(payload_template)
    command['params']['cmd'] = 'show icam resource l2_table module 1 inst 0'
    command['id'] = 1
    payload = [ command ]

    # Post our set of commands (one) to the NXAPI web server
    response_raw = requests.post(url,
                                 data=json.dumps(payload), 
                                 headers=myheaders,
                                 auth=(switchuser,switchpassword)
                                 )

    # Convert response to manageable JSON
    response = response_raw.json()

    # Point down to the correct spot for our answer
    table_data = response['result']['body']['TABLE_l2_table_resource']['ROW_l2_table_resource']

    # Print the "in-use" and "total" entries in the L2 table
    print(int(table_data['Used_Entries']))
    print(int(table_data['Total_Entries']))


if __name__ == '__main__':

    # Print the time counter
    print(int(time.time()))

    while True:
        collect_l2_table()

        time.sleep(sleep_interval)
        print(int(time.time()))
