# este archivo es la raiz y va toda la aplicacion 
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
# imprrtar los modelos para crear las tablas en la bd
import models
from models import Todos
# importar el motor de la bd
from database import engine, SessionLocal


app = FastAPI()
# sql creara una bd llamada todos en la ubicacion de  la app TODOAPP
# esto ocurrira automaticamente al ejecutar la app 
models.Base.metadata.create_all(bind=engine) # crea las tablas en la bd si no existen

def get_db():
    db = SessionLocal()
    try:
        yield db # se ejecuta el codigo anterior incluido el yield antes de enviar la respuesta
    finally:
        db.close() # se ejecuta el cierre de la bd despues de enviar la respuesta
# asi se asegura que solo se abra una conexion a la bd por cada peticion que se haga a la app

        
@app.get("/")     
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()

