class APIError(Exception):
    def __init__(self, status_code: int = 500, detail: str = "API error"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)


class APITooManyRooms(APIError):
    def __init__(self):
        super().__init__(400, "Too many rooms")


class APIInvalidRoomName(APIError):
    def __init__(self):
        super().__init__(422, "Invalid room name")
