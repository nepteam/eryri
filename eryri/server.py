# -*- coding: utf-8 -*-
from logging import ERROR, WARNING, DEBUG, INFO
import threading
from sys import argv

from imagination.loader import Loader
from tori.application import Application
from tori.centre      import settings, services
from tori.common      import LoggerFactory

def load_default_config():
    """ Prototype code for loading the default configuration from the module.
    """
    global settings

    settings['modules'] = [
        'eryri.security',
        'eryri.management',
        'eryri.beacon'
    ]

    settings['roles'] = {}

    for module_path in settings['modules']:
        config = Loader(module_path).package
        settings['roles'].update(config.roles)

LoggerFactory.instance().set_default_level(INFO if '--dev' in argv else ERROR)

# Setup
application = Application('config/app.xml')
load_default_config()

# Initiate the service
application.start()

# Kill all running threads.
for thread in threading.enumerate():
    if not thread.isAlive():
        continue

    thread_name = str(thread.getName())

    if thread_name == 'MainThread': continue

    try:    thread._Thread__stop()
    except: pass