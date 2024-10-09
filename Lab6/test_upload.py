from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Налаштування WebDriver для Chrome
driver = webdriver.Firefox()  # Замість webdriver.Chrome()

# Перехід на сторінку для завантаження файлів
driver.get('https://the-internet.herokuapp.com/upload')

# Знаходимо елемент для вибору файлу
file_input = driver.find_element(By.ID, 'file-upload')

# Файл, який потрібно завантажити
file_path = os.path.abspath("test_file.txt")
file_input.send_keys(file_path)

# Знаходимо кнопку для відправлення форми
upload_button = driver.find_element(By.ID, 'file-submit')
upload_button.click()

# Очікування 2 секунди для завантаження сторінки
time.sleep(2)

# Перевірка наявності повідомлення про успішне завантаження
success_message = driver.find_element(By.TAG_NAME, 'h3')
assert 'File Uploaded!' in success_message.text

# Закриття браузера
driver.quit()
