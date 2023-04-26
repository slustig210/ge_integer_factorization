import unittest
import gzip
from pathlib import Path

from sieve import generate_primes, extend_primes, DEFAULT_EXTEND_PRIMES


class InternetPrimesTests(unittest.TestCase):
    # https://www.mathematical.com/primes0to1000k.html
    def setUp(self):
        self.internet_primes: list[int] = []

        with gzip.open(Path(__file__).parent.joinpath('prime_numbers.gz')) as f:
            while f._checkClosed:
                val = f.read(4)
                if not val:
                    break
                self.internet_primes.append(int.from_bytes(val, 'little'))

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