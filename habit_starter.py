
import os 
import sys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime

def message_print(message): 
    message_highlights= '*' * len(message)
    message = f'\n{message_highlights}\n{message}\n{message_highlights}\n'
    return message


def habit_starter(chrome_driver_load, folder_root, ACTIONS): 
    download_folder= os.path.join(folder_root, "Downloads")
    driver = chrome_driver_load(download_folder)
    timeout = 10

    for url, steps in ACTIONS.items():
        print(f"\n🔗 Navegando a {message_print(url)}")
        driver.get(url)

        try:
            for idx, step in enumerate(steps, start=1):
                by   = step["by"]
                loc  = step["locator"]
                typ  = step["type"]
                print(f"  → Paso {idx}: {typ} en {loc}")

                # use element_to_be_clickable for both click and send_keys
                elem = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by, loc))
                )

                if typ == "click":
                    elem.click()
                    print(f"    ✓ Clicked {loc}")

                elif typ == "send_keys":
                    # click once to focus, then clear and send
                    elem.click()
                    elem.clear()
                    elem.send_keys(step["value"])
                    print(f"    ✓ Sent keys (‘{step['value']}’) to {loc}")

                else:
                    raise ValueError(f"Tipo desconocido: {typ}")

        except TimeoutException as e:
            print(f"    ✗ Timeout en paso {idx} ({typ} @ {loc}): {e}")           
    input(message_print("Presina enter para cerrar el navegador"))
    driver.quit()

if __name__ == "__main__":
    if sys.platform == "darwin":
        folder_root = r"/Users/armjorge/Library/CloudStorage/GoogleDrive-armjorge@gmail.com/My Drive/Projects/habit_starter"
    elif sys.platform.startswith("win"):
        folder_root = r"C:\Users\arman\Documents\habit_starter"
    else:
        raise RuntimeError(f"Unsupported platform: {sys.platform}")
    # 1) Añade al path la carpeta donde está df_multi_match.py
    libs_dir = os.path.join(folder_root, "Library")
    sys.path.insert(0, libs_dir)

    # 2) Ahora importa la función directamente
    from chrome_driver_load import load_chrome
    ACTIONS = {
    "https://tec-csm.symplicity.com/": [
        {"type": "click",     "by": By.XPATH, "locator": '//*[@id="wherechoices"]/a[1]/span'},
        {"type": "send_keys", "by": By.XPATH, "locator": '//*[@id="Ecom_User_ID"]',    "value": "A01793646"},
        {"type": "send_keys", "by": By.XPATH, "locator": '//*[@id="Ecom_Password"]',     "value": "Endeavor1$"},
        {"type": "click",     "by": By.XPATH, "locator": '//*[@id="submitButton"]'},
    ],}
    # 3) Llama a tu función pasándola como parámetro
    habit_starter(load_chrome, folder_root, ACTIONS)
    