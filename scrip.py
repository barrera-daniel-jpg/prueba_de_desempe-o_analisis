# Importacion de las librerias
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey
from urllib.parse import quote_plus



# Carga del DataSet 
df = pd.read_csv('student_performance_dataset.csv', encoding='cp1252')      
# RUTA es una variable que almacena la ruta del dataser

# Exploracion inicial
print(f'>> El DataSet presenta la siguiente catnidad de filas y columnas: {df.shape}')
print(f'>> La informacion de las columnas es: ')
print(df.dtypes)
# Se realiza una exploracion de la informacion de las columnas con su tipo de dato

# Traduccion de columnas
df = df.rename(columns={
    'student_id':'id_estudiante',
    'gender':'genero',
    'study_time_hours':'horas_de_estudio',
    'attendance_percent':'porcentaje_de_asistencia',
    'sleep_hours':'horas_de_sueno',
    'parental_education':'educacion_de_los_padres',
    'internet_access':'acceso_internet',
    'extracurricular_activities':'actividades_extracurriculares',
    'part_time_job':'trabaja_medio_tiempo',
    'previous_grade':'nota_previa',
    'final_exam_score':'nota_posterior',
    'final_grade':'nota_final',
})
# Se traducen los nombres de las columnas para mayor facilidad y compresion en el powerBI

print('==='*20)
# Traduccion de los valores de columnas especificas
df['genero'] = df['genero'].replace({'Male':'Masculino',
                                    'Female': 'Femenino'})

df['educacion_de_los_padres']= df['educacion_de_los_padres'].replace({
    'Bachelors':'Pregrado/Postgrado',
    'High School':'Bachiller',
    'Master':'Maestria',
    'PhD':'Doctorado'
})
df['educacion_de_los_padres']=df['educacion_de_los_padres'].fillna('Sin estudios')

df['actividades_extracurriculares']= df['actividades_extracurriculares'].replace({'Yes': 'Si',})
df['trabaja_medio_tiempo']= df['trabaja_medio_tiempo'].replace({'Yes': 'Si',})
df['acceso_internet']= df['acceso_internet'].replace({'Yes': 'Si',})

# Se traducen los nombres de algunos valores de columnas en especifico para mayor eficiencia en la visualizacion de datos

print(df.dtypes)
print('==='*20)



#¿Cual es la cantidad de personas que trabajan?
personas_trabajadoras = (df['trabaja_medio_tiempo'] == 'Si').sum()
print(f'>> La cantidad de personas que trabajan equivalen a {personas_trabajadoras}')

personas_sin_internet = (df['acceso_internet'] == 'No').sum()
print(f'>> La cantidad de personas que no tienen acceso a internet equivalen a {personas_sin_internet}')

personas_disciplinadas = (df['actividades_extracurriculares'] == 'Si').sum()
print(f'>> La cantidad de personas que son disciplinadas con sus activades extracurricalres equivalen a {personas_disciplinadas}')


# Normalizar entidades
df_estudiantes = df[['id_estudiante', 'genero', 'educacion_de_los_padres', 'acceso_internet']]
df_actividad_estudiantes = df[['id_estudiante', 'horas_de_estudio', 'horas_de_sueno', 'actividades_extracurriculares', 'trabaja_medio_tiempo']]
df_resultado_estudiantes = df[['id_estudiante', 'porcentaje_de_asistencia', 'nota_previa', 'nota_posterior', 'nota_final']]

print(df_resultado_estudiantes)
print(df_actividad_estudiantes)
print(df_estudiantes)


# --- Cargar los datos a postgres

# Datos de conexión
USUARIO = 'daniel'
PASSWORD = quote_plus('123456')
HOST = 'localhost'
PUERTO = '5433'
BASE_DATOS = 'info_db'

# Crear el engine de conexión
engine = create_engine(f'postgresql+psycopg2://{USUARIO}:{PASSWORD}@{HOST}:{PUERTO}/{BASE_DATOS}')

metadata = MetaData()

estudiantes = Table(
    'estudiantes', metadata,
    Column('id_estudiante', Integer, primary_key=True),
    Column('genero', String),
    Column('educacion_de_los_padres', String),
    Column('acceso_internet', String)
)

# Tabla hija: actividad_de_estudiantes (FK -> estudiantes.id_estudiante)
actividad_de_estudiantes = Table(
    'actividad_de_estudiantes', metadata,
    Column('id_estudiante', Integer, ForeignKey('estudiantes.id_estudiante'), primary_key=True),
    Column('horas_de_estudio', Float),
    Column('horas_de_sueno', Float),
    Column('actividades_extracurriculares', String),
    Column('trabaja_medio_tiempo', String)
)

# Tabla hija: metricas_estudiantes (FK -> estudiantes.id_estudiante)
metricas_estudiantes = Table(
    'metricas_estudiantes', metadata,
    Column('id_estudiante', Integer, ForeignKey('estudiantes.id_estudiante'), primary_key=True),
    Column('porcentaje_de_asistencia', Float),
    Column('nota_previa', Float),
    Column('nota_posterior', Float),
    Column('nota_final', String)
)

# Crea las 3 tablas en el orden correcto (padre antes que hijas) respetando las FK
# drop_all primero por si ya existían de una corrida anterior con to_sql (sin constraints)
metadata.drop_all(engine)
metadata.create_all(engine)



# Cargar el DataFrame a una tabla
df_estudiantes.to_sql(
    'estudiantes',   # nombre de la tabla destino
    con=engine,
    if_exists='append',     # 'replace' = borra y crea de nuevo | 'append' = agrega filas | 'fail' = error si ya existe
    index=False               # no guarda el índice de pandas como columna
)
df_actividad_estudiantes.to_sql(
    'actividad_de_estudiantes',   # nombre de la tabla destino
    con=engine,
    if_exists='append',     # 'replace' = borra y crea de nuevo | 'append' = agrega filas | 'fail' = error si ya existe
    index=False               # no guarda el índice de pandas como columna
)
df_resultado_estudiantes.to_sql(
    'metricas_estudiantes',   # nombre de la tabla destino
    con=engine,
    if_exists='append',     # 'replace' = borra y crea de nuevo | 'append' = agrega filas | 'fail' = error si ya existe
    index=False               # no guarda el índice de pandas como columna
)

print('>> Datos cargados exitosamente a PostgreSQL con Pk y FK')

# Creacion de mascaras para la interpretacion de datos y validar el funcionamiento

hombres_trabajadores = (df['genero'] == 'Masculino') & (df['trabaja_medio_tiempo'] == 'Si')
suma_h_trabajadores = (hombres_trabajadores).sum()
print(f'>> La cantidad de hombres que trabajan medio tiempo y tienen actividades extracurriculares equivale a {suma_h_trabajadores}')



