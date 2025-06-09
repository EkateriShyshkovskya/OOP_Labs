from enum import Enum
from typing import Self

COLORING = "\033[{}m{}"  # установка цвета
PLACING = "\033[{};{}H{}"  # позиция курсора и вывод текста

# ANSI-коды цветов
class Color(Enum):
    TRANSPARENT = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


class Printer:
    _font: dict[str, list[str]] = {}    # Словарь для хранения шрифта
    _char_width: int = 5      # ширина символа по умолчанию
    _char_height: int = 5     # длина символа по умолчанию
    _font_type: str = ""      # 'font5' или 'font7'

    # Создает объект с заданным цветом, позицией и символом
    def __init__(self, color: Color, position: tuple[int, int], symbol: str) -> None:
        self.color = color
        self.symbol = symbol
        self.current_x, self.current_y = position

# Загрузка шрифта из файла
    @classmethod
    def load_font(cls, filename: str = "font") -> None:
        try:
            with open(filename, "r") as file:   # Открываем файл шрифта для чтения
                cls._font.clear()        # Очищаем текущий словарь шрифтов
                cls._char_height = int(file.readline().strip())     # Читаем высоту символа
                cls._char_width = int(file.readline().strip())      # Читаем ширину символа

                # Определяем тип шрифта по имени файла
                if "font5" in filename.lower():
                    cls._font_type = "font5"
                elif "font7" in filename.lower():
                    cls._font_type = "font7"
                # Создаем пробел в шрифте
                cls._font[' '] = [' ' * cls._char_width for _ in range(cls._char_height)]

                # Читаем символы из файла
                while True:
                    char = file.readline().replace('-', '').strip()
                    if char == '':      # Пустая строка - конец файла
                        break
                    cls._font[char] = []     # Добавляем новый символ в шрифт
                    for _ in range(cls._char_height):
                        line = file.readline()[:cls._char_width]
                        if '-' in line:
                            raise ValueError(
                                f"Font file is not valid, character height is not consistent. List of correct characters: {cls._font.keys()}")
                        cls._font[char].append(line)
        # Обработка ошибок
        except Exception as e:
            print(f"Error loading font file: {e}")
            raise FileNotFoundError

    # Вывод текста(статистически)
    @classmethod
    def print_(cls, text: str, color: Color, position: tuple[int, int], symbol: str) -> None:
        if not cls._font:
            cls.load_font()

        x, y = position     # Начальная позиция
        # Пропускаем символы, отсутствующие в шрифте
        for char in text:
            if char not in cls._font:
                raise ValueError(f"Character {char} is not in the font file")

            # Печатаем символ построчно
            for line_num, line in enumerate(cls._font[char]):
                rendered = line.replace("*", symbol)
                print(PLACING.format(y + line_num + 1, x + 1, COLORING.format(color.value, rendered)), end="")

            x += cls._char_width

            # Добавляем пробел между символами (разный для font5 и font7)
            if char != ' ':  # Не добавляем пробел после пробела
                space_size = 2 if cls._font_type == "font5" else 1
                for line_num in range(cls._char_height):
                    print(PLACING.format(y + line_num + 1, x + 1, " " * space_size), end="")
                x += space_size
        print()

# Контекстный менеджер
    # устанавливает цвет текста перед выполнением блока with
    def __enter__(self) -> Self:
        print(COLORING.format(self.color.value, ''), end="")
        return self
    # сбрасывает цвет после завершения блока with
    def __exit__(self, *args) -> None:
        print(COLORING.format(Color.TRANSPARENT.value, ''), end="")

# Вывод текста с созданием экземпляра класса
    def print(self, text: str) -> None:
        if not self._font:
            self.load_font()
        # Начальные координаты для вывода текста
        x, y = self.current_x, self.current_y
        for char in text:
            if char not in self._font:
                continue

            # Печатаем символ построчно
            for line_num, line in enumerate(self._font[char]):
                rendered = line.replace("*", self.symbol)
                print(PLACING.format(y + line_num + 1, x + 1, rendered), end="")

            # После вывода символа увеличиваем x-координату на ширину символа
            x += self._char_width

            # Добавляем пробел между символами (разный для font5 и font7)
            if char != ' ':  # Не добавляем пробел после пробела
                space_size = 2 if self._font_type == "font5" else 1
                for line_num in range(self._char_height):
                    print(PLACING.format(y + line_num + 1, x + 1, " " * space_size), end="")
                x += space_size

        self.current_x = x


if __name__ == "__main__":
    for _ in range(30):
        print()
    Printer.load_font(filename="C:/Users/user/Desktop/lab2/font5.txt")
    Printer.print_("HELLO", Color.BLUE, (5, 2), "&")

    Printer.load_font(filename="C:/Users/user/Desktop/lab2/font7.txt")
    with Printer(Color.WHITE, (10, 10), "$") as printer:
        printer.print("WORLD")


