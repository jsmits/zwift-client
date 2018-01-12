# -*- coding: utf-8 -*-
from .request import Request


class Profile:
    def __init__(self, player_id, get_access_token):
        self.player_id = player_id
        self.request = Request(get_access_token)

    def profile(self):
        return self.request.json('/api/profiles/{}'.format(self.player_id))
