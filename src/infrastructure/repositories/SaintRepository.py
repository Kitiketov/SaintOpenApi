import asyncio
import random
import sqlite3
from typing import Any, AsyncGenerator

from infrastructure.repositories.interfaces.ISaintRepository import ISaintRepository
from src.config.settings import Settings


class SqliteSaintRepository(ISaintRepository):
    def __init__(self, settings: Settings):
        self.settings = settings
        self.conn = sqlite3.connect(settings.db_path, check_same_thread=False)

    def _is_valid_name(self, name: str) -> bool:
        forbidden = ["_saint", "_mem", "\\", ".", "/", ",", ":", ";", "'", '"', " ", "*", "+", "-", "#", "@", "$", "%",
                     "^", "!", "~", "`", "&", "|", "<", ">", "[", "]", "(", ")", "{", "}"]
        return all(char not in name for char in forbidden) and not name[0].isdigit() and len(name) <= 30

    async def start_db(self) -> None:
        def _init():
            cur = self.conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS rooms("
                "room_iden TEXT PRIMARY KEY, status BOOLEAN DEFAULT FALSE, admin INTEGER, "
                f"gift_price_range TEXT DEFAULT '{self.settings.room_default_price}', "
                f"event_time TEXT DEFAULT '{self.settings.room_default_event_time}', "
                f"exchange_type TEXT DEFAULT '{self.settings.room_default_exchange_type}'"
                ")"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS users(tg_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, username TEXT)")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS user_rooms("
                "tg_id INTEGER, room_iden TEXT, is_member BOOLEAN DEFAULT FALSE, is_admin BOOLEAN DEFAULT FALSE, "
                "PRIMARY KEY (tg_id, room_iden))"
            )
            self.conn.commit()

        await asyncio.to_thread(_init)
        await self.migrate_rooms_table()

    async def create_room(self, room_name: str, user_id: int) -> str | None:
        if not self._is_valid_name(room_name):
            return None

        def _db_ops():
            cur = self.conn.cursor()
            while True:
                room_id = f"{random.randint(1, 9999):04}"
                room_iden = f"{room_name}{room_id}"
                if not cur.execute("SELECT 1 FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone():
                    break

            cur.execute("INSERT INTO rooms (room_iden, admin) VALUES (?, ?)", (room_iden, user_id))
            cur.execute(f"CREATE TABLE {room_iden}_mem (user_id INTEGER PRIMARY KEY, wishes TEXT, photo_id TEXT)")
            cur.execute(f"CREATE TABLE {room_iden}_saint (saint_user_id INTEGER PRIMARY KEY, reciver_user_id INTEGER)")
            cur.execute("INSERT OR IGNORE INTO user_rooms (tg_id, room_iden) VALUES (?, ?)", (user_id, room_iden))
            cur.execute("UPDATE user_rooms SET is_admin = TRUE WHERE tg_id = ? AND room_iden = ?", (user_id, room_iden))
            self.conn.commit()
            return room_id

        return await asyncio.to_thread(_db_ops)

    async def add_user(self, user: Any) -> None:
        def _ops():
            cur = self.conn.cursor()
            if not cur.execute("SELECT * FROM users WHERE tg_id = ?", (user.id,)).fetchone():
                cur.execute("INSERT INTO users (tg_id, first_name, last_name, username) VALUES (?, ?, ?, ?)",
                            (user.id, user.first_name, user.last_name, user.username))
                self.conn.commit()

        await asyncio.to_thread(_ops)

    async def update_user(self, user: Any) -> None:
        await self.add_user(user)

        def _ops():
            cur = self.conn.cursor()
            cur.execute("UPDATE users SET first_name = ?, last_name = ?, username = ? WHERE tg_id = ?",
                        (user.first_name, user.last_name, user.username, user.id))
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def connect_to_room(self, room_name: str, room_id: str, user_id: int) -> str | bool:
        room_iden = f"{room_name}{room_id}"
        if not self._is_valid_name(room_name):
            return "room_error"

        def _ops():
            cur = self.conn.cursor()
            room = cur.execute("SELECT * FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone()
            if not room:
                return "room_error"
            if room[1]:  # status == True (событие запущено)
                return "joined late"

            if cur.execute(f"SELECT * FROM {room_iden}_mem WHERE user_id = ?", (user_id,)).fetchone():
                return "user_error"

            cur.execute(f"INSERT INTO {room_iden}_mem (user_id, wishes) VALUES (?, '-')", (user_id,))

            if not cur.execute("SELECT * FROM user_rooms WHERE tg_id = ? AND room_iden = ?",
                               (user_id, room_iden)).fetchone():
                cur.execute("INSERT INTO user_rooms (tg_id, room_iden, is_member, is_admin) VALUES (?, ?, TRUE, FALSE)",
                            (user_id, room_iden))
            else:
                cur.execute("UPDATE user_rooms SET is_member = TRUE WHERE tg_id = ? AND room_iden = ?",
                            (user_id, room_iden))
            self.conn.commit()
            return True

        return await asyncio.to_thread(_ops)

    async def get_members_list(self, room_iden: str) -> tuple[list[Any], Any, bool]:
        def _ops():
            cur = self.conn.cursor()
            admin_id = cur.execute("SELECT admin FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone()[0]
            member_ids = cur.execute(f"SELECT user_id FROM {room_iden}_mem").fetchall()
            admin = cur.execute("SELECT * FROM users WHERE tg_id = ?", (admin_id,)).fetchone()

            member_list = []
            is_admin_member = False
            for (m_id,) in member_ids:
                if m_id != admin_id:
                    member = cur.execute("SELECT * FROM users WHERE tg_id = ?", (m_id,)).fetchone()
                    if member:
                        member_list.append(member)
                else:
                    is_admin_member = True
            return member_list, admin, is_admin_member

        return await asyncio.to_thread(_ops)

    async def leave_room(self, room_iden: str, user_id: int) -> None:
        def _ops():
            cur = self.conn.cursor()
            cur.execute(f"DELETE FROM {room_iden}_mem WHERE user_id = ?", (user_id,))
            cur.execute("UPDATE user_rooms SET is_member = FALSE WHERE tg_id = ? AND room_iden = ?",
                        (user_id, room_iden))
            cur.execute(
                "DELETE FROM user_rooms WHERE tg_id = ? AND room_iden = ? AND is_member = FALSE AND is_admin = FALSE",
                (user_id, room_iden))
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def get_my_rooms(self, user_id: int, as_admin: bool) -> list[str]:
        def _ops():
            cur = self.conn.cursor()
            flag = "is_admin" if as_admin else "is_member"
            rooms = cur.execute(f"SELECT room_iden FROM user_rooms WHERE tg_id = ? AND {flag} = TRUE",
                                (user_id,)).fetchall()
            return [r[0] for r in rooms]

        return await asyncio.to_thread(_ops)

    async def delete_room(self, room_iden: str, admin_id: int) -> None:
        def _ops():
            cur = self.conn.cursor()
            users_id = cur.execute(f"SELECT user_id FROM {room_iden}_mem").fetchall()
            cur.execute("DELETE FROM user_rooms WHERE tg_id = ? AND room_iden = ?", (admin_id, room_iden))
            for (u_id,) in users_id:
                cur.execute("DELETE FROM user_rooms WHERE tg_id = ? AND room_iden = ?", (u_id, room_iden))
            cur.execute(f"DROP TABLE IF EXISTS {room_iden}_mem")
            cur.execute(f"DROP TABLE IF EXISTS {room_iden}_saint")
            cur.execute("DELETE FROM rooms WHERE room_iden = ?", (room_iden,))
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def write_pairs(self, pairs: dict[int, int], room_iden: str) -> None:
        def _ops():
            cur = self.conn.cursor()
            for giver, receiver in pairs.items():
                cur.execute(f"INSERT INTO {room_iden}_saint (saint_user_id, reciver_user_id) VALUES (?, ?)",
                            (giver, receiver))
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def start_event(self, room_iden: str) -> None:
        def _ops():
            cur = self.conn.cursor()
            cur.execute("UPDATE rooms SET status = TRUE WHERE room_iden = ?", (room_iden,))
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def who_gives(self, room_iden: str, user_id: int) -> int | str:
        def _ops():
            cur = self.conn.cursor()
            pair = cur.execute(f"SELECT reciver_user_id FROM {room_iden}_saint WHERE saint_user_id = ?",
                               (user_id,)).fetchone()
            return pair[0] if pair else "JOINED LATE"

        return await asyncio.to_thread(_ops)

    async def is_started(self, room_iden: str) -> bool:
        def _ops():
            cur = self.conn.cursor()
            res = cur.execute("SELECT status FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone()
            return bool(res[0]) if res else False

        return await asyncio.to_thread(_ops)

    async def get_user(self, user_id: int) -> Any | None:
        return await asyncio.to_thread(
            lambda: self.conn.cursor().execute("SELECT * FROM users WHERE tg_id = ?", (user_id,)).fetchone())

    async def check_room_and_member(self, user_id: int, room_iden: str) -> str | bool:
        def _ops():
            cur = self.conn.cursor()
            room = cur.execute("SELECT admin FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone()
            if not room:
                return "ROOM NOT EXISTS"
            user = cur.execute(f"SELECT 1 FROM {room_iden}_mem WHERE user_id = ?", (user_id,)).fetchone()
            if not user and room[0] == user_id:
                return "IS ADMIN"
            if not user:
                return "MEMBER NOT EXISTS"
            return True

        return await asyncio.to_thread(_ops)

    async def get_room_admin(self, room_iden: str) -> int | None:
        def _ops():
            res = self.conn.cursor().execute("SELECT admin FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone()
            return res[0] if res else None

        return await asyncio.to_thread(_ops)

    async def count_user_room(self, user_id: int) -> int:
        def _ops():
            res = self.conn.cursor().execute("SELECT COUNT(*) FROM user_rooms WHERE tg_id = ?", (user_id,)).fetchone()
            return res[0] if res else 0

        return await asyncio.to_thread(_ops)

    async def get_wishes_and_photo(self, room_iden: str, user_id: int) -> tuple[str | bool, str | None, str | None]:
        def _ops():
            cur = self.conn.cursor()
            if not cur.execute("SELECT 1 FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone():
                return "ROOM NOT EXISTS", None, None
            user = cur.execute(f"SELECT wishes, photo_id FROM {room_iden}_mem WHERE user_id = ?", (user_id,)).fetchone()
            if not user:
                return "MEMBER NOT EXISTS", None, None
            return True, user[0], user[1]

        return await asyncio.to_thread(_ops)

    async def edit_wishes(self, wishes: str, user_id: int, room_iden: str, photo_id: str = "") -> str | bool:
        def _ops():
            cur = self.conn.cursor()
            if not cur.execute("SELECT 1 FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone():
                return "ROOM NOT EXISTS"
            if not cur.execute(f"SELECT 1 FROM {room_iden}_mem WHERE user_id = ?", (user_id,)).fetchone():
                return "MEMBER NOT EXISTS"
            cur.execute(f"UPDATE {room_iden}_mem SET wishes = ?, photo_id = ? WHERE user_id = ?",
                        (wishes, photo_id, user_id))
            self.conn.commit()
            return True

        return await asyncio.to_thread(_ops)

    async def migrate_rooms_table(self) -> None:
        def _ops():
            cur = self.conn.cursor()
            columns = [col[1] for col in cur.execute("PRAGMA table_info(rooms)").fetchall()]
            migrations = [
                ("gift_price_range",
                 f"ALTER TABLE rooms ADD COLUMN gift_price_range TEXT DEFAULT '{self.settings.room_default_price}'"),
                ("event_time",
                 f"ALTER TABLE rooms ADD COLUMN event_time TEXT DEFAULT '{self.settings.room_default_event_time}'"),
                ("exchange_type",
                 f"ALTER TABLE rooms ADD COLUMN exchange_type TEXT DEFAULT '{self.settings.room_default_exchange_type}'"),
            ]
            for column, query in migrations:
                if column not in columns:
                    cur.execute(query)
            self.conn.commit()

        await asyncio.to_thread(_ops)

    async def get_room_settings(self, room_iden: str) -> tuple[str | bool, str | None, str | None, str | None]:
        def _ops():
            res = self.conn.cursor().execute(
                "SELECT gift_price_range, event_time, exchange_type FROM rooms WHERE room_iden = ?",
                (room_iden,)).fetchone()
            if not res:
                return "ROOM NOT EXISTS", None, None, None
            return True, res[0], res[1], res[2]

        return await asyncio.to_thread(_ops)

    async def update_room_settings(self, room_iden: str, price: str | None = None, event_time: str | None = None,
                                   exchange_type: str | None = None) -> str | None:
        def _ops():
            cur = self.conn.cursor()
            if not cur.execute("SELECT 1 FROM rooms WHERE room_iden = ?", (room_iden,)).fetchone():
                return "ROOM NOT EXISTS"
            if price is not None:
                cur.execute("UPDATE rooms SET gift_price_range = ? WHERE room_iden = ?", (price, room_iden))
            if event_time is not None:
                cur.execute("UPDATE rooms SET event_time = ? WHERE room_iden = ?", (event_time, room_iden))
            if exchange_type is not None:
                cur.execute("UPDATE rooms SET exchange_type = ? WHERE room_iden = ?", (exchange_type, room_iden))
            self.conn.commit()

        return await asyncio.to_thread(_ops)

    async def get_stats(self) -> tuple[int, int, int, int]:
        def _ops():
            cur = self.conn.cursor()
            total_users = (cur.execute("SELECT COUNT(*) FROM users").fetchone() or [0])[0]
            participants = \
            (cur.execute("SELECT COUNT(DISTINCT tg_id) FROM user_rooms WHERE is_member = TRUE").fetchone() or [0])[0]
            rooms_total = (cur.execute("SELECT COUNT(*) FROM rooms").fetchone() or [0])[0]
            started_rooms = (cur.execute("SELECT COUNT(*) FROM rooms WHERE status = TRUE").fetchone() or [0])[0]
            return total_users, participants, rooms_total, started_rooms

        return await asyncio.to_thread(_ops)

    async def get_all_users(self) -> AsyncGenerator[int, None]:
        def _fetch():
            return [row[0] for row in self.conn.cursor().execute("SELECT DISTINCT tg_id FROM users").fetchall()]

        user_ids = await asyncio.to_thread(_fetch)
        for u_id in user_ids:
            yield u_id