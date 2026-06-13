from abc import ABC, abstractmethod
from typing import Any, AsyncGenerator


class ISaintRepository(ABC):

    @abstractmethod
    async def create_room(self, room_name: str, user_id: int) -> str:
        """Создает комнату и возвращает её room_id."""
        pass

    @abstractmethod
    async def add_user(self, user: Any) -> None:
        """Добавляет нового пользователя в систему."""
        pass

    @abstractmethod
    async def update_user(self, user: Any) -> None:
        """Обновляет данные существующего пользователя."""
        pass

    @abstractmethod
    async def connect_to_room(self, room_iden: str, user_id: int) -> str | bool:
        """Подключает пользователя к комнате. Возвращает True или строку ошибки."""
        pass

    @abstractmethod
    async def get_members_list(self, room_iden: str) -> tuple[list[Any], Any, bool]:
        """Возвращает список участников, админа и флаг, является ли админ участником."""
        pass

    @abstractmethod
    async def leave_room(self, room_iden: str, user_id: int) -> None:
        """Удаляет пользователя из участников комнаты."""
        pass

    @abstractmethod
    async def get_my_rooms(self, user_id: int, as_admin: bool) -> list[str]:
        """Возвращает список идентификаторов комнат пользователя."""
        pass

    @abstractmethod
    async def delete_room(self, room_iden: str, admin_id: int) -> None:
        """Полностью удаляет комнату и связи участников."""
        pass

    @abstractmethod
    async def write_pairs(self, pairs: dict[int, int], room_iden: str) -> None:
        """Записывает распределенные пары "Тайного Санты"."""
        pass

    @abstractmethod
    async def start_event(self, room_iden: str) -> None:
        """Переводит комнату в статус 'запущено'."""
        pass

    @abstractmethod
    async def who_gives(self, room_iden: str, user_id: int) -> int | str:
        """Возвращает ID получателя подарка для конкретного пользователя."""
        pass

    @abstractmethod
    async def is_started(self, room_iden: str) -> bool:
        """Проверяет, запущено ли событие в комнате."""
        pass

    @abstractmethod
    async def get_user(self, user_id: int) -> Any | None:
        """Возвращает данные пользователя по его ID."""
        pass

    @abstractmethod
    async def check_room_and_member(self, user_id: int, room_iden: str) -> str | bool:
        """Проверяет существование комнаты и статус членства пользователя."""
        pass

    @abstractmethod
    async def get_room_admin(self, room_iden: str) -> int | None:
        """Возвращает ID администратора комнаты."""
        pass

    @abstractmethod
    async def count_user_room(self, user_id: int) -> int:
        """Возвращает количество комнат, в которых состоит пользователь."""
        pass

    @abstractmethod
    async def get_wishes_and_photo(self, room_iden: str, user_id: int) -> tuple[str | bool, str | None, str | None]:
        """Возвращает статус проверки, пожелания и ID фото участника."""
        pass

    @abstractmethod
    async def edit_wishes(self, wishes: str, user_id: int, room_iden: str, photo_id: str = "") -> str | bool:
        """Обновляет пожелания и фото пользователя в конкретной комнате."""
        pass

    @abstractmethod
    async def get_room_settings(self, room_iden: str) -> tuple[str | bool, str | None, str | None, str | None]:
        """Возвращает настройки комнаты (бюджет, время, тип обмена)."""
        pass

    @abstractmethod
    async def update_room_settings(
        self, room_iden: str, price: str | None = None, event_time: str | None = None, exchange_type: str | None = None
    ) -> str | None:
        """Обновляет конфигурацию настроек комнаты."""
        pass

    @abstractmethod
    async def get_stats(self) -> tuple[int, int, int, int]:
        """Возвращает общую статистику (пользователи, участники, комнаты, запущенные)."""
        pass

    @abstractmethod
    def get_all_users(self) -> AsyncGenerator[int, None]:
        """Асинхронный генератор, отдающий ID всех пользователей."""
        pass
