import unittest
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class TestYandexDiskAPI(unittest.TestCase):
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = os.getenv("YA_TOKEN")
    HEADERS = {"Authorization": f"OAuth {TOKEN}"}
    FOLDER = "test_api_folder"

    def setUp(self):
        if self.TOKEN:
            url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
            requests.delete(url, headers=self.HEADERS)

    def tearDown(self):
        if self.TOKEN:
            url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
            requests.delete(url, headers=self.HEADERS)

    def test_create_folder(self):
        """Параметризованный тест: создание папки на Яндекс.Диске."""
        cases = [
            (
                "success",
                f"{self.BASE_URL}?path=%2F{self.FOLDER}",
                self.HEADERS,
                True,
                "позитивный: создание папки",
            ),
            (
                "unauthorized",
                f"{self.BASE_URL}?path=%2F{self.FOLDER}",
                None,
                False,
                "отрицательный: без токена — 401",
            ),
            (
                "conflict",
                f"{self.BASE_URL}?path=%2F{self.FOLDER}",
                self.HEADERS,
                False,
                "отрицательный: повторное создание — 409",
            ),
            (
                "invalid_path",
                f"{self.BASE_URL}?path=",
                self.HEADERS,
                False,
                "отрицательный: пустой путь — 400",
            ),
        ]

        for case_type, url, headers, expect_success, description in cases:
            with self.subTest(msg=description):
                if not self.TOKEN and headers:
                    self.skipTest("YA_TOKEN не задан")

                headers = headers or {}

                # Для конфликта сначала создаём папку
                if case_type == "conflict":
                    requests.put(url, headers=self.HEADERS)

                response = requests.put(url, headers=headers)

                # Проверка статуса через response.ok
                if expect_success:
                    self.assertTrue(response.ok,
                                    f"Папка не создана: {response.status_code} {response.text}")

                    # Проверяем, что папка появилась в списке
                    check_url = f"{self.BASE_URL}?path=%2F"
                    check_response = requests.get(check_url, headers=self.HEADERS)
                    self.assertTrue(check_response.ok,
                                    f"Не удалось получить список файлов: {check_response.status_code}")
                    files = check_response.json()["_embedded"]["items"]
                    self.assertTrue(
                        any(f["name"] == self.FOLDER for f in files),
                        "Папка не найдена в списке файлов",
                    )
                else:
                    self.assertFalse(response.ok,
                                     f"Ожидалась ошибка, но запрос успешен: {response.status_code}")


if __name__ == "__main__":
    unittest.main()
