from datetime import date, datetime


def get_timestamp():
    now = datetime.now()
    return now.strftime("%d%m%Y%H%M%S")


def get_todays_date():
    return date.today().strftime("%d-%m-%Y")
