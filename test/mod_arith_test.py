import unittest
import random

from sympy import jacobi_symbol
from mod_arith import jacobi_symbol as my_jacobi_symbols, modular_pow


class ModularArithmeticTests(unittest.TestCase):

    def test_modular_pow(self):

        def quick_pow_test(x, y, m):
            assert modular_pow(x, y, m) == pow(x, y, m), f"pow({x}, {y}, {m})"

        for _ in range(1000):
            x = random.randint(0, 30000)
            y = random.randint(0, 30000)
            m = random.randint(1, 30000)
            quick_pow_test(x, y, m)

        x = random.randint(0, 30000)
        m = random.randint(2, 30000)
        quick_pow_test(x, 0, m)

        m = random.randint(2, 30000)
        quick_pow_test(1, 0, m)

        for _ in range(100):
            y = random.randint(0, 30000)
            m = random.randint(1, 30000)
            quick_pow_test(1, y, m)
