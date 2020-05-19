from storage import instruments_db


class Validators:
    def __init__(self):
        pass

    def instrument_exists(self, instrument_id):
        if instruments_db.get(instrument_id) is None:
            return False
        else:
            return True

    def instrument_has_key(self, instrument_id, key):
        if instruments_db.get(instrument_id).get(key) is None:
            return False
        else:
            return True


validator = Validators()

