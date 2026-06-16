from core.schemas.user import User


# todo: вменяемая логика получения из куки id и всего такого
# и создания сущности пользователя (если можно все это оттуда получить)
async def get_current_user() -> User:
    return User(id=99, first_name="Aboba", last_name="Boba", username="BobaAboba")
