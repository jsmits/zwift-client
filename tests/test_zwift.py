# -*- coding: utf-8 -*-
import unittest

from zwift import Client
from zwift.activity import Activity
from zwift.profile import Profile
from zwift.world import World


class TestZwift(unittest.TestCase):

    def setUp(self):
        username = 'Debbie'
        password = 'Harry'
        self.player_id = 123456
        self.client = Client(username, password)

    def test_activity(self):
        activity = self.client.get_activity(self.player_id)
        assert isinstance(activity, Activity)
        assert activity.player_id == self.player_id

    def test_profile(self):
        profile = self.client.get_profile(self.player_id)
        assert isinstance(profile, Profile)
        assert profile.player_id == self.player_id

    def test_profile_me(self):
        profile = self.client.get_profile()
        assert isinstance(profile, Profile)
        assert profile.player_id == 'me'

    def test_world(self):
        world = self.client.get_world()
        assert isinstance(world, World)
        assert world.world_id == 1  # default world id
