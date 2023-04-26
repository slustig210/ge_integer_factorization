import unittest

from ge_integers import GaussianInteger, EisensteinInteger


class GEIntegerTests(unittest.TestCase):

    def test_parsing(self):
        expected_solutions: list[tuple[str, int, int]] = [
            ("(i)", 0, 1),
            ("1+i", 1, 1),
            ("-1", -1, 0),
            (" 50 - 12i ", 50, -12),
            ("         (-319312    + 1300139999932i) ", -319312, 1300139999932),
            (" ( - 1    + i ) ", -1, 1),
        ]

        for (s, x, y) in expected_solutions:
            g = GaussianInteger(x, y)
            e = EisensteinInteger(x, y)

            assert GaussianInteger.from_string(s) == g
            assert EisensteinInteger.from_string(s.replace('i', 'w')) == e

            assert GaussianInteger.from_string(str(g)) == g
            assert EisensteinInteger.from_string(str(e)) == e

        should_fail = [
            "x + i",
            "(12 + )",
            " - ",
            "-1 + 2",
            "i + 25",
            "(53 + 12i"
            "   50)      ",
            "--1",
        ]

        for s in should_fail:
            self.assertRaises(ValueError, GaussianInteger.from_string, s)
            self.assertRaises(ValueError, EisensteinInteger.from_string,
                              s.replace('i', 'w'))

        self.assertRaises(ValueError, GaussianInteger.from_string, "2 + 5w")
        self.assertRaises(ValueError, EisensteinInteger.from_string, "2 + 5i")