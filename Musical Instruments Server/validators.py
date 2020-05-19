from storage import instruments_db


class Validators:
    def __init__(self):
        pass

    def validate_instrument_exists(self, instrument_id):
        if instruments_db.get(instrument_id) == None:
            return False
        else:
            return True


validator = Validators()
