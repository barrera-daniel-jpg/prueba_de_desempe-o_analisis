# Student Performance Analysis & Pipeline ETL
Este proyecto consiste en una solución integral de procesamiento de datos (ETL) y exploración analítica (EDA) orientada a evaluar los factores conductuales, demográficos y de estilo de vida que impactan el rendimiento académico de estudiantes en su último año escolar.
La meta principal del análisis es responder a preguntas de negocio clave e identificar patrones para predecir el rendimiento académico a partir de variables como horas de estudio, hábitos de sueño, trabajo a medio tiempo y actividades extracurriculares.
- - -
##  Arquitectura y Tecnologías Utilizadas
- Lenguaje principal: Python 3.x
- Extracción y Transformación (ETL): pandas
- Librerias de python: SQLAlchemy, psycopg2-binary
- Base de Datos: PostgreSQL (ejecutado dentro de un contenedor en Docker)
- Visualización de Datos: Power BI
-Entorno de Despliegue: Docker / Docker Compose con variables de entorno (.env)
- - -
## Arquitectura y Flujo de Trabajo (Pipeline)

```
+------------------------------------+
|  Dataset Raw: CSV                  |
|  (student_performance_dataset.csv) |
+------------------------------------+
                  |
                  v
+------------------------------------+
|  Procesamiento ETL (Python/Pandas)  |
|  - Limpieza y Rename de columnas   |
|  - Mapeo/Traducción de valores     |
|  - Normalización en 3 Entidades    |
+------------------------------------+
                  |
                  v
+------------------------------------+
|  Modelado y Carga (SQLAlchemy)     |
|  - Definición DDL (PK/FK)          |
|  - Dropped & Re-creation de tablas |
|  - Carga relacional en PostgreSQL  |
+------------------------------------+
                  |
                  v
+------------------------------------+
|  Base de Datos (Docker Container)  |
|  - DB: info_db (PostgreSQL)        |
|  - Tablas: estudiantes,            |
|    actividad_de_estudiantes,       |
|    metricas_estudiantes            |
+------------------------------------+
                  |
                  v
+------------------------------------+
|  Capa de Analítica & Visualización  |
|  - Conexión PostgreSQL en Power BI |
|  - Dashboard de Métricas y EDA     |
+------------------------------------+
```
- - -
## Modelo Entidad-Relación (Base de Datos)
El script implementa un modelo normalizado en PostgreSQL dividiendo el dataset original en tres entidades clave conectadas mediante id_estudiante:
1. **estudiantes (Tabla Padre)**:
- id_estudiante (PK, Integer)
- genero (String)
- educacion_de_los_padres (String)
- acceso_internet (String)
2. **actividad_de_estudiantes (Tabla Hija - FK)**:
- id_estudiante (PK / FK, Integer)
- horas_de_estudio (Float)
- horas_de_sueno (Float)
- actividades_extracurriculares (String)
- trabaja_medio_tiempo (String)
3. **metricas_estudiantes (Tabla Hija - FK)**:
- id_estudiante (PK / FK, Integer)
- porcentaje_de_asistencia (Float)
- nota_previa (Float)
- nota_posterior (Float)
- nota_final (String)
- - -
## Preguntas de Negocio e Hipótesis planteadas
El dashboard en Power BI y los análisis exploratorios buscan resolver las siguientes incógnitas:
- Impacto del tiempo dedicado: ¿Qué tan amplia es la diferencia entre la nota previa y la nota posterior en función de las horas de estudio?
- Rendimientos decrecientes: ¿A partir de cuántas horas de estudio los rendimientos marginales empiezan a decrecer?
- Hábitos perjudiciales: ¿La falta de tiempo y factores perjudiciales (dormir poco, estudiar menos de 2 horas) realmente afectan el rendimiento académico?
- Carga laboral y disciplina: ¿Los estudiantes que trabajan a medio tiempo y aún así mantienen actividades extracurriculares logran mejores notas?
- Driver principal: ¿Qué variable pesa más en el resultado final según la matriz de correlación?
- - -
## Pasos para Ejecución
1. Requisitos Previos
Python 3.9+
Docker Desktop o Docker Engine instalado.
PostgresSQL - pgadmin
- - -
## Creación y Activación del Entorno Virtual (Python)

Es buena práctica aislar las librerías del proyecto en un entorno virtual (`venv`).

* **En Windows (PowerShell / CMD):**
  ```bash
  python -m venv venv
  . env\Scripts ctivate
  ```

* **En macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### 3. Instalación de Dependencias

Con el entorno virtual activado, instala todas las librerías requeridas utilizando `pip`:

```bash
pip install pandas sqlalchemy psycopg2-binary
```

*Nota: `psycopg2-binary` es el conector que permite a SQLAlchemy interactuar de forma nativa con bases de datos PostgreSQL.*

---

### 4. Configuración y Despliegue de PostgreSQL con Docker

Puedes desplegar la base de datos de dos formas según tu preferencia:

#### Opción A: Mediante Comando de Docker Directo
Ejecuta el siguiente comando para levantar un contenedor con PostgreSQL configurado según los parámetros del script (`puerto 5433`):

```bash
docker run --name postgres_student_db   -e POSTGRES_USER=daniel   -e POSTGRES_PASSWORD=123456   -e POSTGRES_DB=info_db   -p 5433:5432   -d postgres:15-alpine
```

#### Opción B: Mediante Docker Compose (Recomendado)
Si prefieres usar un archivo `docker-compose.yml`, crea o utiliza el archivo con la siguiente estructura:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    container_name: postgres_student_db
    environment:
      POSTGRES_USER: daniel
      POSTGRES_PASSWORD: '123456'
      POSTGRES_DB: info_db
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Para iniciar el contenedor con Docker Compose:
```bash
docker compose up -d
```

---

### 5. Ejecución del Pipeline ETL

Una vez que el contenedor de Docker esté en estado `running`, ejecuta el script de procesamiento de datos en Python:

```bash
python script.py
```

**Lo que realiza el script automáticamente:**
1. Carga el dataset `student_performance_dataset.csv` con la codificación requerida (`cp1252`).
2. Traduce los encabezados de las columnas y los valores categóricos (género, nivel educativo, respuestas Sí/No).
3. Separa el conjunto de datos en las 3 entidades normalizadas.
4. Se conecta a PostgreSQL, elimina/crea el esquema de tablas respetando las Claves Primarias y Foráneas, e inserta masivamente los registros.

Al finalizar exitosamente, verás el mensaje:
> `>> Datos cargados exitosamente a PostgreSQL con Pk y FK`

---

### 6. Conexión con Power BI

1. Abre **Power BI Desktop**.
2. Selecciona **Obtener datos** -> **Base de datos de PostgreSQL**.
3. Ingresa los parámetros de conexión:
   - **Servidor:** `localhost:5433`
   - **Base de datos:** `info_db`
4. Selecciona el modo de conectividad (**Import** o **DirectQuery**).
5. Ingresa las credenciales de acceso:
   - **Usuario:** `daniel`
   - **Contraseña:** `123456`
6. Selecciona las 3 tablas (`estudiantes`, `actividad_de_estudiantes`, `metricas_estudiantes`) y carga los datos para interactuar con el Dashboard.
