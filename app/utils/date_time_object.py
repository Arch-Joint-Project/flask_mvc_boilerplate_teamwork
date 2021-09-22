from datetime import date, time


def create_date_object(string_date: str):
    if not isinstance(string_date, str):
        raise TypeError("argument is not of type [str]")
    date_values = list(map(int, string_date.split('-')))
    if len(date_values) != 3:
        raise Exception("Date Invalid.")
    if len(date_values) == 3:
        new_date = date(date_values[0], date_values[1], date_values[2])
    return new_date


def create_time_object(string_time: str):
    if not isinstance(string_time, str):
        raise TypeError("argument is not of type [str]")
    time_values = list(map(int, string_time.split(':')))
    if len(time_values) < 2:
        raise Exception("Time Invalid.")
    else:
        new_time = time(time_values[0], time_values[1])
    return new_time
