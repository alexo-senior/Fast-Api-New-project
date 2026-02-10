# importar un motor para la base de datos 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# sql creara una bd llamada todos en la ubicacion de  la app TODOAPP

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'# la base de datos estara en la url

# crea una variable engine que conecta el motor con la base de datos
# create_engine recibe dos parametros: la url de la base de datos y un diccionario de argumentos de conexion
# el argumento de coneccion chek_thread es para una misma coneccion y evitar errores en sqlite 

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False} )

#se crea una instancia de sesion y cada instancia tendra una sesion de bd
# sesionlocal igual a creador de sesionnes autoconfirmaciones, autolavado(autoflush) y vincula al motor engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# para ser capaz de llamar a la base de datos  y poder crear una bd

Base = declarative_base() # se crea una clase base para los modelos de la bd










