import os
import time
from selenium.webdriver.common.by import By
from utils.styles import Color, clear_screen, display_alpha_hack

def parse_invites(driver):
    clear_screen()
    display_alpha_hack()
    print(f"{Color.GREEN}[+] Парсер инвайтов Alpha Date (Sender){Color.END}\n")

    os.makedirs("Invites", exist_ok=True)

    try:
        driver.get("https://alpha.date/sender")
        print(f"{Color.YELLOW}[i] Ожидаем загрузки...{Color.END}")
        time.sleep(5)

        for i in range(1, 13):  # 12 анкет
            try:
                # Получаем имя и возраст
                name_age_xpath = f'//*[@id="root"]/main/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[{i}]/div[1]/div[2]/div[1]'
                name_age_element = driver.find_element(By.XPATH, name_age_xpath)
                name, age = name_age_element.text.split(", ")
                filename = f"Invites/{name.strip()}_{age.strip()}.txt".replace(" ", "_")

                print(f"{Color.YELLOW}[{i}/12] Парсим: {name}, {age}{Color.END}")

                # Кликаем анкету
                profile_xpath = f'//*[@id="root"]/main/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/div[{i}]/div[1]'
                driver.find_element(By.XPATH, profile_xpath).click()
                time.sleep(2)

                # Собираем инвайты
                invites = []
                for j in range(1, 50):  # Проверяем до 50 сообщений
                    try:
                        invite_xpath = f'//*[@id="root"]/main/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[{j}]/div[1]/div[1]'
                        invite = driver.find_element(By.XPATH, invite_xpath)
                        if invite.text.strip() and "Send" not in invite.text:
                            invites.append(invite.text.strip())
                    except:
                        break  # Прерываем цикл, если сообщений больше нет

                # Сохраняем в файл
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("\n".join(invites))

                print(f"{Color.GREEN}[✓] Сохранено: {len(invites)} инвайтов{Color.END}")

            except Exception as e:
                print(f"{Color.RED}[!] Ошибка в анкете #{i}: {str(e)[:50]}...{Color.END}")
                continue

        print(f"\n{Color.CYAN}[+] Все файлы в: {os.path.abspath('Invites')}{Color.END}")

    except Exception as e:
        driver.save_screenshot("error_parser.png")
        print(f"{Color.RED}[!] Критическая ошибка: {e}{Color.END}")

    input(f"\n{Color.YELLOW}[!] Нажмите Enter...{Color.END}")