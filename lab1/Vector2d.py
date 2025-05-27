from typing import Self
from typing import Generator
import math
from Point2d import Point2d

class Vector2d:

    # конструктор
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def frompoints(cls, p1: Point2d, p2: Point2d) -> Self:
        return cls(p2.x - p1.x, p2.y - p1.y)

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y

    # обращение к координатам вектора по индексу
    def __getitem__(self, index) -> int:
        match index:
            case 0:
                return self.x
            case 1:
                return self.y
            case _:
                raise IndexError("Index out of range")

    # устанавливает координаты вектора по индексам
    def __setitem__(self, index: int, value: int) -> None:
        match index:
            case 0:
                self.x = value
            case 1:
                self.y = value
            case _:
                raise IndexError("Index out of range")

    # итерирование объекта
    def __iter__(self) -> Generator[int, None, None]:
        yield self.x
        yield self.y

    # итерирование объекта
    def __len__(self) -> int:
        return 2  # двумерное пространство

    #  сравнения объектов на эквивалентность
    def __eq__(self, value: Self) -> bool:
        return self.x == value.x and self.y == value.y

    # строкове представление объекта
    def __str__(self) -> str:
        return f"Vector2d({self.x}, {self.y})"

    # строкове представление объекта
    def __repr__(self) -> str:
        return str(self)

    # модуль вектора
    def __abs__(self) -> float:
        return math.sqrt((self.x * self.x) + (self.y * self.y))

    # сложение векторов
    def __add__(self, value: Self) -> Self:
        return Vector2d(self.x + value.x, self.y + value.y)

    # вычитание векторов
    def __sub__(self, value: Self) -> Self:
        return Vector2d(self.x - value.x, self.y - value.y)

    # умножение вектора на число
    def __mul__(self, value: int) -> Self:
        return Vector2d(self.x * value, self.y * value)

    # целочисленное деление векторов
    def __truediv__(self, value: int) -> Self:
        return Vector2d(self.x // value, self.y // value)

    # скалярное произведение векторов
    def dot(self, other: Self) -> float:
        return self.x * other.x + self.y * other.y

    # скалярное произведение векторов(статитический метод)
    @staticmethod
    def dot_product(vector1: Self, vector2: Self) -> int:
        return vector1.x * vector2.x + vector1.y * vector2.y

    # векторное произведение векторов
    def cross(self, other: Self) -> int:
        return self.x * other.y - self.y * other.x

    # векторное произведение векторов(статитический метод)
    @staticmethod
    def cross_product(vector1: Self, vector2: Self) -> int:
        return vector1.x * vector2.y - vector1.y * vector2.x

    # смешанное произведение векторов
    def triple(self, vector2: Self, vector3: Self) -> int:
        return 0  # векторы компланарны

    # смешанное произведение векторов(статитический метод)
    @staticmethod
    def triple_product(vector1: Self, vector2: Self, vector3: Self) -> int:
        return 0  # векторы компланарны