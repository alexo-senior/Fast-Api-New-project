from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session


router = APIRouter()


# para manejar los hash ded encryptacion se debe instalar las librerias:passlib y Bcrypt==4.0.1
# esto se encarga de transformar el texto plano de contraseña que introoduce el usuario en un hash 
# de seguridad evitando ser hackeada la contraseña
# creamos  una nueva variable que contenga Cryptcontext

# esto es configuracion de base para funcionamiento

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

#creamos una clase para autenticacion de datos

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    
# el modelo para obtener la bd se copia tambien en auth:   
    
def get_db():
    db = SessionLocal()
    try:
        yield db # se ejecuta el codigo anterior incluido el yield antes de enviar la respuesta
    finally:
        db.close() # se ejecuta el cierre de la bd despues de enviar la respuesta
# asi se asegura que solo se abra una conexion a la bd por cada peticion que se haga a la app

# simplifica la declaracion de dependencias con una variable

db_dependency = Annotated[Session, Depends(get_db)]
    
        
    

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
# para guardar en la bd se coloca db_dedpendency como parametro
async def created_user(db:db_dependency,
                    create_user_request:CreateUserRequest):
    
    #debe tener la informacion del modelo o tabla
    
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        #hashed_password=create_user_request.password, # campo password por hashed_password
        hashed_password=bcrypt_context.hash(create_user_request.password),# la conntraseña sera iigual a lo que devuelva bcrypt
        is_active= True
        
    )
    # return create_user_model 
    db.add(create_user_model) # agrega el modelo creado a la bd
    db.commit()
    


# El siguiente paso es guaradar la informacion del usuario creado en una bd
# en lugar de solo devolver una respuesta del modelo al cliente




    
    
    


