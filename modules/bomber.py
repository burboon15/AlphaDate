import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.styles import Color, clear_screen, display_alpha_hack

def mass_messaging(driver):
    clear_screen()
    display_alpha_hack()
    print(f"{Color.GREEN}[+] Массовая рассылка Alpha Date{Color.END}\n")

    # 1. Настройка интервала
    interval_min = int(input(f"{Color.YELLOW}[?] Интервал (минуты): {Color.END}"))
    stop_flag = False

    # 2. Основной цикл рассылки
    while not stop_flag:
        try:
            # Переход на страницу
            driver.get("https://alpha.date/chance")
            time.sleep(3)
            
            # Нажимаем кнопку Message
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/main/div/div[2]/div[2]/div[2]/div[1]/div[2]/label[1]'))
            ).click()
            time.sleep(2)

            # Получаем всех видимых мужчин
            men = driver.find_elements(By.XPATH, '//div[contains(@class, "male-profile")]')
            print(f"{Color.GREEN}[✓] Найдено мужчин: {len(men)}{Color.END}")

            for index, man in enumerate(men, 1):
                if stop_flag:
                    break
                    
                try:
                    print(f"{Color.CYAN}[{index}/{len(men)}] Обработка профиля...{Color.END}")
                    
                    # Клик по мужчине (JavaScript для надежности)
                    driver.execute_script("arguments[0].click();", man)
                    time.sleep(2)
                    
                    # Определяем текущую анкету
                    profile_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "current-profile")]'))
                    )
                    profile_name = profile_element.text.split(',')[0].strip()
                    print(f"{Color.YELLOW}[i] Анкета: {profile_name}{Color.END}")
                    
                    # Загружаем инвайты для анкеты
                    file_path = f"Invites/{profile_name}.txt"
                    if not os.path.exists(file_path):
                        print(f"{Color.RED}[!] Файл не найден: {file_path}{Color.END}")
                        continue
                        
                    with open(file_path, "r", encoding="utf-8") as f:
                        invites = [line.strip() for line in f if line.strip()]
                    
                    # Проверяем историю чата
                    chat_history = driver.find_element(By.XPATH, '//div[contains(@class, "message-history")]').text
                    
                    # Отправляем первый непрочитанный инвайт
                    for invite in invites:
                        if invite not in chat_history:
                            textarea = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, '//textarea[contains(@placeholder, "Написать")]'))
                            )
                            send_btn = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, '//button[contains(., "Отправить")]'))
                            )
                            
                            textarea.clear()
                            textarea.send_keys(invite)
                            send_btn.click()
                            print(f"{Color.GREEN}[✓] Отправлено: {invite[:30]}...{Color.END}")
                            time.sleep(3)
                            break
                    else:
                        print(f"{Color.YELLOW}[!] Все инвайты уже отправлены{Color.END}")
                        
                except Exception as e:
                    print(f"{Color.RED}[!] Ошибка: {str(e)[:50]}...{Color.END}")
                    continue

            # Ожидание следующего цикла
            print(f"{Color.CYAN}[i] Следующий цикл через {interval_min} минут{Color.END}")
            time.sleep(interval_min * 60)

        except KeyboardInterrupt:
            stop_flag = True
            print(f"{Color.RED}[!] Ручная остановка{Color.END}")
        except Exception as e:
            print(f"{Color.RED}[!] Ошибка: {e}{Color.END}")
            driver.save_screenshot("error.png")

    print(f"{Color.YELLOW}[!] Работа завершена{Color.END}")