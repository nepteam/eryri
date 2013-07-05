# -*- coding: utf-8 -*-
import threading
from tori.application import Application
from tori.centre      import services

application = Application('config/app.xml')

application.start()
