from json import JSONEncoder


class domain():
    def __init__(self, url, expiration, days):
        self.url = url
        self.expiration = expiration
        self.days = days


class domainencoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
