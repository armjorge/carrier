
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
import pandas as pd
from docx import Document
import yaml
from sqlalchemy import create_engine



class CV_GENERATION():
    def postgre_to_docx(self):
        init(autoreset=True)
        print(f"{Fore.BLUE}CARRIER MANAGEMENT{Style.RESET_ALL}")
        self.templates_path = os.path.join(self.working_folder, "CV Templates")
        os.makedirs(self.templates_path, exist_ok=True)
        # Intialize curriculum template
        self.template_1_path = os.path.join(self.templates_path, "Curriculum.docx")
        # request info
        query = "SELECT * FROM career_accelerator.applications" # Query inicial
        # 1️⃣ Conectar
        connexion = self.sql_conexion(self.data_access['DB_URL']).connect()
        if connexion is None:
            print("❌ No se pudo establecer conexión con SQL Server.")
            return False

        # 2️⃣ Intentar leer tabla de cuentas
        try:

            self.df_applications = pd.read_sql(query, connexion)
            print(f"✅ Loaded applications: {len(self.df_applications)} registros.")
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error ejecutando la consulta SQL: {e}")
        # Debug: imprimir todos los párrafos del template y guardarlos en un archivo
        template_path = self.template_1_path

        if os.path.exists(template_path):
            doc = Document(template_path)
            debug_file = os.path.join(self.output_path, "template_debug.txt")

            print(f"{Fore.YELLOW}🔍 Leyendo estructura del template Word...{Style.RESET_ALL}")
            with open(debug_file, "w", encoding="utf-8") as f:
                for i, p in enumerate(doc.paragraphs):
                    text_repr = repr(p.text)
                    print(f"[{i}] → {text_repr}")
                    f.write(f"[{i}] → {text_repr}\n")

            print(f"{Fore.GREEN}✅ Estructura del template guardada en: {debug_file}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ No se encontró el template en: {template_path}{Style.RESET_ALL}")
        df = self.df_applications
        print(f"{Fore.CYAN}📄 Generando currículums...{Style.RESET_ALL}")

        for _, row in df.iterrows():
            job = str(row.get("job", "Unknown"))
            try:
                doc = Document(self.template_1_path)

                # 🔹 Reemplazar placeholders en párrafos con soporte para saltos de línea y bullets
                for p in doc.paragraphs:
                    for key in df.columns:
                        placeholder = f"{{{key}}}"
                        if placeholder in p.text:
                            value = str(row.get(key, "")).replace('\\n', '\n')
                            parts = value.split('\n')

                            # Reemplaza el placeholder por la primera línea
                            p.text = p.text.replace(placeholder, parts[0])

                            # Si hay más líneas, las inserta como nuevos párrafos con el mismo estilo
                            if len(parts) > 1:
                                p_element = p._element
                                body_element = doc._body._element
                                index = list(body_element).index(p_element)

                                for part in parts[1:]:
                                    new_p = doc.add_paragraph(part, style=p.style.name)
                                    new_p_element = new_p._element
                                    body_element.remove(new_p_element)
                                    body_element.insert(index + 1, new_p_element)
                                    index += 1

                output_file = os.path.join(self.output_path, f"Cuaxospa_{job}.docx")
                doc.save(output_file)
                print(f"{Fore.GREEN}✅ Curriculum generado: {output_file}{Style.RESET_ALL}")

            except Exception as e:
                print(f"{Fore.RED}❌ Error generando {job}: {e}{Style.RESET_ALL}")


    def sql_conexion(self, sql_url):
        try:
            engine = create_engine(sql_url)
            return engine
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
    # Initialize the main components
    def __init__(self, working_folder, data_access):
        self.working_folder = working_folder
        os.makedirs(self.working_folder, exist_ok=True)
        self.data_access = data_access
        self.output_path = os.path.join(self.working_folder, "Output CVs")
        os.makedirs(self.output_path, exist_ok=True)
        
if __name__ == "__main__":
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(env_path, '.env')
    folder_name = "MAIN_PATH"
    db_key = "DB_URL"
    
    working_folder = "."
    pg_dict = {}

    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        working_folder = os.getenv(folder_name)
        pg_dict = {"DB_URL": os.getenv(db_key)} 

    yaml_path = os.path.join(env_path, 'config', 'config.yml')
    with open(yaml_path, 'r') as file:
        data_access = yaml.safe_load(file)
        if data_access is None:
            data_access = {}
        data_access.update(pg_dict)  # ⚠️ Esto solo funciona si data_access es una lista

    app = CV_GENERATION(working_folder, data_access)
    app.postgre_to_docx()