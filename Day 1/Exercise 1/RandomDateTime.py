from random import randrange
from datetime import datetime, timedelta


def create_random_date():
    start_date = datetime.strptime('1/1/2019 1:30 PM', '%m/%d/%Y %I:%M %p')
    end_date = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
    delta = end_date - start_date
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    date = start_date + timedelta(seconds=random_second)
    date = date.strftime("%m/%d/%Y %H:%M:%S")
    return date


