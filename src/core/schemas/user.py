from pydantic import BaseModel


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str

    @classmethod
    def from_row(cls, row):
        row = dict(row)
        return cls(
            id=int(row["tg_id"]),
            first_name=row["first_name"],
            last_name=row["last_name"],
            username=row["username"],
        )
