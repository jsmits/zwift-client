# -*- coding: utf-8 -*-
from .request import Request


class Profile:
    def __init__(self, player_id, get_access_token):
        self.player_id = player_id
        self.request = Request(get_access_token)

    @property
    def profile(self):
        return self.request.json('/api/profiles/{}'.format(self.player_id))

    def check_player_id(self):
        """Most /api/profiles endpoints require the real player id."""
        if self.player_id == 'me':
            profile = self.profile
            self.player_id = profile['id']

    @property
    def followers(self):
        self.check_player_id()
        return self.request.json(
            '/api/profiles/{}/followers'.format(self.player_id))

    @property
    def followees(self):
        self.check_player_id()
        return self.request.json(
            '/api/profiles/{}/followees'.format(self.player_id))

    def get_activities(self, start=0, limit=10):
        self.check_player_id()
        return self.request.json(
            '/api/profiles/{}/activities?start={}&limit={}'.format(
                self.player_id, start, limit))

    @property
    def latest_activity(self):
        activities = self.get_activities(0, 1)
        return activities[0] if len(activities) == 1 else None
