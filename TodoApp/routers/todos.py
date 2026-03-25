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

router = APIRouter()

# sql creara una bd llamada todos en la ubicacion de  la app TODOAPP
# esto ocurrira automaticamente al ejecutar la app

# models.Base.metadata.create_all(bind=engine) # crea las tablas en la bd si no existen

# ahora incluimos el router en el main
# app.include_router(auth.router)

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


# OBTENER TODOS LOS DATOS 

@router.get("/", status_code=status.HTTP_200_OK)
# agregamos el user: user_dependency para obtener todas las tareas del usuario     
async def read_all(user:user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')
    # filtramospor el owner_id de todos los usuarios
    # filtramos por el owner_id del usuario y devolvemos la lista
    # se visualizan solo los id de este usuario autenticado
    return db.query(Todos).filter(Todos.owner_id == user.get('id'))\
        .order_by(Todos.id.asc())\
            .all()
    # en caso de necesitar ver todos los id de usuarios
    
# return db.query(Todos).order_by(Todos.id.asc()).all()

# AÑADIR FUNCIONALIDADES 
# con parametro de ruta 
#se agrega status code 200 ok para validacion de exito
# obtener con id

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# se agrega path para validar que el id sea mayor a 0
async def read_todo(user: user_dependency, 
                    db:db_dependency, 
                    todo_id:int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')
# la bd se obtiene del modelo, filtros id, y se obtiene el primer resultado
# sin embargo se añaden filtros por el id y el owner_id      
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
# si no es none que devuelva el modelo
    if todo_model is not None:
        return todo_model
    # sino lanzamos una excepcion
    raise HTTPException(status_code=404, detail='Todo not found')



# CREAR REGISTROS 
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user:user_dependency, db:db_dependency, 
                    todo_request:TodoRequest):
    # si el usuario no exite o es nulo lanza excepcion
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit() # guarda los cambios en la bd
    db.refresh(todo_model) # recarga el modelo con los datos de la bd
    return todo_model # devuelve el modelo creado 


# ACTUALIZAR REGISTROS  

@router.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, #solicitar la dependencia del usuario para validar el jwt y obtener la carga util(payload)
                    db:db_dependency, 
                    todo_request:TodoRequest, 
                    todo_id:int = Path(gt=0)):# el metodo TodoRrequest debe estar siempre encima de cualquier path
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first() # filtra por el id y el owner_id para validar que el usuario solo pueda actualizar sus tareas
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()
    
    
# BORRAR DATOS  
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def todo_delete(user:user_dependency,db:db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Autentication Failed')
    # se hace el filtrado por el id y por el owner_id
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).delete()
    
    # confirmacion de borrado 
    db.commit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    