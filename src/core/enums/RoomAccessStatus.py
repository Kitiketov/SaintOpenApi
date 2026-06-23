from enum import Enum


class RoomAccessStatus(str, Enum):
    MEMBER = "MEMBER"
    ADMIN = "ADMIN"
