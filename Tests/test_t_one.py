import unittest

from t_one import discriminant


class TestDiscriminant(unittest.TestCase):

    def test_two_roots(self):
        """Уравнение  два корня"""
        result = discriminant(1, -3, 2)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertEqual(result, (2.0, 1.0))

    def test_one_root(self):
        """Уравнение один корень"""
        result = discriminant(1, -2, 1)
        self.assertIsInstance(result, float)
        self.assertEqual(result, 1.0)

    def test_no_roots(self):
        """Уравнение корней нет"""
        result = discriminant(1, 1, 1)
        self.assertEqual(result, 'корней нет')