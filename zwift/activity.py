# -*- coding: utf-8 -*-
from fitparse import FitFile, StandardUnitsDataProcessor

from .request import Request, download_file


class Activity:
    def __init__(self, player_id, get_access_token):
        self.player_id = player_id
        self.request = Request(get_access_token)

    def list(self, start=0, limit=20):
        return self.request.json(
            '/api/profiles/{}/activities/?start={}&limit={}'.format(self.player_id, start, limit))

    def get_data(self, activity_id):
        activity_data = self.get_activity(activity_id)
        fit_file_bucket = activity_data['fitFileBucket']
        fit_file_key = activity_data['fitFileKey']
        fit_file_url = 'https://{}.s3.amazonaws.com/{}'.format(
            fit_file_bucket, fit_file_key)
        raw_fit_data = download_file(fit_file_url)
        records = decode_fit_file(raw_fit_data)
        return process_fit_data(records)

    def get_activity(self, activity_id):
        return self.request.json(
            '/api/profiles/{}/activities/{}'.format(
                self.player_id, activity_id))


def decode_fit_file(raw_fit_data):
    fit_file = FitFile(
        raw_fit_data, data_processor=StandardUnitsDataProcessor())
    return [m for m in fit_file.get_messages() if m.name == 'record']


def process_fit_data(records):
    return [parse_fit_record(r) for r in records]


def parse_fit_record(record):
    return {
        'time': record.get_value('timestamp'),  # datetime in UTC
        'lat': record.get_value('position_lat'),  # WGS84
        'lng': record.get_value('position_long'),  # WGS84
        'altitude': record.get_value('enhanced_altitude'),  # m
        'distance': record.get_value('distance'),  # km
        'speed': record.get_value('enhanced_speed'),  # km/h
        'power': record.get_value('power'),  # watt
        'cadence': record.get_value('cadence'),  # rpm
        'heartrate': record.get_value('heart_rate'),  # bpm
    }
