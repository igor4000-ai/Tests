import unittest
import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Загружаем переменные окружения из файла .env
load_dotenv()


class TestYandexAuth(unittest.TestCase):
    """
    UI-тест для проверки авторизации на Яндексе с использованием данных из .env
    """

    def setUp(self):
        # Получаем данные из переменных окружения
        self.login = os.getenv('YA_TEST_LOGIN')
        self.password = os.getenv('YA_TEST_PASSWORD')
        self.token = os.getenv('YA_TOKEN')  # Если понадобится в будущем

        # Проверка, что данные загрузились
        if not self.login or not self.password:
            raise ValueError("Логин или пароль не найдены в файле .env")

        # Настройка драйвера
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Закомментировано для визуального режима
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        service = Service("/usr/bin/chromedriver")
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.actions = ActionChains(self.driver)

    def tearDown(self):
        """Закрываем браузер после каждого теста."""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    def _hide_webdriver_signs(self):
        """Убираем признаки автоматизации после загрузки страницы."""
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => false});"
        )
        self.driver.execute_script("window.navigator.chrome = {runtime: {}};")
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru']});"
        )
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});"
        )

    def _find_element_by_selectors(self, selectors, condition=EC.element_to_be_clickable, timeout=None):
        """
        Перебирает список селекторов и возвращает первый найденный элемент.

        :param selectors: список кортежей (By, selector_string)
        :param condition: ожидаемое условие из EC (по умолчанию element_to_be_clickable)
        :param timeout: неявное время ожидания в секундах (если None — используется стандартное из self.wait)
        :return: найденный WebElement или None
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        for by, selector in selectors:
            try:
                element = wait.until(condition((by, selector)))
                print(f"  -> Найден элемент по селектору: {by}={selector}")
                return element
            except Exception as e:
                print(f"  -> Селектор {by}={selector} не найден: {e}")
        return None

    def test_login_via_more_button(self):
        """Тест сценария: Вход по логину и паролю."""
        driver = self.driver

        # === ШАГ 1: Открываем страницу авторизации ===
        print("\n=== ШАГ 1: Открытие страницы авторизации ===")
        driver.get("https://passport.yandex.ru/auth/")
        time.sleep(2)

        # Убираем признаки автоматизации
        self._hide_webdriver_signs()

        # === ШАГ 2: Ищем кнопку выбора метода входа ===
        print("\n=== ШАГ 2: Выбор метода входа ===")
        try:
            method_button_selectors = [
                (By.XPATH, "//button[contains(text(), 'Другие способы входа')]"),
                (By.XPATH, "//button[contains(text(), 'Ещё')]"),
                (By.XPATH, "//button[contains(@class, 'more')]"),
                (By.XPATH, "//button[contains(@class, 'dropdown')]"),
                (By.XPATH, "//button[@data-t='button:more']"),
            ]
            method_button = self._find_element_by_selectors(method_button_selectors)

            if method_button:
                driver.execute_script("arguments[0].click();", method_button)
                print("  -> Кнопка выбора метода входа нажата.")
                time.sleep(1)

                # Ждём появления пункта "Войти по логину" в выпадающем меню
                print("  -> Поиск пункта 'Войти по логину' в меню...")

                menu_item = self._find_element_by_selectors([
                    (By.XPATH, "//div[@data-testid='menu-option-switchToLogin']"),
                    (By.XPATH, "//span[contains(text(), 'Войти по логину')]/ancestor::div[@role='menuitem']"),
                    (By.XPATH, "//div[contains(@class, 'menu')]//div[contains(text(), 'логину')]"),
                ], timeout=5)

                if menu_item:
                    driver.execute_script("arguments[0].scrollIntoView(true);", menu_item)
                    # Визуальное выделение элемента перед кликом (для отладки)
                    driver.execute_script(
                        "arguments[0].style.border='3px solid red';"
                        "arguments[0].style.backgroundColor='yellow';",
                        menu_item
                    )
                    location = menu_item.location
                    size = menu_item.size
                    print(f"  -> Координаты элемента: {location}, размер: {size}")

                    self.actions.move_to_element(menu_item).click().perform()
                    print("  -> Опция 'Войти по логину' выбрана.")
                    time.sleep(1.5)
                else:
                    print("  -> Пункт 'Войти по логину' не найден, продолжаем с текущей формой.")
            else:
                print("  -> Кнопка выбора метода входа не найдена, продолжаем с основной формой.")
        except Exception as e:
            print(f"  -> Ошибка при выборе метода входа: {e}")
            print("  -> Продолжаем с основной формой входа.")

        # === ШАГ 3: Ввод логина ===
        print("\n=== ШАГ 3: Ввод логина ===")
        print(f"  -> Текущий URL: {driver.current_url}")
        print(f"  -> Заголовок страницы: {driver.title}")

        login_selectors = [
            (By.XPATH, "//input[@data-testid='text-field-input' and @aria-label='Логин или email']"),
            (By.XPATH, "//input[@placeholder='Логин или email']"),
            (By.XPATH, "//input[@type='text' and contains(@class, 'ya_')]"),
            (By.ID, "passp-field-login"),
            (By.NAME, "login"),
            (By.CSS_SELECTOR, "input[type='text']"),
        ]
        login_input = self._find_element_by_selectors(
            login_selectors, condition=EC.presence_of_element_located
        )

        if not login_input:
            print("  -> Поле ввода логина не найдено. HTML страницы:")
            print(driver.page_source)
            self.fail("Не удалось найти поле ввода логина")

        # Кликаем, фокусируемся, вводим логин
        self.actions.move_to_element(login_input).click().perform()
        time.sleep(0.5)
        login_input.clear()
        for char in self.login:
            login_input.send_keys(char)
            time.sleep(0.05)
        print(f"  -> Логин введён: {self.login}")

        # Нажимаем кнопку "Войти" (переход к следующему шагу — вводу пароля)
        print("  -> Поиск кнопки подтверждения логина...")
        login_submit_selectors = [
            (By.XPATH, "//button[@data-testid='split-add-user-next-login']"),
            (By.XPATH, "//button[.//span[text()='Войти']]"),
            (By.XPATH, "//button[contains(text(), 'Войти')]"),
            (By.XPATH, "//button[@type='submit']"),
            (By.ID, "passp:sign-in"),
        ]
        login_submit_button = self._find_element_by_selectors(login_submit_selectors)

        if not login_submit_button:
            # Попробуем найти любую кнопку отправки
            login_submit_button = self._find_element_by_selectors([
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(@class, 'button')]"),
            ])

        if not login_submit_button:
            self.fail("Не удалось найти кнопку подтверждения логина")

        driver.execute_script("arguments[0].click();", login_submit_button)
        print("  -> Кнопка подтверждения логина нажата.")
        time.sleep(2)

        # Если появилась кнопка "Войти с паролем" — нажимаем её
        print("  -> Проверка наличия кнопки 'Войти с паролем'...")
        password_method_selectors = [
            (By.XPATH, "//button[@data-testid='split-add-user-submit-password']"),
            (By.XPATH, "//button[.//span[text()='Войти с паролем']]"),
            (By.XPATH, "//span[text()='Войти с паролем']/ancestor::button"),
            (By.XPATH, "//button[.//span[contains(text(), 'паролем')]]"),
        ]
        password_method_button = self._find_element_by_selectors(
            password_method_selectors, timeout=5
        )
        if password_method_button:
            driver.execute_script("arguments[0].click();", password_method_button)
            print("  -> Нажали кнопку 'Войти с паролем'.")
            time.sleep(1.5)
        else:
            print("  -> Кнопка 'Войти с паролем' не появилась, продолжаем.")

        # === ШАГ 4: Ввод пароля ===
        print("\n=== ШАГ 4: Ввод пароля ===")
        password_selectors = [
            (By.XPATH, "//input[@data-testid='text-field-input' and @aria-label='Пароль']"),
            (By.XPATH, "//input[@placeholder='Пароль']"),
            (By.ID, "passp-field-passwd"),
            (By.NAME, "passwd"),
            (By.XPATH, "//input[@type='password']"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ]
        password_input = self._find_element_by_selectors(
            password_selectors, condition=EC.presence_of_element_located
        )

        if not password_input:
            print("  -> Поле ввода пароля не найдено. HTML страницы:")
            print(driver.page_source)
            self.fail("Не удалось найти поле ввода пароля")

        self.actions.move_to_element(password_input).click().perform()
        time.sleep(0.5)
        password_input.clear()
        for char in self.password:
            password_input.send_keys(char)
            time.sleep(0.05)
        print("  -> Пароль введён.")

        # === ШАГ 4.5: Нажимаем кнопку "Далее" ===
        print("\n=== ШАГ 4.5: Нажатие кнопки 'Далее' ===")
        next_button_selectors = [
            (By.XPATH, "//button[.//span[text()='Далее']]"),
            (By.XPATH, "//button[contains(text(), 'Далее')]"),
            (By.XPATH, "//button[contains(@class, 'next')]"),
            (By.XPATH, "//button[@data-testid='next-button']"),
        ]
        next_button = self._find_element_by_selectors(next_button_selectors, timeout=5)

        if next_button:
            driver.execute_script("arguments[0].click();", next_button)
            print("  -> Кнопка 'Далее' нажата.")
            time.sleep(2)
        else:
            print("  -> Кнопка 'Далее' не найдена, продолжаем.")

        # Нажимаем финальную кнопку "Войти"
        print("  -> Поиск кнопки отправки пароля...")
        password_submit_selectors = [
            (By.XPATH, "//button[@data-testid='split-add-user-submit-password']"),
            (By.XPATH, "//button[.//span[text()='Войти']]"),
            (By.XPATH, "//button[contains(text(), 'Войти')]"),
            (By.XPATH, "//button[@type='submit']"),
            (By.ID, "passp:sign-in"),
        ]
        password_submit_button = self._find_element_by_selectors(password_submit_selectors)

        if not password_submit_button:
            self.fail("Не удалось найти кнопку отправки пароля")

        driver.execute_script("arguments[0].click();", password_submit_button)
        print("  -> Кнопка отправки пароля нажата.")
        time.sleep(3)

        # === ШАГ 5: Проверка успешной авторизации ===
        print("\n=== ШАГ 5: Проверка успешной авторизации ===")
        current_url = driver.current_url
        print(f"  -> Текущий URL: {current_url}")

        # Проверяем, что произошёл редирект со страницы авторизации
        auth_urls = [
            "passport.yandex.ru/auth",
            "passport.yandex.ru/registration",
        ]
        is_auth_page = any(auth_url in current_url for auth_url in auth_urls)

        if is_auth_page:
            # Возможно, запрашивают 2FA — проверяем
            print("  -> Всё ещё на странице авторизации, проверяем наличие запроса 2FA...")

            # Проверяем, есть ли запрос кода подтверждения (SMS, push, TOTP)
            twofa_indicators = [
                "//input[contains(@aria-label, 'код')]",
                "//input[contains(@placeholder, 'код')]",
                "//div[contains(text(), 'код подтверждения')]",
                "//div[contains(text(), 'подтвердите')]",
                "//div[contains(text(), 'введите код')]",
                "//input[@data-testid='text-field-input']",
            ]
            twofa_found = self._find_element_by_selectors(
                [(By.XPATH, sel) for sel in twofa_indicators],
                condition=EC.presence_of_element_located,
                timeout=3
            )
            if twofa_found:
                print("  -> Обнаружен запрос 2FA (код подтверждения).")
                print("  -> Для завершения авторизации необходим ввод кода (тест остановлен).")
                self.skipTest("Требуется двухфакторная аутентификация — автоматический ввод кода не поддерживается")

            # Проверяем наличие ошибок
            error_indicators = [
                "//div[contains(@class, 'error')]",
                "//div[contains(@data-testid, 'error')]",
                "//span[contains(@class, 'error')]",
            ]
            error_element = self._find_element_by_selectors(
                [(By.XPATH, sel) for sel in error_indicators],
                condition=EC.presence_of_element_located,
                timeout=3
            )
            if error_element:
                error_text = error_element.text
                print(f"  -> Обнаружена ошибка на странице: {error_text}")
                self.fail(f"Ошибка авторизации: {error_text}")

            self.fail("Авторизация не удалась — остаёмся на странице авторизации")

        # Успешная авторизация: редирект прошёл
        print(f"  -> Редирект выполнен успешно: {current_url}")
        self.assertNotIn("passport.yandex.ru/auth", current_url,
                          "Авторизация не удалась — всё ещё на странице входа")
        print("  -> ТЕСТ ПРОЙДЕН: Авторизация успешна!")


if __name__ == '__main__':
    unittest.main(verbosity=2)