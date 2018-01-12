# -*- coding: utf-8 -*-
from .request import Request


class World:
    def __init__(self, world_id, get_access_token):
        self.world_id = world_id
        self.request = Request(get_access_token)

    def players(self):
        return self.request.json('/relay/worlds/{}'.format(self.world_id))

    def player_status(self, player_id):
        # do the protobuf request and parse the player status messages
        # TODO: implement
        pass
