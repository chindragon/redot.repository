# -*-coding:utf-8-*-
import json
import datetime


def json_encoder(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, datetime.date):
        return obj.strftime("%Y-%m-%d")
    else:
        return json.JSONEncoder.default(obj)
