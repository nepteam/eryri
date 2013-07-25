# -*- coding: utf-8 -*-
import threading
from imagination.loader import Loader
from tori.application import Application
from tori.centre      import settings, services

def load_default_config():
    """ Prototype code for loading the default configuration from the module.
    """
    global settings

    settings['modules'] = [
        'neptune.security',
        'neptune.management',
        'neptune.beacon'
    ]

    settings['roles'] = {}

    for module_path in settings['modules']:
        config = Loader(module_path).package
        settings['roles'].update(config.roles)

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