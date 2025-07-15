
import os 
import sys 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import yaml


def message_print(message): 
    message_highlights= '*' * len(message)
    message = f'\n{message_highlights}\n{message}\n{message_highlights}\n'
    return message

def yaml_creation(download_folder): 
    output_yaml = os.path.join(download_folder, "passwords.yaml")
    yaml_exists = os.path.exists(output_yaml)

    if yaml_exists:
        # Abrir y cargar el contenido YAML en un diccionario
        with open(output_yaml, 'r', encoding='utf-8') as f:
            data_access = yaml.safe_load(f)
        print(f"Archivo cargado correctamente: {os.path.basename(output_yaml)}")
        return data_access

    else: 
        print(message_print("No se localizó un yaml válido, vamos a crear uno con: "))
        platforms = ["1st_item"] # Los items
        fields    = ["url", "user", "password", "ACTIONS"] # Cada variable de los bancos
        
        lines = []
        for platform in platforms:
            for field in fields:
                # clave = valor vacío
                lines.append(f"{platform}_{field}: ")
            lines.append("")  # línea en blanco entre bloques
        
        # Escribe el archivo YAML (aunque use "=" tal como en tu ejemplo)
        with open(output_yaml, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def site_operation(ACTIONS, driver, timeout):
    for url, steps in ACTIONS.items():
        print(f"\n🔗 Navegando a {message_print(url)}")
        driver.get(url)

        try:
            for idx, step in enumerate(steps, start=1):
                typ = step["type"]
                print(f"  → Paso {idx}: {typ}", end="")
                if typ == "wait_user":
                    msg = step.get("value", "Presiona enter para continuar...")
                    print(f"\n    ⏸ {msg}")
                    input()  # Aquí espera al usuario antes de continuar
                    continue  # Saltamos cualquier búsqueda de elementos
                else:
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



def habit_starter(chrome_driver_load, folder_root): 
    download_folder= os.path.join(folder_root, "Downloads")
    data_access = yaml_creation(download_folder) 
    driver = chrome_driver_load(download_folder)
    message_simplicity = "Primer objetivo: cargar mi perfil en simplicity"
    print(message_print(message_simplicity))
    timeout = 20
    ACTIONS = data_access['ACTIONS']
    site_operation(ACTIONS, driver, timeout)    


if __name__ == "__main__":
    folder_root = os.getcwd()
    # 1) Añade al path la carpeta donde está df_multi_match.py
    libs_dir = os.path.join(folder_root, "Library")
    sys.path.insert(0, libs_dir)
    # 2) Ahora importa la función directamente
    from chrome_driver_load import load_chrome
    # 3) Llama a tu función pasándola como parámetro
    habit_starter(load_chrome, folder_root)
    