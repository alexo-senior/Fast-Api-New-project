# importar un motor para la base de datos 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'# la base de datos estara en la url

# crea una variable engine que conecta el motor con la base de datos
# create_engine recibe dos parametros: la url de la base de datos y un diccionario de argumentos de conexion
# el argumento de coneccion chek_thread es para una misma coneccion y evitar errores en sqlite 
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False} )

#se cra una instancia de sesion y cada instancia tendra una sesion de bd
# sesioj local igual a creador de sesionnes autoconfirmaciones, autolavado y vincula al motor engine
sessionmakerLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# para ser capaz de llamar a la base de datos datos.py y poder crear una bd

Base = declarative_base() # se crea una clase base para los modelos de la bd









