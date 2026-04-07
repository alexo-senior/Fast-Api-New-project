from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import  APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos, Users
# importar el motor de la bd
from database import SessionLocal
#para validar el jwt y obtener la carga uutil(payload)
from .auth import get_current_user
#para trabajar con contraseñas
from passlib.context import CryptContext


# LOGICA DE LOS ENDPOINTS BASICOS DE LA APP 

router = APIRouter(
    prefix='/user',
    tags=['user']
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
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#clase modelo para crear el acmbio de contraseña
class userVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    
    # SE CREA LA CLASE PARA ACTUALIZAR EL NUMERO DE TELEFONO DEL USUARIO, 
    # SE AÑADE UNA VALIDACION DE LONGITUD MINIMA Y MAXIMA PARA ASEGURAR QUE EL NUMERO DE TELEFONO SEA VALIDO
class PhoneUpdate(BaseModel):
    phone_number: str = Field(min_length=10, max_length=15, description="Nuevo número de teléfono del usuario")
    
    

# ENDPOINT PARA MIRAR LA INFOORMACION DEL USUARIO

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()



# ENDPOINT QUE PERMITE CAMBIAR LA CONTRASEÑA DE USUARIO

# es ded notar que no se usa {password} en esta funcion ya que seria un parametro de ruta
# y no seria seguro exponer la contraseña en la url, por eso se usa un modelo de 
# pydantic para recibir la ocntraseña actula y e la nueva contraseña en el cuerpo 
# de la solicitud 

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency,
                        user_verification: userVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    user_model.hashed_password= bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    
    
    # NUEVA SOLICITUD TIPO PUT QUE PERMITE ACTUALIZAR EL NUMERO DE TELEFONO DEL USUARIO
"""    
@router.put("/phone_number/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency, db:db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # primero obtenemos el modelo del usuario a partir de su id que se obtiene del token
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    # luego se actualiza el numero de telefono con el valor que recibe en el endpoint
    user_model.phone_number = phone_number
    # se guarad el modelo actualizado en la bd y se confirma el cambio con commit
    db.add(user_model)
    db.commit()
    
    """
    
    # NUEVA FORMA SEGURA DE ACTUALIZAR EL NUMERO BASADO EN PYDANTIC Y NO EN PARAMETROS DE RUTA
    
@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_update: PhoneUpdate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    # primero obtenemos el modelo del usuario a partir de su id que se obtiene del token
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    # luego se actualiza el numero de telefono con el valor que recibe en el endpoint
    user_model.phone_number = phone_update.phone_number
    # se guarda el modelo actualizado en la bd y se confirma el cambio con commit
    db.add(user_model)
    db.commit()
    # DE ESTA FORMA SE EVITA EXPONER EL NUMERO EN LA URL Y SE PUEDE AÑADIR VALIDACIONES DE LONGITUD 
    # Y FORMATO AL NUMERO DE TELEFONO
    
    