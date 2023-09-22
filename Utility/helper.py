from datetime import datetime, timedelta


def get_by_id(id: int, items: list) -> object | None:
    res = None
    for item in items:
        if type(item) is dict:
            if item['id'] == id:
                res = item
                break
        else:
            if item.id == id:
                res = item
                break

    return res


def format_date(dt: datetime) -> str:
    if dt + timedelta(days=1) > datetime.now():
        return f"сегодня в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=2) > datetime.now():
        return f"вчера в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=3) > datetime.now():
        return f"2 дня назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=4) > datetime.now():
        return f"3 дня назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=5) > datetime.now():
        return f"4 дня назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=6) > datetime.now():
        return f"5 дней назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=7) > datetime.now():
        return f"6 дней назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=8) > datetime.now():
        return f"неделю назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=31) > datetime.now():
        return f"месяц назад в {dt.strftime('%H:%M')}"
    elif dt + timedelta(days=365) > datetime.now():
        return f"год назад в {dt.strftime('%H:%M')}"
    else:
        return dt.strftime("%d.%m.%Y в %H:%M")


def format_date_without_time(dt: datetime) -> str:
    if dt + timedelta(days=1) > datetime.now():
        return f"сегодня"
    elif dt + timedelta(days=2) > datetime.now():
        return f"вчера"
    elif dt + timedelta(days=3) > datetime.now():
        return f"2 дня назад"
    elif dt + timedelta(days=4) > datetime.now():
        return f"3 дня назад"
    elif dt + timedelta(days=5) > datetime.now():
        return f"4 дня назад"
    elif dt + timedelta(days=6) > datetime.now():
        return f"5 дней назад"
    elif dt + timedelta(days=7) > datetime.now():
        return f"6 дней назад"
    elif dt + timedelta(days=8) > datetime.now():
        return f"неделю назад"
    elif dt + timedelta(days=31) > datetime.now():
        return f"месяц назад"
    elif dt + timedelta(days=365) > datetime.now():
        return f"год назад"
    else:
        return dt.strftime("%d.%m.%Y")
