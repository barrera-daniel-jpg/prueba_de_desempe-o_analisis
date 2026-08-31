# Importacion de las librerias
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, ForeignKey
from urllib.parse import quote_plus


# Carga del DataSet 
RUTA = ('student_performance_dataset.csv')
df = pd.read_csv(RUTA)

# Exploracion inicial
print(f'>> El DataSet presenta la siguiente catnidad de filas y columnas: {df.shape}')
print(f'>> La informacion de las columnas es: ')
print(df.dtypes)

# Traduccion de columnas
df = df.rename(columns={
    'studen_id':'id_estudiante',
    'gender':'genero',
    'study_time_hours':'horas_de_estudio',
    'attendance_percent':'%_de_asistencia',
    'sleep_hours':'horas_de_sueño',
    'parental_education':'educacion_de_los_padres',
    'internet_access':'acceso_internet',
    'extracurricular_activities':'actividades_extracurriculares',
    'part_time_job':'trabaja_medio_tiempo',
    'previous_grade':'nota_previa',
    'final_exam_score':'nota_posterios',
    'final_grade ':'nota_final',
})

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

print(df.dtypes)
print('==='*20)


#¿Cual es la cantidad de personas que trabajan?
personas_trabajadoras = (df['trabaja_medio_tiempo'] == 'Si').sum()
print(f'>> La cantidad de personas que trabajan equivalen a {personas_trabajadoras}')

personas_sin_internet = (df['acceso_internet'] == 'No').sum()
print(f'>> La cantidad de personas que no tienen acceso a internet equivalen a {personas_sin_internet}')

personas_disciplinadas = (df['actividades_extracurriculares'] == 'Si').sum()
print(f'>> La cantidad de personas que son disciplinadas con sus activades extracurricalres equivalen a {personas_disciplinadas}')