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

1. **Registras una vez** tu información base: educación, experiencias, skills
2. **Creas aplicaciones** vinculadas a empresas y roles específicos
3. **Generas CVs personalizados** automáticamente en el idioma que necesites
4. **Haces seguimiento** del estado (aplicado, entrevista, oferta, rechazado)

El sistema usa **templates de Word con placeholders inteligentes** que se alimentan de una base de datos PostgreSQL, permitiéndote modificar tu narrativa profesional sin tocar el diseño del documento.

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
1. **Inicializar la base de datos** (primera vez)
2. **Capturar aplicaciones** via interfaz Streamlit
3. **Generar CVs personalizados** en Word

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
- `company_types`: Tipos de empresa (consultora, startup, corporativo)
- `companies`: Empresas objetivo con clasificación
- `applications`: Aplicaciones con info completa del CV + estado

### Generación de CVs
Los templates de Word usan placeholders tipo `{job}`, `{skills}`, `{experience1}` que se reemplazan dinámicamente con datos de PostgreSQL.

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

