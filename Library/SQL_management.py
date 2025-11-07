import os
from sqlalchemy import create_engine
import yaml
from datetime import date, datetime
import pandas as pd
import glob
import numpy as np
from psycopg2.extras import execute_values
from pandas._libs.missing import NAType
from pandas._libs.tslibs.nattype import NaTType
from dateutil.relativedelta import relativedelta

try:
    from Library.SQL_initialize import INITIALIZE
except ModuleNotFoundError:
    # fallback if running inside the Library folder
    from SQL_initialize import INITIALIZE
from dotenv import load_dotenv


class CSV_TO_SQL:
    def csv_to_sql_process(self):
        query = "SELECT * FROM carrier_accelerator.companies" # Query inicial
        # 1️⃣ Conectar
        connexion = self.sql_conexion(self.data_access['DB_URL']).connect()
        if connexion is None:
            print("❌ No se pudo establecer conexión con SQL Server.")
            return False

        # 2️⃣ Intentar leer tabla de cuentas
        try:
            
            self.df_companies = pd.read_sql(query, connexion)
            print(f"✅ Loaded companies: {len(self.df_companies)} registros.")

        except Exception as e:
            error_msg = str(e)

            # Si la tabla no existe
            if "UndefinedTable" in error_msg or "does not exist" in error_msg:
                print("⚠️ Table 'banorte_load.accounts' not found.")
                print("🛠️ Running INITIALIZE().initialize_postgres_db() to create schema and tables...")
                initializer = INITIALIZE()
                initializer.initialize_postgres_db(self.data_access, self.working_folder)

                # Reintento
                try:
                    self.df_companies = pd.read_sql(query, connexion)
                    print(f"✅ Loaded companies after creation: {len(self.companies)} registros.")
                except Exception as e2:
                    print(f"❌ Error after trying to create schema/tables: {e2}")
                    return False

            # Si el esquema no existe
            elif "InvalidSchemaName" in error_msg or "schema" in error_msg.lower():
                print("⚠️ Schema 'banorte_load' not found.")
                print("🛠️ Running INITIALIZE().initialize_postgres_db() to create schema and tables...")
                initializer = INITIALIZE()
                initializer.initialize_postgres_db(self.data_access, self.working_folder)

                # Reintento
                try:
                    self.df_companies = pd.read_sql(query, connexion)
                    print(f"✅ Loaded companies after creation: {len(self.df_companies)} registros.")
                except Exception as e2:
                    print(f"❌ Error after trying to create schema/tables: {e2}")
                    return False
            else:
                print(f"❌ Error ejecutando la consulta SQL: {e}")
                return False

        # 3️⃣ Validar contenido de cuentas
        if self.df_companies.empty:
            print("⚠️ No hay registros en 'self.df_companies'. Captura empresas antes de comenzar.")
            return False

    def sql_conexion(self, sql_url):
        try:
            engine = create_engine(sql_url)
            return engine
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
        
    def __init__(self, working_folder, data_access):
        self.today = date.today()
        self.working_folder = working_folder
        self.data_access = data_access
        self.current_folder = os.path.join(self.working_folder,'Info Bancaria', f'{self.today.year}-{self.today.month:02d}')
        self.closed_folder = os.path.join(self.working_folder,'Info Bancaria', 'Meses cerrados', 'Repositorio por mes')
        
if __name__ == "__main__":
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(env_path, '.env')
    folder_name = "MAIN_PATH"
    db_key = "DB_URL"
    
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        working_folder = os.getenv(folder_name)
        pg_dict = {"DB_URL": os.getenv(db_key)}  # ✅ dict correcto, no set

    yaml_path = os.path.join(env_path, 'config', 'config.yml')
    with open(yaml_path, 'r') as file:
        data_access = yaml.safe_load(file)
        if data_access is None:
            data_access = {}
        data_access.update(pg_dict)  # ⚠️ Esto solo funciona si data_access es una lista

    app = CSV_TO_SQL(working_folder, data_access)
    app.csv_to_sql_process()