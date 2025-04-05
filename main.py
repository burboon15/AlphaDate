import os
import time
from enum import Enum
from getpass import getpass
from auth import AlphaDateAuth
from utils.styles import Color, display_alpha_hack, clear_screen
from modules.invites import parse_invites
from modules.bomber import mass_messaging  # Добавлен импорт новой функции

class MenuOption(Enum):
    INVITE_PARSER = 1
    MESSAGE_BOMBER = 2
    PHOTO_DOWNLOADER = 3
    AUTO_REGISTER = 4
    STATS_ANALYZER = 5
    RESET_ACCOUNT = 6
    EXIT = 0

def show_menu(username):
    print(f"\n{Color.BOLD}Главное меню (пользователь: {username}):{Color.END}")
    print(f"{Color.CYAN}[{MenuOption.INVITE_PARSER.value}] {Color.END}Парсер инвайтов")
    print(f"{Color.CYAN}[{MenuOption.MESSAGE_BOMBER.value}] {Color.END}Массовая рассылка")
    print(f"{Color.CYAN}[{MenuOption.PHOTO_DOWNLOADER.value}] {Color.END}В разработке")
    print(f"{Color.CYAN}[{MenuOption.AUTO_REGISTER.value}] {Color.END}В разработке")
    print(f"{Color.CYAN}[{MenuOption.STATS_ANALYZER.value}] {Color.END}В разработке")
    print(f"{Color.YELLOW}[{MenuOption.RESET_ACCOUNT.value}] {Color.END}Сменить аккаунт")
    print(f"{Color.RED}[{MenuOption.EXIT.value}] {Color.END}Выход\n")

def main():
    auth = AlphaDateAuth()
    saved_data = auth.ask_to_use_saved()
    
    if saved_data:
        username, password = saved_data["username"], saved_data["password"]
    else:
        clear_screen()
        display_alpha_hack()
        print(f"{Color.YELLOW}\n[!] Введите данные от Alpha Date{Color.END}")
        username = input(f"{Color.CYAN}[?] Логин: {Color.END}").strip()
        password = getpass(f"{Color.CYAN}[?] Пароль: {Color.END}").strip()
    
    if not auth.start_browser():
        return
    
    if not auth.login(username, password):
        print(f"{Color.RED}[!] Не удалось войти.{Color.END}")
        auth.close()
        time.sleep(3)
        return
    
    while True:
        try:
            clear_screen()
            display_alpha_hack()
            show_menu(username)
            
            choice = input(f"{Color.YELLOW}> Выберите опцию: {Color.END}").strip()
            
            if choice == str(MenuOption.INVITE_PARSER.value):
                parse_invites(auth.driver)
                
            elif choice == str(MenuOption.MESSAGE_BOMBER.value):
                mass_messaging(auth.driver)  # Теперь используем новую функцию
                
            elif choice == str(MenuOption.PHOTO_DOWNLOADER.value):
                clear_screen()
                display_alpha_hack()
                print(f"\n{Color.GREEN}[+] Загрузчик фото...{Color.END}")
                time.sleep(2)
                input(f"\n{Color.CYAN}[?] Нажмите Enter, чтобы вернуться в меню...{Color.END}")
                
            elif choice == str(MenuOption.RESET_ACCOUNT.value):
                auth.secure_config.clear_credentials()
                print(f"\n{Color.YELLOW}[!] Данные удалены. Перезапустите скрипт.{Color.END}")
                auth.close()
                time.sleep(3)
                break
                
            elif choice == str(MenuOption.EXIT.value):
                print(f"\n{Color.RED}[!] Выход...{Color.END}")
                auth.close()
                break
                
            else:
                print(f"\n{Color.RED}[!] Неверный выбор!{Color.END}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{Color.RED}[!] Принудительный выход...{Color.END}")
            auth.close()
            break

if __name__ == "__main__":
    main()