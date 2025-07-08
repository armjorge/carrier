
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

def habit_starter(chrome_driver_load, folder_root): 
    download_folder= os.path.join(folder_root, "Downloads")

    driver = chrome_driver_load(download_folder)
    message_simplicity = "Primer objetivo: cargar mi perfil en simplicity"
    print(message_print(message_simplicity))
    driver.get("https://tec-csm.symplicity.com/")
    exatec_xpath = '//*[@id="wherechoices"]/a[1]/span'
    try:
        # 1) Espera y click en Exatec
        elemento = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, exatec_xpath))
        )
        elemento.click()
        print("✓ Hice click en Exatec")

        # 2) Espera al campo de usuario y envía el ID
        user_xpath = '//*[@id="Ecom_User_ID"]'
        user_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, user_xpath))
        )
        user_input.clear()
        user_input.send_keys('A01793646')
        print("✓ Usuario ingresado")

        # 3) Espera al campo de contraseña y envía la clave
        password_xpath = '//*[@id="Ecom_Password"]'
        pass_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, password_xpath))
        )
        pass_input.clear()
        pass_input.send_keys('Endeavor1$')
        print("✓ Contraseña ingresada")

        # 4) Espera y click en el botón de entrar
        enter_xpath = '//*[@id="submitButton"]'
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, enter_xpath))
        )
        submit_btn.click()
        print("✓ Click en Entrar realizado")
        
    except TimeoutException as e:
        print(f"✗ No se encontró alguno de los elementos en tiempo: {e}")
        
    input("Presiona Enter para cerrar el navegador...")
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

    # 3) Llama a tu función pasándola como parámetro
    habit_starter(load_chrome, folder_root)
    