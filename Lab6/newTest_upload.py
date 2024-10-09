from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Функція для налаштування драйвера
def get_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument('--headless')  # Режим без інтерфейсу
    driver = webdriver.Chrome(options=options)
    return driver

# Функція для тесту завантаження файлу
def test_file_upload(driver):
    try:
        driver.get('https://the-internet.herokuapp.com/upload')

        # Знаходимо елемент для вибору файлу
        file_input = driver.find_element(By.ID, 'file-upload')

        # Файлу, який потрібно завантажити
        file_path = os.path.abspath("test_file.txt")
        file_input.send_keys(file_path)

        # Знаходимо кнопку для відправлення форми
        upload_button = driver.find_element(By.ID, 'file-submit')
        upload_button.click()

        # Очікування наявності повідомлення про успішне завантаження
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h3'))
        )

        # Перевірка наявності повідомлення про успішне завантаження
        success_message = driver.find_element(By.TAG_NAME, 'h3')
        assert 'File Uploaded!' in success_message.text
        print("Тест пройшов успішно: файл завантажено!")

    except Exception as e:
        print(f"Помилка при виконанні тесту: {e}")

# Головна функція для виконання тесту
def main():
    driver = None
    try:
        driver = get_driver(headless=True)
        test_file_upload(driver)

    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()
