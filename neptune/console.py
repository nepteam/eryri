#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
from tori.application import Application
from tori.centre      import services

# Load common configuration
application = Application('config/app.xml')

if len(sys.argv) == 1:
    print('usage: {} command'.format(sys.argv[0]))
    sys.exit(15)

command_id = sys.argv[1]

print('Console: {}'.format(command_id))

command  = None
commands = services.find_by_tag('command:{}'.format(command_id))

if commands:
    command = commands[0]

if not command:
    raise KeyError('Command not found')

# Reconfigure the parser.
parser         = argparse.ArgumentParser(description='Console')
subparsers     = parser.add_subparsers()
command_parser = subparsers.add_parser(command_id, description=command.__class__.__doc__.strip())

command.define_arguments(command_parser)
command.execute(parser.parse_args())