import unittest
from t_two import vote


class TestVote(unittest.TestCase):

    def test_vote(self):
        """Параметризованный тест функции vote."""
        cases = [
            (['Alice', 'Bob', 'Alice', 'Charlie', 'Alice'], 'Alice', "обычное большинство"),
            (['Alice'], 'Alice', "один голос"),
            ([42, 42, 42], 42, "все голоса за одного кандидата"),
            (['Alice', 'Bob', 'Alice', 'Bob'], 'Alice', "ничья: первый в словаре побеждает"),
            (['Bob', 'Alice', 'Bob', 'Alice'], 'Bob', "ничья: другой порядок — другой победитель"),
            ([], None, "пустой список — None"),
            ([1, 2, 1, 3, 1], 1, "числа"),
            (['cat', 7, 'cat', 'dog', 7, 'cat'], 'cat', "смешанные типы"),
            (['x'] * 100 + ['y'] * 99, 'x', "длинный список с явным лидером"),
        ]

        for votes, expected, description in cases:
            with self.subTest(msg=description):
                result = vote(votes)
                self.assertEqual(result, expected)
