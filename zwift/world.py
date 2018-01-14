# -*- coding: utf-8 -*-
from . import zwift_messages_pb2
from .request import Request

COURSE_TO_WORLD = {3: 1, 4: 2, 5: 3, 6: 1}


class COURSES:
    WATOPIA = 3
    RICHMOND = 4
    LONDON = 5


class World:
    def __init__(self, world_id, get_access_token):
        self.world_id = world_id
        self.request = Request(get_access_token)

    @property
    def players(self):
        return self.request.json('/relay/worlds/{}'.format(self.world_id))

    def player_status(self, player_id):
        buffer = self.request.protobuf(
            '/relay/worlds/{}/players/{}'.format(self.world_id, player_id))
        player_state = zwift_messages_pb2.PlayerState()
        player_state.ParseFromString(buffer)
        return PlayerStateWrapper(player_state)


class PlayerStateWrapper(object):
    """
    Wrap a PlayerState instance to make it more usable.

    Fields provided by wrapped player_state:
    id, worldTime, distance, roadTime, laps, speed, roadPosition, cadenceUHz,
    heartrate, power, heading, lean, climbing, time, f19, f20, progress,
    customisationId, justWatching, calories, x, altitude, y, watchingRiderId,
    groupId, sport

    """
    class TURN_SIGNALS:
        RIGHT = 'right'
        LEFT = 'left'
        STRAIGHT = 'straight'

    def __init__(self, player_state):
        self.player_state = player_state

    @property
    def ride_ons(self):
        return (self.player_state.f19 >> 24) & 0xfff

    @property
    def is_turning(self):
        return (self.player_state.f19 & 8) != 0

    @property
    def is_forward(self):
        return (self.player_state.f19 & 4) != 0

    @property
    def course(self):
        return (self.player_state.f19 & 0xff0000) >> 16

    @property
    def world(self):
        return COURSE_TO_WORLD[self.course]

    @property
    def road_id(self):
        return (self.player_state.f20 & 0xff00) >> 8

    @property
    def road_direction(self):
        return (self.player_state.f20 & 0xffff000000) >> 24

    @property
    def turn_signal(self):
        signal_code = self.player_state.f20 & 0x70
        if signal_code == 0x10:
            return self.TURN_SIGNALS.RIGHT
        elif signal_code == 0x20:
            return self.TURN_SIGNALS.LEFT
        elif signal_code == 0x40:
            return self.TURN_SIGNALS.STRAIGHT
        else:
            return None

    @property
    def power_up(self):
        return self.player_state.f20 & 0xf

    @property
    def has_feather_boost(self):
        return self.power_up == 0

    @property
    def has_draft_boost(self):
        return self.power_up == 1

    @property
    def has_aero_boost(self):
        return self.power_up == 5

    @property
    def cadence(self):
        return int((self.player_state.cadenceUHz * 60) / 1000000)

    def __getattr__(self, item):
        """
        First try to get the requested item from the player_state. When it's
        not found, try to get it directly from the wrapper.
        """
        try:
            return getattr(self.player_state, item)
        except AttributeError:
            return self.__getattribute__(item)
