# este archivo es la raiz y va toda la aplicacion 
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, Path, status
# imprrtar los modelos para crear las tablas en la bd
import models
from models import Todos
# importar el motor de la bd
from database import engine, SessionLocal


app = FastAPI(title="TodoApp create on FastApi")
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

# simplifica la declaracion de dependencias 

db_dependency = Annotated[Session, Depends(get_db)]
        
"""@app.get("/")     
async def read_all(db: Annotated[Session, Depends(get_db)]):
    return db.query(Todos).all()"""

#creamos una clase basada en BaseModel de pydantic

class TodoRequest(BaseModel):
    # el id no se pasa por ser clave primaria y debe ser autoincremental
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority:int = Field(gt=0, lt=6)
    complete:bool = Field(default=False)



@app.get("/")     
async def read_all(db: db_dependency):
    return db.query(Todos).all()

# AÑADIR FUNCIONALIDADES 
# con parametro de ruta 
#se agrega status code 200 ok para validacion de exito

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)

# se agrega path para validar que el id sea mayor a 0
async def read_todo(db:db_dependency, todo_id:int = Path(gt=0)):

    # la bd se obtiene del modelo, filtros id, y se obtiene el primer resultado
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    #si no es none que devuelva el modelo
    if todo_model is not None:
        return todo_model
    # sino lanzamos una excepcion
    raise HTTPException(status_code=404, detail='Todo not found')

# crear registros

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_request:TodoRequest):
    todo_model = Todos(**todo_request.dict())

    db.add(todo_model)
    db.commit() # guarda los cambios en la bd
    db.refresh(todo_model)# recarga el modelo con los datos de la bd
    return todo_model# devuelve el modelo creado 


# actualizar registros 

@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency, todo_id:int, todo_request:TodoRequest):
                    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    
    
    
    
    



