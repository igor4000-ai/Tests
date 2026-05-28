import os
import unittest
import requests
from dotenv import load_dotenv
load_dotenv()

class TestYandexDiskAPI(unittest.TestCase):
    BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"
    TOKEN = os.getenv("YA_TOKEN")
    HEADERS = {"Authorization": f"OAuth {TOKEN}"}
    FOLDER = "test_api_folder"

    def setUp(self):
        """Перед каждым тестом удаляем папку, если она осталась с прошлого запуска."""
        if self.TOKEN:
            url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"  # URL-кодируем путь
            requests.delete(url, headers=self.HEADERS)      # удаляем папку (игнорируем ответ)

    def tearDown(self):
        """После теста также удаляем папку."""
        if self.TOKEN:
            url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
            requests.delete(url, headers=self.HEADERS)

    def test_create_folder_success(self):
        """Позитивный тест: создание папки и проверка её появления в списке файлов."""
        if not self.TOKEN:
            self.skipTest("YA_TOKEN не задан")

        # 1. Создаём папку (PUT)
        put_url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
        response = requests.put(put_url, headers=self.HEADERS)
        # API возвращает 201 Created при успешном создании новой папки
        self.assertEqual(response.status_code, 201, f"Не удалось создать папку: {response.text}")

        # 2. Проверяем, что папка существует (GET ресурс)
        check_url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
        response = requests.get(check_url, headers=self.HEADERS)
        self.assertEqual(response.status_code, 200, f"Папка не найдена после создания: {response.text}")

        # Проверяем, что это именно папка
        data = response.json()
        self.assertEqual(data.get("type"), "dir", "Созданный ресурс не является папкой")

    def test_create_folder_unauthorized(self):
        """Отрицательный тест: запрос без токена должен вернуть 401."""
        url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
        response = requests.put(url)  # без заголовка Authorization
        self.assertEqual(response.status_code, 401,
                         f"Ожидался 401 Unauthorized, получен {response.status_code}")

    def test_create_folder_conflict(self):
        """Отрицательный тест: повторное создание той же папки вызывает 409 Conflict."""
        if not self.TOKEN:
            self.skipTest("YA_TOKEN не задан")

        url = f"{self.BASE_URL}?path=%2F{self.FOLDER}"
        # Первое создание – успех (201)
        first = requests.put(url, headers=self.HEADERS)
        self.assertEqual(first.status_code, 201, "Ошибка при первом создании папки")
        # Второе создание – конфликт (409)
        second = requests.put(url, headers=self.HEADERS)
        self.assertEqual(second.status_code, 409,
                         f"Ожидался 409 Conflict, получен {second.status_code}")

    def test_invalid_path(self):
        """Отрицательный тест: пустой путь (или другие недопустимые символы) – 400."""
        if not self.TOKEN:
            self.skipTest("YA_TOKEN не задан")

        url = f"{self.BASE_URL}?path="  # пустой параметр path
        response = requests.put(url, headers=self.HEADERS)
        self.assertEqual(response.status_code, 400,
                         f"Ожидался 400 Bad Request, получен {response.status_code}")

if __name__ == "__main__":
    unittest.main()