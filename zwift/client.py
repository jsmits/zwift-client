# -*- coding: utf-8 -*-
from .activity import Activity
from .auth import AuthToken
from .profile import Profile
from .world import World


class Client:
    def __init__(self, username, password):
        self.auth_token = AuthToken(username, password)

    def get_activity(self, player_id):
        return Activity(player_id, self.auth_token.get_access_token)

    def get_profile(self, player_id='me'):
        return Profile(player_id, self.auth_token.get_access_token)

    def get_world(self, world_id=1):
        return World(world_id, self.auth_token.get_access_token)
