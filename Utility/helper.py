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