import unittest
import t_three


class TestCourseStatistics(unittest.TestCase):
    """Тесты для вычисления статистики по курсам."""

    def test_courses(self):
        """Параметризованный тест: структура курсов и статистика длительности."""
        cases = [
            # (type, params, description)
            ("length", {}, "длина списка курсов = 4"),
            ("structure", {"index": 0, "title": "Java-разработчик с нуля", "duration": 14},
             "структура курса 0"),
            ("structure", {"index": 1, "title": "Fullstack-разработчик на Python", "duration": 20},
             "структура курса 1"),
            ("structure", {"index": 2, "title": "Python-разработчик с нуля", "duration": 12},
             "структура курса 2"),
            ("structure", {"index": 3, "title": "Frontend-разработчик с нуля", "duration": 20},
             "структура курса 3"),
            ("stat", {"attr": "min_duration", "expected": 12}, "минимальная длительность"),
            ("stat", {"attr": "max_duration", "expected": 20}, "максимальная длительность"),
            ("stat", {"attr": "minis", "expected": [2]}, "индексы коротких курсов"),
            ("stat", {"attr": "maxes", "expected": [1, 3]}, "индексы длинных курсов"),
            ("stat", {"attr": "courses_min", "expected": ["Python-разработчик с нуля"]},
             "названия коротких курсов"),
            ("stat", {"attr": "courses_max",
                      "expected": ["Fullstack-разработчик на Python", "Frontend-разработчик с нуля"]},
             "названия длинных курсов"),
        ]

        for case in cases:
            case_type = case[0]
            description = case[2]

            with self.subTest(msg=description):
                if case_type == "length":
                    self.assertEqual(len(t_three.courses_list), 4)

                elif case_type == "structure":
                    params = case[1]
                    index = params["index"]
                    course = t_three.courses_list[index]
                    self.assertIsInstance(course, dict)
                    self.assertIn("title", course)
                    self.assertIn("mentors", course)
                    self.assertIn("duration", course)
                    self.assertIsInstance(course["mentors"], list)
                    self.assertGreater(len(course["mentors"]), 0)
                    self.assertEqual(course["title"], params["title"])
                    self.assertEqual(course["duration"], params["duration"])

                elif case_type == "stat":
                    params = case[1]
                    actual = getattr(t_three, params["attr"])
                    if params["attr"] == "maxes":
                        self.assertEqual(sorted(actual), sorted(params["expected"]))
                    else:
                        self.assertEqual(actual, params["expected"])
