from tori.controller           import Controller as BaseController
from tori.decorator.controller import renderer

@renderer('neptune.view')
class Controller(BaseController):
    def render(self, template_name, **contexts):
        common = {
            'user': self.session.get('user')
        }

        contexts['nep'] = common

        self.write(self.render_template(template_name, **contexts))
