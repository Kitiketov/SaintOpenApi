class DomainException(Exception):
    pass

class TooManyRoomsException(DomainException):
    pass

class InvalidRoomNameException(DomainException):
    pass

class BaseRoomException(DomainException):
    def __init__(self, room_name: str):
        self.room_name = room_name

class RoomNotExistException(BaseRoomException):
    pass

class MemberNotExistException(BaseRoomException):
    pass

class UserNotAdminException(BaseRoomException):
    pass