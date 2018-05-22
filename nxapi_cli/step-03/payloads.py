#!/usr/bin/env python
"""
Given a set of CLI commands, generate a payload based on the message and command types.

Current supported message types are:  json-rpc (2.0)
Current supported command types are: 
    (json-rpc) cli/cli_ascii and 

"""

# http://python-future.org/quickstart.html
from __future__ import absolute_import, division, print_function

import copy

# Declare list of supported messaging types and command types
supported_messages = ( 'json-rpc' )
supported_command_types = { 
    'json-rpc': [ 'cli', 'cli_ascii' ],
    }

supported_headers = {
    'post' : {
        'json-rpc': { 'content-type': 'application/json-rpc' },
    },
}

class invalidType(Exception):
    """
    Generic exception to throw when an invalid message or command type is used.
    """
    pass


class json_rpc:
    """
    Class for the JSON-RPC 2.0 standard for Remote Procedure Calls that
    are encoded within JSON formatting.

    JSON-RPC Standard - http://www.jsonrpc.org/specification
    Server implementation - https://github.com/pavlov99/json-rpc

    """

    def __init__(self, method=None, cmd=None):
        self._messages = 'json-rpc'
        self._version = '2.0'
        self._method = None
        self._commands = []

        self._set_method(method=method)
        self.add_command(command=cmd)

    def _set_method(self, method=None):
        if method not in supported_command_types[self._messages]:
            raise invalidType(
                "Unsupported command type {0} for {1}".format(method, self._messages)
                )
        self._method = method

    def add_command(self, command=None):
        if not command:
            return
        self._commands.append(command)

    def _get_template(self):
        """
        Template generator
        """

        return {
            'jsonrpc' : '2.0',
            'method'  : self._method,
            'params'  : {
                'cmd'     : None,
                'version' : 1,
            },
            'id'      : None,
        }

    def post_input(self):
        template = self._get_template()
        id = 0
        commands = []

        for cmd in self._commands:
            id = id + 1

            template['params']['cmd'] = cmd
            template['id'] = id

            commands.append(copy.deepcopy(template))

        return commands

    def post_header(self):
        return supported_headers['post']['json-rpc']
    

