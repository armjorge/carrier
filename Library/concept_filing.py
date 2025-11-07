import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import yaml
from urllib.parse import urlparse

class CONCEPT_FILING:

    def __init__(self, working_folder, data_access):
        self.working_folder = working_folder
        self.data_access = data_access 

    def run_streamlit_interface(self):
        # 1) Parse DB URL from self.data_access['sql_workflow']
        sql_url = self.data_access['DB_URL']
        parsed = urlparse(sql_url)
        dbname = parsed.path.lstrip('/')
        user = parsed.username
        password = parsed.password
        host = parsed.hostname
        port = parsed.port

        # 2) Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # 3) Streamlit UI
        st.set_page_config(page_title="Resumen aplicaciones", layout="wide")

        vista = st.sidebar.radio(
            "Seleccionar vista:",
            [
                "Company Types",
                "Companies",
                "Applications"
            ]
        )

        schema = "career_accelerator"

        if vista == "Company Types":
            st.title("📂 Company Types")

            # Mostrar registros actuales
            try:
                df = pd.read_sql(f'SELECT type_business FROM "{schema}".company_types ORDER BY type_business;', conn)
            except Exception:
                df = pd.DataFrame()
            st.dataframe(df, use_container_width=True)

            st.markdown("### ➕ Agregar nuevo Company Type")
            new_type_business = st.text_input("Type Business")

            if st.button("Agregar Company Type"):
                if new_type_business:
                    try:
                        with conn.cursor() as cur:
                            cur.execute(
                                f'INSERT INTO "{schema}".company_types (type_business) VALUES (%s) ON CONFLICT DO NOTHING;',
                                (new_type_business,)
                            )
                            conn.commit()
                        st.success("✅ Company Type agregado correctamente.")
                    except Exception as e:
                        st.error(f"❌ Error al agregar Company Type: {e}")
                else:
                    st.warning("⚠️ El tipo de negocio no puede estar vacío.")

        elif vista == "Companies":
            st.title("🏢 Companies")

            # Mostrar registros actuales
            try:
                df = pd.read_sql(f'SELECT company_name, company_type, created_at FROM "{schema}".companies ORDER BY company_name;', conn)
            except Exception:
                df = pd.DataFrame()
            st.dataframe(df, use_container_width=True)

            st.markdown("### ➕ Agregar nueva Company")
            new_company_name = st.text_input("Company Name")
            try:
                company_types_df = pd.read_sql(f'SELECT type_business FROM "{schema}".company_types ORDER BY type_business;', conn)
                company_type_options = company_types_df['type_business'].tolist()
            except Exception:
                company_type_options = []
            selected_company_type = st.selectbox("Company Type", options=company_type_options)

            if st.button("Agregar Company"):
                if new_company_name and selected_company_type:
                    try:
                        with conn.cursor() as cur:
                            cur.execute(
                                f'INSERT INTO "{schema}".companies (company_name, company_type) VALUES (%s, %s) ON CONFLICT DO NOTHING;',
                                (new_company_name, selected_company_type)
                            )
                            conn.commit()
                        st.success("✅ Company agregada correctamente.")
                    except Exception as e:
                        st.error(f"❌ Error al agregar Company: {e}")
                else:
                    st.warning("⚠️ El nombre y tipo de company son obligatorios.")

        elif vista == "Applications":
            st.title("📝 Applications")

            # Mostrar registros actuales
            try:
                df = pd.read_sql(f'''
                    SELECT job, education1, education2, education3, diplomado, experience1, experience2, experience3, skills, interests, lang, status, company_name, company_type
                    FROM "{schema}".applications
                    ORDER BY job;
                    ''', conn)
            except Exception:
                df = pd.DataFrame()
            st.dataframe(df, use_container_width=True)

            st.markdown("### ➕ Agregar nueva Application")

            new_job = st.text_input("Job")
            new_education1 = st.text_input("Education 1")
            new_education2 = st.text_input("Education 2")
            new_education3 = st.text_input("Education 3")
            new_diplomado = st.text_input("Diplomado")
            new_experience1 = st.text_input("Experience 1")
            new_experience2 = st.text_input("Experience 2")
            new_experience3 = st.text_input("Experience 3")
            new_skills = st.text_area("Skills")
            new_interests = st.text_area("Interests")

            # Solo valores válidos según CHECK constraint
            lang_options = ["English", "Spanish", "French"]
            new_lang = st.selectbox("Language", options=lang_options)

            status_options = ["applied", "interviewing", "offered", "rejected"]
            selected_status = st.selectbox("Status", options=status_options)

            # Llaves foráneas
            new_company_name = st.text_input("Company Name")
            new_company_type = st.text_input("Company Type (must exist in company_types.type_business)")

            try:
                companies_df = pd.read_sql(f'SELECT company_name, company_type FROM "{schema}".companies ORDER BY company_name;', conn)
                company_options = companies_df[['company_name', 'company_type']].drop_duplicates().to_dict('records')
            except Exception:
                company_options = []

            company_names = [c['company_name'] for c in company_options]
            selected_company_name = st.selectbox("Company Name", options=company_names)

            # Get company_type for selected company_name
            selected_company_type = None
            for c in company_options:
                if c['company_name'] == selected_company_name:
                    selected_company_type = c['company_type']
                    break

            if st.button("Agregar Application"):
                if new_job and selected_company_name and selected_company_type and selected_status:
                    try:
                        with conn.cursor() as cur:
                            cur.execute(
                                f'''INSERT INTO "{schema}".applications 
                                (job, education1, education2, education3, diplomado, experience1, experience2, experience3, skills, interests, lang, status, company_name, company_type) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;''',
                                (new_job, new_education1, new_education2, new_education3, new_diplomado, new_experience1, new_experience2, new_experience3, new_skills, new_interests, new_lang, selected_status, selected_company_name, selected_company_type)
                            )
                            conn.commit()
                        st.success("✅ Application agregada correctamente.")
                    except Exception as e:
                        st.error(f"❌ Error al agregar Application: {e}")
                else:
                    st.warning("⚠️ Los campos Job, Company Name y Status son obligatorios.")

    def sql_conexion(self, sql_url):
        try:
            engine = create_engine(sql_url)
            return engine
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return None
        
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

    app = CONCEPT_FILING(working_folder, data_access)
    app.run_streamlit_interface()