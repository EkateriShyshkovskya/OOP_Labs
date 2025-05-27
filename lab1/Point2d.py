from typing import Self

SCREEN_WIDTH, SCREEN_HEIGHT = 1092, 1080

class Point2d:

    # конструктор
    def __init__(self, x: int, y: int) -> None:
        # protected
        self.x = x
        self.y = y

    # getter
    @property
    def x(self) -> int:
        return self._x

    # setter
    @x.setter
    def x(self, x) -> None:
        if x < 0 or x > SCREEN_WIDTH:
            raise ValueError("0 < x < SCREEN_WIDTH")
        self._x = x

    # getter
    @property
    def y(self) -> int:
        return self._y

    # setter
    @y.setter
    def y(self, y) -> None:
        if y < 0 or y > SCREEN_HEIGHT:
            raise ValueError("0 < y < SCREEN_HEIGHT")
        self._y = y

    # методы

    # сравнение точек(по координатам)
    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y

    # строковое представление(пользователю)
    def __str__(self) -> str:
        return f'({self.x}, {self.y})'

    # строковое представление(программистам)
    def __repr__(self) -> str:
        return f'Point2d({self.x}, {self.y})'

