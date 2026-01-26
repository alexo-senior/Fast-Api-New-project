# este archivoes la raiz y va toda la aplicacion 
from fastapi import FastAPI
# imprrtar los modelos para crear las tablas en la bd
import models
# importar el motor de la bd
from database import engine


app = FastAPI()
# sql creara una bd llamada todos en la ubicacion de  la app TODOAPP
# esto ocurrira automaticamente al ejecutar la app 
models.Base.metadata.create_all(bind=engine) # crea las tablas en la bd si no existen

