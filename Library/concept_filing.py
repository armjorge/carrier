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
                "Companies",
                "Applications",
                "Cover Letters"
            ]
        )

        schema = self.data_access['db_structure']['schema_name']    

        if vista == "Companies":
            st.title("🏢 Companies & Business Types")

            col1, col2 = st.columns(2)

            # === 🗂️ Sección: Company Types ===
            with col1:
                st.subheader("📂 Company Types")

                # Mostrar registros actuales
                try:
                    df_types = pd.read_sql(
                        f'SELECT type_business FROM "{schema}".company_types ORDER BY type_business;',
                        conn
                    )
                except Exception:
                    df_types = pd.DataFrame()

                st.dataframe(df_types, use_container_width=True, height=250)

                st.markdown("### ➕ Agregar nuevo Company Type")
                new_type_business = st.text_input("Nuevo Type Business")

                if st.button("Agregar Company Type"):
                    if new_type_business:
                        try:
                            with conn.cursor() as cur:
                                cur.execute(
                                    f'''
                                    INSERT INTO "{schema}".company_types (type_business)
                                    VALUES (%s)
                                    ON CONFLICT DO NOTHING;
                                    ''',
                                    (new_type_business,)
                                )
                                conn.commit()
                            st.success("✅ Tipo de negocio agregado correctamente.")
                        except Exception as e:
                            st.error(f"❌ Error al agregar tipo de negocio: {e}")
                    else:
                        st.warning("⚠️ El tipo de negocio no puede estar vacío.")

            # === 🏢 Sección: Companies ===
            with col2:
                st.subheader("🏢 Companies")

                # Mostrar registros actuales
                try:
                    df_companies = pd.read_sql(
                        f'SELECT company_name, company_type, created_at FROM "{schema}".companies ORDER BY company_name;',
                        conn
                    )
                except Exception:
                    df_companies = pd.DataFrame()

                st.dataframe(df_companies, use_container_width=True, height=250)

                st.markdown("### ➕ Agregar nueva Company")
                new_company_name = st.text_input("Nombre de la Company")

                # Cargar opciones de tipo de negocio
                try:
                    company_types_df = pd.read_sql(
                        f'SELECT type_business FROM "{schema}".company_types ORDER BY type_business;',
                        conn
                    )
                    company_type_options = company_types_df['type_business'].tolist()
                except Exception:
                    company_type_options = []

                selected_company_type = st.selectbox("Tipo de negocio", options=company_type_options)

                if st.button("Agregar Company"):
                    if new_company_name and selected_company_type:
                        try:
                            with conn.cursor() as cur:
                                cur.execute(
                                    f'''
                                    INSERT INTO "{schema}".companies (company_name, company_type)
                                    VALUES (%s, %s)
                                    ON CONFLICT DO NOTHING;
                                    ''',
                                    (new_company_name, selected_company_type)
                                )
                                conn.commit()
                            st.success("✅ Company agregada correctamente.")
                        except Exception as e:
                            st.error(f"❌ Error al agregar Company: {e}")
                    else:
                        st.warning("⚠️ Debes llenar ambos campos para agregar una Company.")

        elif vista == "Applications":
            st.title("📝 Applications")

            # === Mostrar registros actuales ===
            try:
                df = pd.read_sql(f'''
                    SELECT job, education1, education2, education3,
                        experience1, experience2, experience3,
                        skills, interests, lang, status,
                        company_name, company_type, created_at
                    FROM "{schema}".applications
                    ORDER BY created_at DESC;
                ''', conn)
            except Exception:
                df = pd.DataFrame()

            st.dataframe(df, use_container_width=True)

            st.markdown("### ➕ Agregar nueva Application")

            # === Formulario ===
            with st.form("add_application_form", clear_on_submit=True):
                st.subheader("🧠 Información General")

                new_job = st.text_input("Job position")

                # === Educación ===
                st.markdown("#### 🎓 Education")
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_education1 = st.text_area("Education 1", height=100)
                with col2:
                    new_education2 = st.text_area("Education 2", height=100)
                with col3:
                    new_education3 = st.text_area("Education 3", height=100)

                # === Experiencia ===
                st.markdown("#### 💼 Experience")
                col4, col5, col6 = st.columns(3)
                with col4:
                    new_experience1 = st.text_area("Experience 1", height=100)
                with col5:
                    new_experience2 = st.text_area("Experience 2", height=100)
                with col6:
                    new_experience3 = st.text_area("Experience 3", height=100)

                # === Skills & Interests ===
                st.markdown("#### 🧩 Skills & Interests")
                new_skills = st.text_area("Skills", height=120)
                new_interests = st.text_area("Interests", height=120)

                # === Idioma y Estado ===
                st.markdown("#### 🌍 Language & Status")
                col7, col8 = st.columns(2)
                with col7:
                    lang_options = ["English", "Spanish", "French"]
                    new_lang = st.selectbox("Language", options=lang_options)
                with col8:
                    status_options = ["applied", "interviewing", "offered", "rejected"]
                    selected_status = st.selectbox("Status", options=status_options)

                # === Empresa y Tipo ===
                st.markdown("#### 🏢 Company Information")

                try:
                    companies_df = pd.read_sql(
                        f'SELECT company_name, company_type FROM "{schema}".companies ORDER BY company_name;',
                        conn
                    )
                    company_options = companies_df.to_dict('records')
                except Exception:
                    company_options = []

                if company_options:
                    company_names = [c['company_name'] for c in company_options]
                    selected_company_name = st.selectbox("Company Name", options=company_names)

                    # Obtener automáticamente el company_type correspondiente
                    selected_company_type = next(
                        (c['company_type'] for c in company_options if c['company_name'] == selected_company_name),
                        None
                    )
                    st.info(f"**Company Type:** {selected_company_type}")
                else:
                    selected_company_name = st.text_input("Company Name (if none available)")
                    selected_company_type = st.text_input("Company Type (must exist in company_types.type_business)")

                # === Botón de envío ===
                submitted = st.form_submit_button("💾 Agregar Application")

                if submitted:
                    if new_job and selected_company_name and selected_company_type and selected_status:
                        try:
                            with conn.cursor() as cur:
                                cur.execute(
                                    f'''
                                    INSERT INTO "{schema}".applications 
                                    (job, education1, education2, education3,
                                    experience1, experience2, experience3,
                                    skills, interests, lang, status,
                                    company_name, company_type)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT DO NOTHING;
                                    ''',
                                    (
                                        new_job,
                                        new_education1, new_education2, new_education3,
                                        new_experience1, new_experience2, new_experience3,
                                        new_skills, new_interests,
                                        new_lang, selected_status,
                                        selected_company_name, selected_company_type
                                    )
                                )
                                conn.commit()
                            st.success("✅ Application agregada correctamente.")
                        except Exception as e:
                            st.error(f"❌ Error al agregar Application: {e}")
                    else:
                        st.warning("⚠️ Los campos Job, Company Name y Status son obligatorios.")
        elif vista == "Cover Letters":
            st.title("📄 Cover Letters")

            # === Cargar combinaciones válidas desde applications ===
            try:
                apps_df = pd.read_sql(
                    f'SELECT job, lang, company_name FROM "{schema}".applications ORDER BY job;',
                    conn
                )
            except Exception:
                apps_df = pd.DataFrame()

            if apps_df.empty:
                st.warning("⚠️ No existen aplicaciones registradas aún. Agrega una antes de crear cartas.")
                st.stop()

            # Crear lista legible para selección
            combo_options = [
                f"{row.job} — {row.lang} — {row.company_name}" for _, row in apps_df.iterrows()
            ]
            selected_combo = st.selectbox("Selecciona una aplicación (Job — Language — Company):", combo_options)

            # Parsear selección
            job_selected, lang_selected, company_selected = selected_combo.split(" — ")

            # === Buscar si ya existe una carta para esa combinación ===
            try:
                query = f'''
                    SELECT header, address, date, body, "end", sign
                    FROM "{schema}".cover_letters
                    WHERE job = %s AND lang = %s AND company_name = %s;
                '''
                cover_df = pd.read_sql(query, conn, params=(job_selected, lang_selected, company_selected))
            except Exception:
                cover_df = pd.DataFrame()

            # Valores iniciales si ya existe
            if not cover_df.empty:
                current = cover_df.iloc[0]
                st.info("✏️ Carta existente: puedes editar los campos abajo.")
            else:
                current = pd.Series({"header": "", "address": "", "date": "", "body": "", "end": "", "sign": ""})
                st.info("🆕 Nueva carta: llena los campos para crearla.")

            # === Formulario ===
            with st.form("cover_letter_form"):
                st.markdown("### 🧾 Información de la carta")

                header = st.text_area("Header", value=current["header"], height=100)
                address = st.text_area("Address", value=current["address"], height=80)
                date_str = st.text_input("Date (YYYY-MM-DD)", value=str(current["date"]) if pd.notna(current["date"]) else "")
                body = st.text_area("Body", value=current["body"], height=250)
                end_text = st.text_area("End", value=current["end"], height=80)
                sign = st.text_area("Sign", value=current["sign"], height=60)

                submitted = st.form_submit_button("💾 Guardar carta")

                if submitted:
                    try:
                        with conn.cursor() as cur:
                            # 1️⃣ Intentar insertar si no existe
                            cur.execute(f'''
                                INSERT INTO "{schema}".cover_letters
                                (job, lang, company_name, header, address, date, body, "end", sign)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT DO NOTHING;
                            ''', (
                                job_selected, lang_selected, company_selected,
                                header, address, date_str if date_str else None, body, end_text, sign
                            ))

                            # 2️⃣ Actualizar siempre (si ya existía, se actualiza)
                            cur.execute(f'''
                                UPDATE "{schema}".cover_letters
                                SET header = %s, address = %s, date = %s, body = %s, "end" = %s, sign = %s
                                WHERE job = %s AND lang = %s AND company_name = %s;
                            ''', (
                                header, address, date_str if date_str else None, body, end_text, sign,
                                job_selected, lang_selected, company_selected
                            ))

                            conn.commit()

                        st.success("✅ Carta guardada correctamente.")

                    except Exception as e:
                        st.error(f"❌ Error al guardar la carta: {e}")

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