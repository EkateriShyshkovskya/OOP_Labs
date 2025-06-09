import re
import sys
from abc import abstractmethod
from datetime import datetime
from typing import List, Protocol
import socket

# 1. Протокол фильтра
class LogFilterProtocol(Protocol):
    @abstractmethod
    def match(self, text: str) -> bool:
        """Проверяет, подходит ли текст под фильтр: класс, который реализует match() -> bool, считается фильтром"""
        pass


# 2. Классы фильтров

class SimpleLogFilter:
    """
    Фильтр по подстроке: проверяет, содержится ли заданный текст в сообщении.
    """
    def __init__(self, pattern: str):
        self.pattern = pattern

    def match(self, text: str) -> bool:
        return self.pattern.lower() in text.lower()


class ReLogFilter:
    """
    Фильтр по регулярному выражению: для поиска совпадений в сообщении
    """
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def match(self, text: str) -> bool:
        return bool(self.pattern.search(text))


# 3. Протокол обработчика
class LogHandlerProtocol(Protocol):
    @abstractmethod
    def handle(self, text: str) -> None:
        """Обрабатывает текст сообщения: класс с методом handle() считается обработчиком"""
        pass


# 4. Классы обработчиков

class FileHandler:
    """
    Обработчик: Запись логов в файл.
    """
    def __init__(self, filename: str):
        self.filename = filename

    def handle(self, text: str) -> None:
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write(f"{text}\n")
        except Exception as e:
            print(f"[FileHandler] Ошибка при записи в файл: {e}")


class SocketHandler:
    """Запись логов в системные логи"""
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def handle(self, text: str) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(f"[{datetime.now()}] {text}\n".encode("utf-8"))
        except socket.error as e:
            print(f"SocketHandler error: {e}")


class ConsoleHandler:
    """Вывод логов в консоль"""
    def handle(self, text: str) -> None:
        print(f"{text}")


class SyslogHandler:
    """Отправка логов через сокет"""
    def __init__(self, facility: str = "user"):
        self.facility = facility

    def handle(self, text: str) -> None:
        try:
            sys.stderr.write(f"[{datetime.now()}] {text}\n")
        except Exception as e:
            print(f"SyslogHandler error: {e}")


# 5. Основной класс логгера
class Logger:
    """
    Класс Logger принимает фильтры и обработчики.
    Вызывает обработку только если все фильтры одобряют сообщение.
    """
    def __init__(self, filters: List[LogFilterProtocol] = None, handlers: List[LogHandlerProtocol] = None):
        self.filters = filters or []
        self.handlers = handlers or []

    def log(self, text: str) -> None:
        if not text:
            return
        # Применяем все фильтры
        for f in self.filters:
            if not f.match(text):
                return
        # Отправляем сообщение всем обработчикам
        for handler in self.handlers:
            handler.handle(text)


if __name__ == "__main__":
    # Создаем фильтры
    filters = [
        SimpleLogFilter("ERROR"),
        ReLogFilter(r"\d{4}-\d{2}-\d{2}")  # Дата в формате YYYY-MM-DD
    ]

    # Создаем обработчики
    handlers = [
        ConsoleHandler(),
        FileHandler("log_output.txt"),
    ]

    # Создаем логгер с фильтрами и обработчиками
    logger = Logger(filters, handlers)

    # Демонстрация логирования
    print("\n=== Демонстрация системы логирования ===\n")

    logger.log("2025-06-08 ERROR: Something went wrong")   # пройдет оба фильтра
    logger.log("2025-06-08 ERROR: Disk is full")           # пройдет оба фильтра
    logger.log("2025-06-08 INFO: Just a test")             # нет слова ERROR
    logger.log("ERROR without date")                       # нет даты
    logger.log("2025-06-08 ERROR: Out of memory")          # пройдет оба фильтра

    print("\nЛогирование завершено. Проверь файл 'log_output.txt'.")

