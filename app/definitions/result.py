from flask import json


class Result:
    def __init__(self, value, status_code):
        self.status_code = status_code
        self.value = value
