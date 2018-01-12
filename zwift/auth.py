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
        self.refresh_token =None
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
        """Parse the access token response.

        example token response:
        {u'access_token': u'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI3MmM3MGMzYi01ZDJmLTQ3YTktOTkzZS1hMWM3MDYyZDJhZDMiLCJleHAiOjE1MTU3NzA1MjMsIm5iZiI6MCwiaWF0IjoxNTE1NzU5NzIzLCJpc3MiOiJodHRwczovL3NlY3VyZS56d2lmdC5jb20vYXV0aC9yZWFsbXMvendpZnQiLCJhdWQiOiJad2lmdF9Nb2JpbGVfTGluayIsInN1YiI6IjhjNGM0NGI0LWI1MDYtNDk1YS1hZjY1LTgwOTEwYzlkMTUxYiIsImF6cCI6Ilp3aWZ0X01vYmlsZV9MaW5rIiwic2Vzc2lvbl9zdGF0ZSI6Ijg1Yzc2ZmVmLTdkZmQtNDI3OC04ODU5LTI2NDUyNWUzZGZhYiIsImNsaWVudF9zZXNzaW9uIjoiOWFjMDAwNTMtMjUwZS00NDMzLWI1NWMtOWZhZjYyZmVjMzM3IiwiYWxsb3dlZC1vcmlnaW5zIjpbXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImV2ZXJ5Ym9keSIsInRyaWFsLXN1YnNjcmliZXIiLCJiZXRhLXRlc3RlciJdfSwicmVzb3VyY2VfYWNjZXNzIjp7Im15LXp3aWZ0Ijp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiWndpZnQgUkVTVCBBUEkgLS0gcHJvZHVjdGlvbiI6eyJyb2xlcyI6WyJhdXRob3JpemVkLXBsYXllciIsImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiWndpZnQgSlNGIC0tIHByb2R1Y3Rpb24iOnsicm9sZXMiOlsiYXV0aG9yaXplZC1wbGF5ZXIiXX0sIlp3aWZ0IFplbmRlc2siOnsicm9sZXMiOlsiYXV0aGVudGljYXRlZC11c2VyIl19LCJEYXNoYm9hcmQiOnsicm9sZXMiOlsiYXV0aGVudGljYXRlZC11c2VyIl19LCJad2lmdCBSZWxheSBSRVNUIEFQSSAtLSBwcm9kdWN0aW9uIjp7InJvbGVzIjpbImF1dGhvcml6ZWQtcGxheWVyIl19LCJlY29tLXNlcnZlciI6eyJyb2xlcyI6WyJhdXRoZW50aWNhdGVkLXVzZXIiXX0sImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJ2aWV3LXByb2ZpbGUiXX19LCJuYW1lIjoiU2FuZGVyIFNtaXRzIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiamhtc21pdHNAZ21haWwuY29tIiwiZ2l2ZW5fbmFtZSI6IlNhbmRlciIsImZhbWlseV9uYW1lIjoiU21pdHMiLCJlbWFpbCI6ImpobXNtaXRzQGdtYWlsLmNvbSJ9.Jy2t1WGH6Npr4imU8HqImJD-CwS89pBEIiGX5JoA50mKXzTN9w1MePbDChP53Q5eoA-nxFPuFU6-7Q10IbNoeo_-siWelPBD0bqbn7ZdvnH_PAWZ1QNhOEj35aUkR7muc2RwMnI3zC2CaK-VlkAxLCWtDkNCVZ7Q4W6hJ2Ib16mQMMv9cNr0b8YFJ-sj92PJf3ZHV-z7ART4dGB0Y-RiVfbjYxvS2K6OkwHFehzR2UVc1CqEKmSKnSEN5IKnbBhbdM9U_0dAXc3RLYOCZlHbsiQCAbiMAZmw6hRSd-DVVLkfiV9unGIE3myFu2H5bOJC33G4Ahnd_LfHtg50ocRfVA',
         u'expires_in': 10800,
         u'id_token': u'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiIzMDE1NDA4Ni04ZGM1LTQ5YzItYTA4ZC0xMjA1N2Y0NDMxMmYiLCJleHAiOjE1MTU3NzA1MjMsIm5iZiI6MCwiaWF0IjoxNTE1NzU5NzIzLCJpc3MiOiJodHRwczovL3NlY3VyZS56d2lmdC5jb20vYXV0aC9yZWFsbXMvendpZnQiLCJhdWQiOiJad2lmdF9Nb2JpbGVfTGluayIsInN1YiI6IjhjNGM0NGI0LWI1MDYtNDk1YS1hZjY1LTgwOTEwYzlkMTUxYiIsImF6cCI6Ilp3aWZ0X01vYmlsZV9MaW5rIiwic2Vzc2lvbl9zdGF0ZSI6Ijg1Yzc2ZmVmLTdkZmQtNDI3OC04ODU5LTI2NDUyNWUzZGZhYiIsIm5hbWUiOiJTYW5kZXIgU21pdHMiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJqaG1zbWl0c0BnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiU2FuZGVyIiwiZmFtaWx5X25hbWUiOiJTbWl0cyIsImVtYWlsIjoiamhtc21pdHNAZ21haWwuY29tIn0.eMKPY67nrc-4BEZSX1O8N7HxGQCqP3eBr5XfdvOeNQu8y6lXYl-fxV3Zg7RoiZV3QPcM0uqHwbh1pHF9kXgLV8D7gzA8_uNkO2Daci1ambrbxUqUApGX7ggN2MnehUDYqtKJmvYN4Hc3yQYN0rpF3qMDuo5cp0Q9H2QqS5bdBG4L557jesAlEX-c5jV8LxwcqrqdG7TakSXUoKe_EWVkasEV6Aw8ZgpgWhsvZ24aDXMkLkBFxVWShDsd7pCBxmQ2GWhQPnF1hLOGY7TYKuU4SOxr8SL0em-7rQcOozJVjz4j8UbdDz6WCpBsoi_3j2Ivhx1_rPFxuwrfHC8TaADO9A',
         u'not-before-policy': 1408478984,
         u'refresh_expires_in': 2592000,
         u'refresh_token': u'eyJhbGciOiJSUzI1NiJ9.eyJqdGkiOiI0YzRmMjU2OC00ODRiLTQ1MzEtOTc4NC1jZjY0MTgyNzY5YTQiLCJleHAiOjE1MTgzNTE3MjMsIm5iZiI6MCwiaWF0IjoxNTE1NzU5NzIzLCJpc3MiOiJodHRwczovL3NlY3VyZS56d2lmdC5jb20vYXV0aC9yZWFsbXMvendpZnQiLCJzdWIiOiI4YzRjNDRiNC1iNTA2LTQ5NWEtYWY2NS04MDkxMGM5ZDE1MWIiLCJ0eXAiOiJSRUZSRVNIIiwiYXpwIjoiWndpZnRfTW9iaWxlX0xpbmsiLCJzZXNzaW9uX3N0YXRlIjoiODVjNzZmZWYtN2RmZC00Mjc4LTg4NTktMjY0NTI1ZTNkZmFiIiwiY2xpZW50X3Nlc3Npb24iOiI5YWMwMDA1My0yNTBlLTQ0MzMtYjU1Yy05ZmFmNjJmZWMzMzciLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZXZlcnlib2R5IiwidHJpYWwtc3Vic2NyaWJlciIsImJldGEtdGVzdGVyIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsibXktendpZnQiOnsicm9sZXMiOlsiYXV0aGVudGljYXRlZC11c2VyIl19LCJad2lmdCBSRVNUIEFQSSAtLSBwcm9kdWN0aW9uIjp7InJvbGVzIjpbImF1dGhvcml6ZWQtcGxheWVyIiwiYXV0aGVudGljYXRlZC11c2VyIl19LCJad2lmdCBKU0YgLS0gcHJvZHVjdGlvbiI6eyJyb2xlcyI6WyJhdXRob3JpemVkLXBsYXllciJdfSwiWndpZnQgWmVuZGVzayI6eyJyb2xlcyI6WyJhdXRoZW50aWNhdGVkLXVzZXIiXX0sIkRhc2hib2FyZCI6eyJyb2xlcyI6WyJhdXRoZW50aWNhdGVkLXVzZXIiXX0sIlp3aWZ0IFJlbGF5IFJFU1QgQVBJIC0tIHByb2R1Y3Rpb24iOnsicm9sZXMiOlsiYXV0aG9yaXplZC1wbGF5ZXIiXX0sImVjb20tc2VydmVyIjp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsInZpZXctcHJvZmlsZSJdfX19.ZuyopXmy2RuNjrLN2s6UfZO0A7iyXxINwmYk5evl1_6vHGD3tG__jn4np2T1LGjH35MR09GBTxAauD7-fwN4lnFOu5fucHlbytaXZ4hs7VArVJ4xlwXQw1-BOYERHLXAX7ANOJiws4xD_sivzd6rVP783JvIxo0RJ6ET4F50MieB-51MCo9iJ_pFj3BMO-eIRNVHo8fYlP2ZLW_bmrnnHlTZy4FpTZhnvP-5yC7vzz0JDUdXNG4gwrDnDglkAEI6FuBt_-xWK1BZO6nZOnhrTaKwPn3p06S4x5soQ9bBS4gBOfCSFEBmBIHGC4kUsWJnzO39IlU15AOtIb4wMyTyAg',
         u'session-state': u'85c76fef-7dfd-4278-8859-264525e3dfab',
         u'token_type': u'bearer'}

        """
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
        if not self.refresh_token or time.time() > self.refresh_token_expiration:
            return False
        else:
            return True

    def get_access_token(self):
        if self.have_valid_access_token():
            return self.access_token
        else:
            self.update_token_data()
            return self.access_token
