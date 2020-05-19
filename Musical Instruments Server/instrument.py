

class Instrument(dict):
    def __init__(self, instrument_object):
        dict.__init__(self, instrument=instrument_object.get("instrument"), user=instrument_object.get("user"), videos=None, images = [])





