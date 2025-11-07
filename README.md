# Career Manager 🎯

## El Problema

Gestionar aplicaciones de empleo ejecutivas es un desafío estratégico. Cada aplicación requiere:
- **Personalización**: Adaptar tu narrativa profesional al perfil específico
- **Multi-idioma**: Competir en mercados globales (inglés, español, francés)
- **Trazabilidad**: No perder de vista qué enviaste, a quién, y en qué estado está
- **Consistencia**: Mantener la calidad sin repetir trabajo manual

El resultado: Pierdes tiempo en tareas administrativas en lugar de enfocarte en lo que realmente importa: **resaltar los aspectos de tu carrera que hacen match con cada oportunidad**.

## La Solución

**Career Manager** es un sistema que centraliza la gestión de tus aplicaciones laborales, permitiéndote:

✅ **Crear CVs personalizados** en segundos para cada aplicación  
✅ **Trabajar en 3 idiomas** (English, Spanish, French) sin esfuerzo adicional  
✅ **Mantener trazabilidad** de cada aplicación y su estado  
✅ **Enfocarte en lo estratégico**: qué elementos de tu experiencia destacar para cada rol  

### ¿Cómo funciona?

1. **Inicializas** el sistema (primera vez): se crea automáticamente el schema en PostgreSQL
2. **Poblas datos** via una **interfaz web Streamlit** que te guía paso a paso:
   - Defines tipos de empresa (Consultoría, Servicios Financieros, Tech, etc.)
   - Registras empresas objetivo con su clasificación
   - Capturas aplicaciones con toda tu información profesional personalizada para cada rol
3. **Generas CVs** automáticamente en el idioma que necesites (English, Spanish, French)
4. **Mantienes trazabilidad** del estado de cada aplicación (aplicado, entrevista, oferta, rechazado)

**Sin escribir una sola línea de SQL**. La interfaz web elimina la fricción de generar inserts manuales, permitiéndote enfocarte en la narrativa estratégica de tu carrera.

El sistema usa **templates de Word con placeholders inteligentes** (e.g., `{job}`, `{skills}`, `{experience1}`) que se alimentan automáticamente de PostgreSQL.

---

## Inicio Rápido

### Prerequisitos
- Python 3.8+
- PostgreSQL
- Cuenta con acceso a base de datos PostgreSQL

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/armjorge/career_manager.git
cd career_manager

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu DB_URL y MAIN_PATH
```

### Configuración

Edita el archivo `.env`:
```bash
DB_URL=postgresql://usuario:password@host:5432/nombre_db
MAIN_PATH=/ruta/donde/quieres/guardar/los/archivos
```

### Uso

```bash
python carrier_management.py
```

El menú interactivo te permite:
1. **Inicializar la base de datos** (primera vez) - Crea el schema PostgreSQL automáticamente
2. **Poblar datos** - Abre una interfaz web Streamlit donde capturas:
   - Company Types (tipos de empresa)
   - Companies (empresas objetivo)
   - Applications (aplicaciones con toda tu info profesional)
3. **Generar CVs personalizados** en Word con un click

---

## Arquitectura (Técnico)

```
career_manager/
├── carrier_management.py      # Orquestador principal
├── Library/
│   ├── SQL_initialize.py      # Setup de schema PostgreSQL
│   ├── SQL_management.py      # Gestión de conexiones
│   ├── CV_generation.py       # Motor de generación de CVs
│   ├── concept_filing.py      # UI Streamlit para captura
│   └── chrome_helper.py       # Utilidades web
├── SQL/
│   └── initializing.sql       # Schema con 3 tablas relacionales
└── config/
    └── config.yml             # Configuración de estructura DB
```

### Base de Datos
Estructura relacional en PostgreSQL:
- `company_types`: Tipos de empresa (consultoría, startup, corporativo, finanzas, tech)
- `companies`: Empresas objetivo vinculadas a su tipo
- `applications`: Aplicaciones con información completa del CV + tracking de estado

**Ventaja clave**: Se pobla mediante una **interfaz web Streamlit** intuitiva que muestra las 3 tablas con formularios guiados. Esto elimina completamente la necesidad de escribir INSERTs SQL a mano, acelerando la captura de datos y reduciendo errores.

### Generación de CVs
Los templates de Word usan placeholders tipo `{job}`, `{skills}`, `{experience1}` que se reemplazan dinámicamente con datos de PostgreSQL. Cada aplicación puede tener contenido diferente según el match con el rol objetivo.

---

## Roadmap

- [ ] Exportación a PDF automática
- [ ] Dashboard de métricas (tasa de respuesta por tipo de empresa)
- [ ] Integración con LinkedIn para importar datos
- [ ] Sistema de recordatorios para hacer follow-up
- [ ] Carga de templates

---

## Licencia

MIT License - Úsalo libremente para impulsar tu carrera profesional.

---

**¿Dudas o sugerencias?** Abre un issue o contacta a [@armjorge](https://github.com/armjorge) 

