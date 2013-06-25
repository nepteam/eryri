#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import re
import sys
from tori.application import Application
from tori.centre      import services

# Load common configuration
application = Application('config/app.xml')

if len(sys.argv) == 1:
    print('USAGE: {} command'.format(sys.argv[0]))
    print('\nAvailable commands:')

    # This is a hack to get the list of IDs from Imagination Framework.
    command_ids = [entity_id for entity_id in services._tag_to_entity_ids['command']]
    command_desc_map = {}
    longest_cmd_length = 0

    for command_id in command_ids:
        # This is also a hack to get the entity (metadata) of the commands.
        entity = services._entities[command_id]
        alias  = re.sub('^[^\.]+\.', '', command_id)
        
        if longest_cmd_length < len(alias):
            longest_cmd_length = len(alias)

        command_desc_map[alias] = entity._loader.package.__doc__.strip()
    
    format_string = '  {:<%d}{}' % (longest_cmd_length + 4)
    
    for id in command_desc_map:
        print(format_string.format(id, command_desc_map[id]))

    sys.exit(15)

command_id = sys.argv[1]

print('Console: {}'.format(command_id))

command  = None
commands = services.find_by_tag('command:{}'.format(command_id))

if commands:
    command = commands[0]

if not command:
    raise RuntimeError('Command not found')

# Reconfigure the parser.
parser         = argparse.ArgumentParser(description='Console')
subparsers     = parser.add_subparsers()
command_parser = subparsers.add_parser(command_id, description=command.__class__.__doc__.strip())

command.define_arguments(command_parser)
command.execute(parser.parse_args())