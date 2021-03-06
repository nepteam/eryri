# -*- coding: utf-8 -*-
from tori.decorator.controller import renderer
from eryri.common             import Controller
from eryri.security.model     import Credential, WebAccessMode, User
from eryri.security.decorator import access_control, restricted_to_xhr_only

class Home(Controller):
    @access_control(WebAccessMode.ONLY_ANONYMOUS_ACCESS, relay_point='/dashboard')
    def get(self):
        #self.render('index.html')
        self.redirect('/login')

class Dashboard(Controller):
    @access_control(WebAccessMode.ANY_AUTHENTICATED_ACCESS, relay_point='/')
    def get(self):
        #self.render('dashboard.html')
        self.redirect('/beacon')
