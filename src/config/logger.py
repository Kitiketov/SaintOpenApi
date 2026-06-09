import logging


def setup_logging() -> None:
    """Инициализация базовых настроек логирования для всего проекта"""
    logging.basicConfig(
        level=logging.INFO,
        filename="py_log.log",
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )
