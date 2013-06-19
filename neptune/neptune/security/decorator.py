from tornado.web import HTTPError

def allow_access(users=[], roles=[]):
    if not users and not roles:
        raise ValueError('The list of either users or roles must be provided.')

    def decorator(reference):
        def new_reference(self, *args, **kwargs):
            user = self.session.get('user')

            if not user:
                raise HTTPError(401)
            
            access_granted = False
            
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
                raise HTTPError(403)

            return reference(self, *args, **kwargs)
        return new_reference
    return decorator
