from pathlib import Path
from datetime import *
from dateutil.relativedelta import *
import calendar
import json


def get_string(items: list[str]) -> str:
    result = []
    for item in items:
        if item:
            result.append(item)

    return ", ".join(result)


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
    if (dt + relativedelta(days=+1)).timestamp() > datetime.now().timestamp():
        return f"сегодня в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+2)).timestamp() > datetime.now().timestamp():
        return f"вчера в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+3)).timestamp() > datetime.now().timestamp():
        return f"2 дня назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+4)).timestamp() > datetime.now().timestamp():
        return f"3 дня назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+5)).timestamp() > datetime.now().timestamp():
        return f"4 дня назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+6)).timestamp() > datetime.now().timestamp():
        return f"5 дней назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+7)).timestamp() > datetime.now().timestamp():
        return f"6 дней назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(days=+8)).timestamp() > datetime.now().timestamp():
        return f"неделю назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(months=+1)).timestamp() > datetime.now().timestamp():
        return f"месяц назад в {dt.strftime('%H:%M')}"
    elif (dt + relativedelta(years=+1)).timestamp() > datetime.now().timestamp():
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


def save_file(path: Path, file_name: str, obj_list: list) -> None:
    dir_path = path.joinpath(
        path, file_name
    )
    with open(dir_path, 'w', encoding='utf-8') as f:
        json.dump(obj_list, f, ensure_ascii=False)
