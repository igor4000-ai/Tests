import unittest
from t_one import discriminant


class TestDiscriminant(unittest.TestCase):

    def test_discriminant(self):
        """Параметризованный тест функции discriminant."""
        cases = [
            (1, -3, 2, (2.0, 1.0), "два корня"),
            (1, -2, 1, 1.0, "один корень"),
            (1, 1, 1, 'корней нет', "корней нет"),
            (2, -8, 8, 2.0, "один корень (кратный)"),
            (1, -5, 6, (3.0, 2.0), "два корня (целые)"),
            (1, 0, -1, (1.0, -1.0), "два корня (b=0)"),
        ]

        for a, b, c, expected, description in cases:
            with self.subTest(msg=description):
                result = discriminant(a, b, c)
                self.assertEqual(result, expected)
