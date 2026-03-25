from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
# importar el motor de la bd
from database import SessionLocal
#para validar el jwt y obtener la carga uutil(payload)
from .auth import get_current_user

# LOGICA DE LOS ENDPOINTS BASICOS DE LA APP 

router = APIRouter(
    prefix= '/admin',
    tags= ['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db # se ejecuta el codigo anterior incluido el yield antes de enviar la respuesta
    finally:
        db.close() # se ejecuta el cierre de la bd despues de enviar la respuesta
# asi se asegura que solo se abra una conexion a la bd por cada peticion que se haga a la app

# simplifica la declaracion de dependencias 

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


#OBTENER TODOS LOS ENDPOINTS 

@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    if user is None or user.get('user_role')!= 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

# BORRAR 

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db:db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role')!='admin': # si el usuario es dif de admin
        raise HTTPException(status_code=401, detail='Authentication Failed') # lanzaz una excepcion
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() # consulta el modelo y trae la primera coincidencia
    if todo_model is None: # si el modelo es none 
        raise HTTPException(status_code=404, detail='Todo not found') # lanza la excepcion
    db.query(Todos).filter(Todos.id == todo_id).delete() # si es correcto el id borrar
    db.commit() # confirma el borrado y cierra
    
    
    
    

    
    
