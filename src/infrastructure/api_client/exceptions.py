class APIError(Exception):
    def __init__(self, status_code: int = 500, detail: str = "API error"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)