import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# sqlite_database
sqlite_file_name = "../database.sqlite"
# Leer el directorio actual de este archivo
base_dir = os.path.dirname(os.path.realpath(__file__))

# URL de la base de datos
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Echo Muestra por consola lo que se esta revisando
engine = create_engine(database_url, echo=True)

# bind se enlaza con el motor de la db
Session = sessionmaker(bind=engine)

# permite manipualar las tablas de la bd
Base = declarative_base()