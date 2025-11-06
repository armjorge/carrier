import os
from dotenv import load_dotenv
from colorama import Fore, Style, init
from sqlalchemy import create_engine, text
from datetime import date
import pandas as pd  
from urllib.parse import urlparse
import psycopg2
import sys
import subprocess

class INITIALIZE:
    def __init__(self):
        print(f"{Fore.BLUE}CLASS INITIALIZE{Style.RESET_ALL}")

    def initialize_postgres_db(self, data_access, working_folder):
        print(f"{Fore.BLUE}INICIALIZANDO BASE DE DATOS PostgreSQL{Style.RESET_ALL}")
        self.today = date.today()

        # Extraer datos de la URL
        db_url = data_access["DB_URL"]
        parsed = urlparse(db_url)
        conn_params = {
            "dbname": parsed.path.lstrip("/"),
            "user": parsed.username,
            "password": parsed.password,
            "host": parsed.hostname,
            "port": parsed.port or 5432,
        }

        # Conexión directa psycopg2
        try:
            raw_conn = psycopg2.connect(**conn_params)
            raw_conn.autocommit = True
            cur = raw_conn.cursor()
            print(f"{Fore.GREEN}✅ Direct PostgreSQL connection established.{Style.RESET_ALL}")
        except Exception as e:
            print(f"❌ Error creating raw PostgreSQL connection: {e}")
            return False



        # Leer el resto del script
        file_path = os.path.dirname(__file__)
        sql_path = os.path.join(file_path, "..", "SQL", "initializing.sql")

        if not os.path.exists(sql_path):
            print(f"❌ SQL file not found: {sql_path}")
            raw_conn.close()
            return False

        try:
            with open(sql_path, "r", encoding="utf-8") as f:
                sql_content = f.read()
            # Diccionario db_structure del yaml 
            dict_db = data_access['db_structure']
            # Extracción de los placeholders anidados
            resolved = {}
            for key, value in dict_db.items():
                if isinstance(value, str):
                    temp = value
                    for inner_key, inner_value in dict_db.items():
                        if isinstance(inner_value, str):
                            temp = temp.replace(f"{{{inner_key}}}", inner_value)
                    resolved[key] = temp.strip()
            # Dividir respetando $$, ignorar comentarios
            statements = []
            current_stmt = []
            inside_function = False
            for line in sql_content.splitlines():
                stripped = line.strip()
                if not stripped or stripped.startswith("--"):
                    continue
                if "$$" in stripped:
                    inside_function = not inside_function
                    current_stmt.append(line)
                    continue
                if not inside_function and stripped.endswith(";"):
                    current_stmt.append(line)
                    statements.append("\n".join(current_stmt).strip())
                    current_stmt = []
                else:
                    current_stmt.append(line)
            if current_stmt:
                statements.append("\n".join(current_stmt).strip())
            # después, reemplazar todos los placeholders del SQL
            rendered_statements = []
            for stmt in statements:
                for key, value in resolved.items():
                    stmt = stmt.replace(f"{{{key}}}", value)
                rendered_statements.append(stmt)
            statements = rendered_statements
            print(f"🛠️ Executing {len(statements)} statements from 00_create_base.sql ...")


            for i, stmt in enumerate(statements, 1):
                try:
                    print(f"{Fore.YELLOW}▶️  Executing statement {i}/{len(statements)}...{Style.RESET_ALL}")
                    print(f"🧾  {stmt[:60].replace(chr(10),' ')}...")  # muestra inicio del query
                    print(stmt)
                    cur.execute(stmt)
                except Exception as e:
                    print(f"{Fore.RED}❌ Error in statement {i}: {e}{Style.RESET_ALL}")
                    print(f"--- SQL ---\n{stmt[:400]}...\n")
                    continue

            # Listar tablas creadas
            print(f"{Fore.CYAN}📋 Current tables in '{dict_db['schema_name']}':{Style.RESET_ALL}")
            cur.execute(f"SELECT tablename FROM pg_tables WHERE schemaname = '{dict_db['schema_name']}';")
            for row in cur.fetchall():
                print(f"   - {row[0]}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error executing script: {e}{Style.RESET_ALL}")
            raw_conn.close()
            return False

        raw_conn.close()
        print(f"{Fore.GREEN}🎯 Initialization complete and connection closed.{Style.RESET_ALL}")

        streamlit_path = os.path.join(file_path, "concept_filing.py")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_path], check=True)
        except Exception as e:
            print(f"❌ Error al ejecutar Streamlit: {e}")

        return True
        
