import unittest
from sieve import generate_primes, extend_primes, DEFAULT_EXTEND_PRIMES

from pathlib import Path


class InternetPrimesTests(unittest.TestCase):
    # https://www.mathematical.com/primes0to1000k.html
    def setUp(self):
        self.internet_primes: list[int] = []

        with open(Path(__file__).parent.joinpath('prime_numbers.txt')) as f:
            # some lines end in a newline in the middle of a number!
            carry = ''

            for line in f:
                if line == '\n':
                    continue

                numbers = [s for s in line.rstrip().split(",") if s]
                if carry:
                    numbers[0] = carry + numbers[0]

                if line[-2] != ',':
                    carry = numbers[-1]
                    numbers.pop()
                else:
                    carry = ''

                self.internet_primes.extend(int(s) for s in numbers)

            if carry:
                self.internet_primes.append(int(carry))

    def test_sieve_matches_expected(self):
        my_primes = generate_primes(self.internet_primes[-1])

        # for i, j in zip(internet_primes, my_primes):
        #     assert i == j, f"expected {i} from internet primes, {j} from my_primes was found"

        assert self.internet_primes == my_primes

    def test_extend_primes(self):
        primes: list[int] = []

        extend_primes(primes)

        i = self.internet_primes.index(primes[-1])

        assert i == len(primes) - 1

        assert self.internet_primes[len(primes)] >= DEFAULT_EXTEND_PRIMES

        assert self.internet_primes[:len(primes)] == primes

        for _ in range(5):
            extend_primes(primes)
            assert self.internet_primes[:len(primes)] == primes

        extend_primes(primes, 50000)
        assert self.internet_primes[:len(primes)] == primes

        extend_primes(primes, 531203)
        assert self.internet_primes[:len(primes)] == primes


class BasicSieveTests(unittest.TestCase):

    def test_extend_primes_edge_cases(self):
        primes: list[int] = []

        self.assertRaises(ValueError, extend_primes, primes, 1)

        assert primes == []

        extend_primes(primes, 2)
        assert primes == [2]

        extend_primes(primes, 2)
        assert primes == [2]

        extend_primes(primes, 3)
        assert primes == [2, 3]

        primes.pop()
        extend_primes(primes)
        assert primes == [2, 3]