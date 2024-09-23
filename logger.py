import logging
from datetime import datetime
from contextlib import contextmanager


class EventLogger:
    def __init__(self):
        # Создаем глобальную переменную для хранения текущего ID пользователя
        self.current_user_id = None

        # Создаем логгер
        self.logger = logging.getLogger('my_bot_logger')
        self.logger.setLevel(logging.DEBUG)

        # Создаем форматтер для логов
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [User ID: %(user_id)s] - %(message)s')

        # Создаем обработчик для записи логов в файл с таймстэмпом
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_filename = f'bot_log_{timestamp}.log'
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Добавляем фильтр для добавления ID пользователя
        user_id_filter = self.UserIdFilter(self)
        self.logger.addFilter(user_id_filter)

        # Добавляем обработчик к логгеру
        self.logger.addHandler(file_handler)

    @contextmanager
    def log_user_context(self, user_id):
        old_user_id = self.current_user_id
        self.current_user_id = user_id
        try:
            yield
        finally:
            self.current_user_id = old_user_id

    class UserIdFilter(logging.Filter):
        def __init__(self, event_logger):
            super().__init__()
            self.event_logger = event_logger

        def filter(self, record):
            record.user_id = self.event_logger.current_user_id
            return True

    def handle_event(self, user_id, event):
        with self.log_user_context(user_id):
            try:
                self.logger.debug(f'Handling event: {event}')
                # Обработка события
                # ...
            except Exception as e:
                self.logger.exception(f"Exception occurred while handling event: {event}")
