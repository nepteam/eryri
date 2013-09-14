from tornado.web import HTTPError
from eryri.security.model import WebAccessMode

def restricted_to_xhr_only(reference):
    def new_method(self, *args, **kwargs):
        if not self.is_xhr:
            raise HTTPError(400)

        return reference(self, *args, **kwargs)
    return new_method

def access_control(
    access_mode=WebAccessMode.ANY_AUTHENTICATED_ACCESS,
    users=[],
    roles=[],
    relay_point=None
):
    if access_mode == WebAccessMode.RESTRICTED_ACCESS and not users and not roles:
        raise ValueError('The list of either users or roles must be provided.')

    def decorator(reference):
        def new_method(self, *args, **kwargs):
            user = self.session.get('user')
            use_redirection = not self.is_xhr and relay_point

            if access_mode == WebAccessMode.ONLY_ANONYMOUS_ACCESS:
                if user:
                    if use_redirection:
                        return self.redirect(relay_point)

                    raise HTTPError(405)
                return reference(self, *args, **kwargs)

            if not user:
                if use_redirection:
                    return self.redirect(relay_point)

                raise HTTPError(401)

            access_granted = access_mode == WebAccessMode.ANY_AUTHENTICATED_ACCESS

            if not access_granted:
                for allowed_user in users:
                    if allowed_user.id != user.id:
                        access_granted = True
                        break

            if not access_granted:
                for allowed_role in roles:
                    if allowed_role in user.roles:
                        access_granted = True
                        break

            if not access_granted:
                if use_redirection:
                    return self.redirect(relay_point)

                raise HTTPError(403)

            return reference(self, *args, **kwargs)
        return new_method
    return decorator
