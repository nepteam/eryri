# -*- coding: utf-8 -*-
import threading
from tori.application import Application
from tori.centre      import services

application = Application('config/app.xml')

application.start()

thread_feedback = '\r{}\tForce stop "{}"'
for thread in threading.enumerate():
    if thread.isAlive():
        thread_name = str(thread.getName())

        if thread_name == 'MainThread':
            continue

        try:
            thread._Thread__stop()
            print(thread_feedback.format('Okay', thread_name))
        except:
            print(thread_feedback.format('Failed', thread_name))