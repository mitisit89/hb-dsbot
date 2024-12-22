from datetime import datetime


def days_until_birthday(birthday_str: str) -> tuple[str, int]:
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d %H:%M:%S")
    today = datetime.today()
    next_birthday = birthday.replace(year=today.year)
    if today > next_birthday:
        next_birthday = next_birthday.replace(year=today.year + 1)
    days_left = (next_birthday - today).days
    next_birthday_day_month = next_birthday.strftime("%d.%b")
    return next_birthday_day_month, days_left


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%y")
        return True
    except ValueError:
        return False
