import time
from tori.db.entity import entity
from tori.db.mapper import AssociationType, link

class Message(object):
    def __init__(self, sender, owner, recipients, body, kind, created=None, is_read=False):
        self.sender = sender
        self.owner = owner
        self.kind = kind
        self.body = body
        self.recipients = recipients
        self.created = created or time.time()
        self.is_read = is_read

@link(
    mapped_by='sender',
    target='neptune.security.model.Credential',
    association=AssociationType.MANY_TO_ONE,
    read_only=True
)
@link(
    mapped_by='owner',
    target='neptune.security.model.Credential',
    association=AssociationType.MANY_TO_ONE,
    read_only=True
)
@entity('beacon_message')
class BeaconMessage(Message):
    def __init__(self, sender, owner, body, kind, created=None, is_read=False):
        super(BeaconMessage, self).__init__(sender, owner, '', body, kind, created, is_read)