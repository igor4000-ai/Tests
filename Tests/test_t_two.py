import unittest

from t_two import vote


class TestVote(unittest.TestCase):

    def test_simple_majority(self):
        """Обычный случай: явный победитель."""
        votes = ['Alice', 'Bob', 'Alice', 'Charlie', 'Alice']
        self.assertEqual(vote(votes), 'Alice')

    def test_single_vote(self):
        """Список из одного элемента."""
        self.assertEqual(vote(['Alice']), 'Alice')

    def test_all_same(self):
        """Все голоса за одного кандидата."""
        self.assertEqual(vote([42, 42, 42]), 42)

    def test_tie_first_encountered_wins(self):
        """
        При ничьей функция возвращает того, кто первым достиг максимального
        количества (благодаря сохранению порядка вставки в словаре).
        """
        votes = ['Alice', 'Bob', 'Alice', 'Bob']
        # Оба встречаются по 2 раза. Первый, кто попал в словарь с макс. счётчиком — Alice.
        self.assertEqual(vote(votes), 'Alice')

    def test_tie_different_order(self):
        """Меняем порядок: теперь Bob первый, он и должен выиграть при ничьей."""
        votes = ['Bob', 'Alice', 'Bob', 'Alice']
        self.assertEqual(vote(votes), 'Bob')

    def test_empty_list(self):
        """Пустой список -> возвращает None (нет голосов)."""
        self.assertIsNone(vote([]))

    def test_numbers(self):
        """Работа с числами."""
        self.assertEqual(vote([1, 2, 1, 3, 1]), 1)

    def test_mixed_types(self):
        """Смешанные типы (строка и число)."""
        votes = ['cat', 7, 'cat', 'dog', 7, 'cat']
        self.assertEqual(vote(votes), 'cat')

    def test_long_list(self):
        """Длинный список с явным лидером."""
        votes = ['x'] * 100 + ['y'] * 99
        self.assertEqual(vote(votes), 'x')