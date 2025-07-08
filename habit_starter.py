
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
    message = f'{message_highlights}\n{message}\n{message_highlights}'
    return message

def habit_starter(chrome_driver_load, folder_root): 
    download_folder= os.path.join(folder_root, "Downloads")

    driver = chrome_driver_load(download_folder)
    message_simplicity = "Primer objetivo: cargar mi perfil en simplicity"
    print(message_print(message_simplicity))
    driver.get("https://tec-csm.symplicity.com/")
    input("Presiona Enter para cerrar el navegador...")
    driver.quit()
    

if __name__ == "__main__":
    folder_root = r"/Users/armjorge/Library/CloudStorage/GoogleDrive-armjorge@gmail.com/My Drive/Projects/habit_starter"
   

    # 1) Añade al path la carpeta donde está df_multi_match.py
    libs_dir = os.path.join(folder_root, "Library")
    sys.path.insert(0, libs_dir)

    # 2) Ahora importa la función directamente
    from chrome_driver_load import load_chrome

    # 3) Llama a tu función pasándola como parámetro
    habit_starter(load_chrome, folder_root)
    