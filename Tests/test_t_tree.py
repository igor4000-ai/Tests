import unittest
import t_three

class TestCourseStatistics(unittest.TestCase):
    """Тесты для вычисления статистики по курсам."""

    def test_courses_list_length(self):
        """Список курсов должен содержать 4 элемента."""
        self.assertEqual(len(t_three.courses_list), 4)

    def test_courses_list_structure(self):
        """Каждый элемент — словарь с ключами 'title', 'mentors', 'duration'."""
        for course in t_three.courses_list:
            self.assertIn("title", course)
            self.assertIn("mentors", course)
            self.assertIn("duration", course)
            self.assertIsInstance(course["mentors"], list)

    def test_min_max_durations(self):
        """Минимальная длительность: 12, максимальная: 20."""
        self.assertEqual(t_three.min_duration, 12)
        self.assertEqual(t_three.max_duration, 20)

    def test_minis_indices(self):
        """Индекс курса с минимальной длительностью: [2]."""
        self.assertEqual(t_three.minis, [2])

    def test_maxes_indices(self):
        """Индексы курсов с максимальной длительностью: [1, 3]."""
        self.assertEqual(sorted(t_three.maxes), [1, 3])

    def test_courses_min_names(self):
        """Названия самых коротких курсов: ['Python-разработчик с нуля']."""
        self.assertEqual(
            t_three.courses_min,
            ["Python-разработчик с нуля"]
        )

    def test_courses_max_names(self):
        """Названия самых длинных курсов: два курса по 20 недель."""
        expected = [
            "Fullstack-разработчик на Python",
            "Frontend-разработчик с нуля"
        ]
        self.assertEqual(t_three.courses_max, expected)