# -*- coding: utf-8 -*-
from tori.controller           import Controller
from tori.decorator.controller import renderer
from neptune.security.model     import Credential, WebAccessMode, User
from neptune.security.decorator import access_control, restricted_to_xhr_only

@renderer('neptune.view')
class Home(Controller):
    @access_control(WebAccessMode.ONLY_ANONYMOUS_ACCESS, relay_point='/home')
    def get(self):
        self.render('index.html')

@renderer('neptune.view')
class Dashboard(Controller):
    @access_control(WebAccessMode.ANY_AUTHENTICATED_ACCESS, relay_point='/')
    def get(self):
        self.render('index.html')
