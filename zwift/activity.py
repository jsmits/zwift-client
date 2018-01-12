# -*- coding: utf-8 -*-
from .request import Request


class Activity:
    def __init__(self, player_id, get_access_token):
        self.player_id = player_id
        self.request = Request(get_access_token)

    def list(self):
        return self.request.json('/api/profiles/{}/activities'.format(self.player_id))

    def get_activity(self, activity_id):
        return self.request.json(
            '/api/profiles/{}/activities/{}'.format(self.player_id, activity_id))

    # TODO: implement FIT file downloading and processing
    # also see: https://github.com/Ogadai/zwift-mobile-api/blob/master/src/Activity.js
    # We can probably use python-fitparse (https://github.com/dtcooper/python-fitparse).
