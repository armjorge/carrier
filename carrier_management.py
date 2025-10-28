import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from Library.yaml_creator import YAMLCREATOR
from Library.chrome_helper import CHROME_HELPER
import pandas as pd
from docx import Document

class CARRIER_MANAGEMENT:
    # Orchstrate the main flow
    def run(self):
        init(autoreset=True)
        print(f"{Fore.BLUE}CARRIER MANAGEMENT{Style.RESET_ALL}")
        self.templates_path = os.path.join(self.working_folder, "CV Templates")
        os.makedirs(self.templates_path, exist_ok=True)
        # Intialize curriculum template
        self.template_1_path = os.path.join(self.templates_path, "Curriculum.docx")
        # Initialize database 
        self.db_path = os.path.join(self.working_folder, "applications")
        self.output_path = os.path.join(self.working_folder, "Output CVs")
        os.makedirs(self.output_path, exist_ok=True)
        # Path to the applications database

        if not os.path.exists(self.db_path):
            print(f"{Fore.YELLOW}⚠️ No se encontró el archivo applications.db en {self.working_folder}.{Style.RESET_ALL}")
            return

        df = pd.read_sql_query("SELECT * FROM applications", f"sqlite:///{self.db_path}")

        print(f"{Fore.CYAN}📄 Generando currículums...{Style.RESET_ALL}")
        for _, row in df.iterrows():
            job = str(row.get("JOB", "Unknown"))
            try:
                doc = Document(self.template_1_path)
                for p in doc.paragraphs:
                    for key in ["JOB", "TRIPLETEN", "MBA", "DIPLOMADO", "RETAIL", "ESEOTRES", "STATUS"]:
                        if f"{{{key}}}" in p.text:
                            for run in p.runs:
                                if f"{{{key}}}" in run.text:
                                    value = str(row.get(key, "")).replace('\\n', '\n')
                                    parts = value.split('\n')
                                    run.text = run.text.replace(f"{{{key}}}", parts[0])
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
                                    break
                output_file = os.path.join(self.output_path, f"Cuaxospa_{job}.docx")
                doc.save(output_file)
                print(f"{Fore.GREEN}✅ Curriculum generado: {output_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}❌ Error generando {job}: {e}{Style.RESET_ALL}")
        

    # Initialize the main components
    def __init__(self):
        self.folder_root = self.get_root_path()
        self.working_folder = os.path.join(self.folder_root, "Carrier management")  
        os.makedirs(self.working_folder, exist_ok=True)
        self.data_yaml = YAMLCREATOR(self.working_folder).data
        # Initialize Sprint 1.1: Get product list
        self.chrome_helper = CHROME_HELPER()
    # Get the root path
    def get_root_path(self):
        # Get the directory where main.py lives (repo folder)
        repo_path = os.path.dirname(os.path.abspath(__file__))
        repo_name = os.path.basename(repo_path)
        print(f"Current script path: {os.path.abspath(__file__)}")
        env_file = ".env"
        # Load .env if it exists
        full_repo_path = None
        if os.path.exists(env_file):
            load_dotenv(env_file)
            full_repo_path = os.getenv("MAIN_PATH") or os.getenv("Main_path")
            if not full_repo_path:
                with open(env_file, "r") as env_handle:
                    for line in env_handle:
                        stripped = line.strip()
                        if not stripped or stripped.startswith("#"):
                            continue
                        if stripped.lower().startswith("main_path"):
                            if ":" in stripped:
                                _, value = stripped.split(":", 1)
                            elif "=" in stripped:
                                _, value = stripped.split("=", 1)
                            else:
                                value = ""
                            full_repo_path = value.strip()
                            break
        if not full_repo_path:
            path_user = input("Please paste the path where the repo files will be created or enter to use the root: ")
            if path_user.strip():
                if os.path.exists(path_user):
                    full_repo_path = os.path.join(path_user, repo_name)
                else:
                    print("Path does not exist, using root")
                    full_repo_path = os.path.join(repo_path, repo_name)
            else:
                full_repo_path = os.path.join(repo_path, repo_name)
            os.makedirs(full_repo_path, exist_ok=True)
            # Write to .env
            with open(env_file, "a+") as f:
                f.seek(0)
                content = f.read()
                if "MAIN_PATH=" not in content:
                    f.write(f"MAIN_PATH={full_repo_path}\n")
            # Check if full_repo_path is inside repo_path
            if full_repo_path.startswith(repo_path + os.sep):
                gitignore_path = ".gitignore"
                with open(gitignore_path, "r") as f:
                    content = f.read()
                if f"{repo_name}/" not in content:
                    with open(gitignore_path, "a") as f:
                        f.write(f"{repo_name}/\n")
        return full_repo_path


if __name__ == "__main__":
    app = CARRIER_MANAGEMENT()
    app.run()