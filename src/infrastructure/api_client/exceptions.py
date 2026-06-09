class APIError(Exception):
    pass


class APITooManyRooms(APIError):
    pass


class APIInvalidRoomName(APIError):
    pass