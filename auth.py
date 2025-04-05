from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import SecureConfig
from utils.styles import Color, display_alpha_hack  # Перенесено из utils/styles.py
import time  # Добавлен отсутствующий импорт
import os  # Добавлен для clear_screen()

class AlphaDateAuth:
    def __init__(self):
        self.driver = None
        self.secure_config = SecureConfig()

    def ask_to_use_saved(self):
        saved = self.secure_config.load_credentials()
        if not saved:
            return None
        
        print(f"{Color.GREEN}[+] Найден сохранённый аккаунт: {saved['username']}{Color.END}")
        choice = input(f"{Color.YELLOW}[?] Использовать его? (Y/N): {Color.END}").strip().lower()
        
        if choice == "y":
            return saved
        elif choice == "n":
            self.secure_config.clear_credentials()
            print(f"{Color.RED}[!] Данные удалены.{Color.END}")
            return None
        else:
            print(f"{Color.RED}[!] Неверный выбор. Данные не загружены.{Color.END}")
            return None

    def start_browser(self):
        print(f"{Color.YELLOW}\n[!] Запуск браузера...{Color.END}")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-notifications")
            options.add_argument("--no-default-browser-check")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--app=https://alpha.date/login")
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            
            if "data:," in self.driver.current_url:
                self.driver.get("https://alpha.date/login")
                
            self.driver.maximize_window()
            return True
        except Exception as e:
            print(f"{Color.RED}[!] Ошибка запуска браузера: {e}{Color.END}")
            return False

    def login(self, username, password):
        try:
            if "alpha.date" not in self.driver.current_url:
                self.driver.get("https://alpha.date/login")
            
            print(f"{Color.CYAN}[+] Вход в систему...{Color.END}")
            time.sleep(2)
            
            login_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/form/div[1]/input')
            login_field.clear()
            login_field.send_keys(username)
            
            password_field = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/form/div[2]/input')
            password_field.clear()
            password_field.send_keys(password)
            
            self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/form/button').click()
            time.sleep(3)
            
            if "error" in self.driver.page_source.lower():
                print(f"{Color.RED}[!] Ошибка входа!{Color.END}")
                return False
            
            self.secure_config.save_credentials(username, password)
            return True
            
        except Exception as e:
            print(f"{Color.RED}[!] Ошибка авторизации: {e}{Color.END}")
            return False

    def close(self):
        if self.driver:
            self.driver.quit()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')