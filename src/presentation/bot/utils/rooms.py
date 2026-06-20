def pick_rooms(data: dict[str, list[str]], as_admin: bool | None = None):
    if as_admin is True:
        return data["admin"]

    if as_admin is False:
        return data["member"]

    return data["admin"] + data["member"]
