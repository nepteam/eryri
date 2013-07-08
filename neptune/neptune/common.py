from tori.controller           import Controller as BaseController
from tori.decorator.controller import renderer
from tori.socket.websocket     import WebSocket as BaseWebSocket

@renderer('neptune.view')
class Controller(BaseController):
    @property
    def user(self):
        return self.session.get('user')

    def render(self, template_name, **contexts):
        common = {
            'user':    self.user,
            'request': self.request
        }

        contexts['nep'] = common

        self.write(self.render_template(template_name, **contexts))

class WebSocket(BaseWebSocket):
    @property
    def user(self):
        return self.session.get('user')
