# -*- coding: utf-8 -*-
from __future__ import print_function

import time

import requests


class AuthToken:
    def __init__(self, username, password):
        self.username = username
        self.password = password

        # variables from the API response
        self.access_token = None
        self.expires_in = None
        self.id_token = None
        self.not_before_policy = None
        self.refresh_token = None
        self.refresh_expires_in = None
        self.session_state = None
        self.token_type = None
        # absolute expire times of the access and refresh tokens
        self.access_token_expiration = None
        self.refresh_token_expiration = None

    def fetch_token_data(self):
        if self.have_valid_refresh_token():
            data = {
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
            }
        else:
            data = {
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
            }
        data['client_id'] = "Zwift_Mobile_Link"
        r = requests.post(
            'https://secure.zwift.com/auth/realms/zwift/tokens/access/codes',
            data=data)
        if not r.ok:
            # TODO: handle exceptions
            pass
        return r.json()

    def update_token_data(self):
        """Parse the access token response."""
        token_data = self.fetch_token_data()
        now = time.time()
        for key, value in token_data.items():
            key = key.replace('-', '_')
            setattr(self, key, value)
        self.access_token_expiration = now + self.expires_in - 5
        self.refresh_token_expiration = now + self.refresh_expires_in - 5

    def have_valid_access_token(self):
        if not self.access_token or time.time() > self.access_token_expiration:
            return False
        else:
            return True

    def have_valid_refresh_token(self):
        if (not self.refresh_token or
                time.time() > self.refresh_token_expiration):
            return False
        else:
            return True

    def get_access_token(self):
        if self.have_valid_access_token():
            return self.access_token
        else:
            self.update_token_data()
            return self.access_token
