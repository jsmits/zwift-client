# -*- coding: utf-8 -*-
import time

from .request import Request


class Event:
    def __init__(self, get_access_token):
        self.request = Request(get_access_token)

    def search(self):
        now = int(time.time() * 1000)
        eventStartsAfter = now - 3600000
        eventStartsBefore = now + 600000
        limit = 100
        return self.request.post(
            # '/api/events/search?use_subgroup_time=true&created_before={}&start=0&limit={}'.format(eventStartsAfter, limit),
            '/api/events/search?start=0&limit=100',
            data={
                'eventStartsAfter': eventStartsAfter,
                'eventStartsBefore': eventStartsBefore
            }
        )

    def list(self):
        return self.request.json('/api/events')
