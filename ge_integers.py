# TODO page number wrong

from typing import NamedTuple, Union, TypeVar, Type
from abc import ABC, abstractmethod
import re
import sys

from mod_arith import cornacchias

# cannot import Self until python 3.11 :(
TGEInt = TypeVar("TGEInt", bound="GEInteger")


class GEInteger(ABC):
    _x: int
    _y: int

    # i or w (omega) for Gaussian and Eisenstein integers respectively
    _special_character: str = 'i'

    __slots__ = ('_x', '_y')

    def __init__(self, x: int = 0, y: int = 0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self: TGEInt, other: TGEInt, /) -> TGEInt:
        return self.__class__(self._x + other._x, self._y + other._y)

    def __sub__(self: TGEInt, other: TGEInt, /) -> TGEInt:
        return self.__class__(self._x - other._x, self._y - other._y)

    # could potentially allow this to work with complex/int
    def __eq__(self: TGEInt, other: TGEInt, /) -> bool:
        if not isinstance(other, type(self)):
            return False

        return self._x == other._x and self._y == other._y

    @abstractmethod
    def __mul__(self: TGEInt, other: TGEInt, /) -> TGEInt:
        ...

    def norm(self):
        return (self * self.conj())._x

    @abstractmethod
    def conj(self: TGEInt) -> TGEInt:
        ...

    # follows the pseudocode in Prime Numbers: A Computational Perspective, page 468
    # Algorithm 9.3.2
    def __pow__(self, exponent: int, /):
        if exponent < 0:
            raise ValueError("exponent must be a non-negative integer")

        base = self
        ret = type(self)(1)

        while exponent != 0:
            if exponent % 2 == 1:
                ret *= base

            base *= base
            exponent //= 2

        return ret

    @classmethod
    def from_string(cls: Type[TGEInt], s: str, /) -> TGEInt:
        m = re.fullmatch(
            rf' *((\([ +\-{cls._special_character}0-9]+\))|([ +\-{cls._special_character}0-9]+)) *',
            s)

        if m is None:
            raise ValueError(f"Could not parse {cls.__name__}")

        s = m.group(1)
        if s[0] == '(':
            s = s[1:-1]

        s = s.replace(' ', '')

        m = re.fullmatch(
            rf'([+-]?[0-9]+)([+-]([0-9]*)){cls._special_character}', s)

        if m:
            return cls(int(m[1]), int(m[2]) if m[3] else int(m[2] + '1'))

        try:
            if s[-1] == cls._special_character:
                return cls(0, 1 if len(s) == 1 else int(s[:-1]))

            return cls(int(s))
        except ValueError:
            raise ValueError(f"Could not parse {cls.__name__}")

    def __floordiv__(self: TGEInt, other: TGEInt, /) -> TGEInt:
        numerator = self * other.conj()
        denominator = other.norm()

        return self.__class__(round(numerator._x / denominator),
                              round(numerator._y / denominator))

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self._x}, y={self._y})"

    def __str__(self):
        s1 = str(self._x) if self._x else ''

        if self._y == 0:
            s2 = ''
        elif self._y == 1 or self._y == -1:
            s2 = self._special_character
        else:
            s2 = str(abs(self._y)) + self._special_character

        if not s1 and not s2:
            return '0'

        if not s2:
            return s1

        if not s1:
            return f'{"-" if self._y < 0 else ""}{s2}'

        return f'({s1} {"-" if self._y < 0 else "+"} {s2})'

    def __bool__(self):
        return self._x == 0 == self._y

    @classmethod
    @abstractmethod
    def ramifies(cls, p: int) -> bool:
        ...

    @classmethod
    @abstractmethod
    def is_inert(cls, p: int) -> bool:
        ...

    @classmethod
    @abstractmethod
    def splits(cls, p: int) -> bool:
        ...

    @classmethod
    def factor_type_s(cls: Type[TGEInt], p: int) -> TGEInt:
        """Finds a G/E prime which divides p, given that p splits."""
        ...


class GaussianInteger(GEInteger):
    _special_character = 'i'

    def __mul__(self, other: 'GaussianInteger', /):
        return GaussianInteger(self._x * other._x - self._y * other._y,
                               self._x * other._y + self._y * other._x)

    def conj(self):
        return GaussianInteger(self._x, -self._y)

    @classmethod
    def ramifies(cls, p: int):
        return p == 2

    @classmethod
    def is_inert(cls, p: int):
        return p % 4 == 3

    @classmethod
    def splits(cls, p: int):
        return p % 4 == 1

    @classmethod
    def factor_type_s(cls, p: int):
        ret = cornacchias(1, p)

        assert ret

        x, y = ret
        return GaussianInteger(x, y)


class EisensteinInteger(GEInteger):
    _special_character = 'w'

    def __mul__(self, other: 'EisensteinInteger', /):
        return EisensteinInteger(
            self._x * other._x - self._y * other._y,
            self._x * other._y + self._y * other._x - self._y * other._y)

    def conj(self):
        return EisensteinInteger(self._x - self._y, -self._y)

    @classmethod
    def ramifies(cls, p: int):
        return p == 3

    @classmethod
    def is_inert(cls, p: int):
        return p % 3 == 2

    @classmethod
    def splits(cls, p: int):
        return p % 3 == 1

    @classmethod
    def factor_type_s(cls, p: int):
        ret = cornacchias(3, p)

        assert ret

        x, y = ret
        return EisensteinInteger(x + y, 2 * y)
