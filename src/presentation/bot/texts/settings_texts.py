def room_settings_info(room_name, price, event_time, exchange_type):
    return (
        f"Настройки комнаты {room_name}\n\n"
        f"💰Диапазон стоимости подарка: {price}\n"
        f"🗓Ориентировочное время проведения: {event_time}\n"
        f"🎁Тип обмена: {exchange_type}"
    )


def prompt_price(price):
    return f"Текущий диапазон: {price}\n" "Напишите новый диапазон стоимости через дефис (например 500-1500)."


def invalid_price():
    return "Некорректный диапазон. Используйте формат 500-1500 (минимум меньше максимума)."


def prompt_event_time(event_time):
    return f"Текущее время проведения: {event_time}\n" "Укажите дату в формате ДД:ММ (например 24:12)."


def invalid_event_time():
    return "Некорректная дата. Используйте формат ДД:ММ и существующие значения."


def choose_exchange_type(current_type):
    return f"Текущий тип обмена: {current_type}\n" "Выберите новый вариант:"


def settings_updated(room_name, price, event_time, exchange_type):
    return (
        f"Настройки комнаты {room_name} обновлены\n\n"
        f"💰Диапазон стоимости подарка: {price}\n"
        f"🗓Ориентировочное время проведения: {event_time}\n"
        f"🎁Тип обмена: {exchange_type}"
    )
