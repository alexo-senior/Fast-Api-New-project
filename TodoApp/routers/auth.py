from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
#Esta libreria tiene su propio portal en swagger y es mas seguro
#podremos obtener usuario y contraseña desde la solicitud
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from jose import jwt, JWTError

# AUTENTICACIONES Y AUTORIZACIONES

# para organizar el swagger u dividir las authorizazciones de los endpoints

router = APIRouter(
    prefix= '/auth',
    tags= ['auth']
    
)


SECRET_KEY = 'ecb3072a588916deec8528324ebbe7794fdee92dd45aab26da6e011979295b7d'
# ahora trabaja junto con secret_key parra dar mas seguridad a jwt
ALGORITHM = 'HS256'


# para manejar los hash ded encryptacion se debe instalar las librerias:passlib y Bcrypt==4.0.1
# esto se encarga de transformar el texto plano de contraseña que introoduce el usuario en un hash 
# de seguridad evitando ser hackeada la contraseña
# creamos  una nueva variable que contenga Cryptcontext

# esto es configuracion de base para funcionamiento

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# para verificar cada solicitud que se nos envie desde el cliente 

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


#FUNCION PARA AUTENTICACION

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        print(f"DEBUG: el usuario'{username}' No existe en esta BD")
        return False
    
    print(f"DEBUG: Usuario encontrado. Hash en DB: {user.hashed_password}")
    
    #if not bcrypt_context.verify(password, user.hashed_password):
    #    return False
    #return True
    try:
        # Forzamos la verificación
        is_valid = bcrypt_context.verify(password, user.hashed_password)
        print(f"DEBUG: ¿Coincide la clave?: {is_valid}")
        return user if is_valid else False
    except Exception as e:
        print(f"DEBUG: Error crítico en bcrypt: {e}")
        return False
    return user


# funcion para jwt 
    
def create_access_token(username: str, user_id: int, expires_delta:timedelta):
    
    #cuando obtenemos el token se puede decodificar el jwt si esta autenticado
    # y tenemos el username y el user_id 
    
    encode = {'sub':username, 'id':user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# funcion parra que los demas endpoints puedan verificar el usuario actual
# valida el jwt, obtener la carga util y convertirla en nombre de usuario y el id

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        # la carga util es decodificada y verificada la clave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username':username, 'id': user_id}
    
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        
    
    

#creamos una clase para autenticacion de datos

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    

# esta clase es para devolver mas informacion     
class Token(BaseModel):
    access_token: str
    token_type:str 
    
# el modelo para obtener la bd se copia tambien en auth:   
    
def get_db():
    db = SessionLocal()
    try:
        yield db # se ejecuta el codigo anterior incluido el yield antes de enviar la respuesta
    finally: 
        db.close() 
        


db_dependency = Annotated[Session, Depends(get_db)]
    
        
    

@router.post("/", status_code=status.HTTP_201_CREATED)
# para guardar en la bd se coloca db_dedpendency como parametro
async def created_user(db:db_dependency,
                    create_user_request:CreateUserRequest):

    # check for existing username/email before hashing
    existing = db.query(Users).filter(
        (Users.username == create_user_request.username) |
        (Users.email == create_user_request.email)
    ).first()
    if existing:
        # conflict: user already exists
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already registered",
        )

    #debe tener la informacion del modelo o tabla
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active= True
    )
    # return create_user_model 
    db.add(create_user_model) # agrega el modelo creado a la bd
    try:
        db.commit()
        db.refresh(create_user_model)
    except Exception as err:
        # rollback and turn into HTTP error
        db.rollback()
        # if it's an integrity error, send a sensible message, otherwise re-raise
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        )
    return create_user_model
    


# El siguiente paso es guaradar la informacion del usuario creado en una bd
# en lugar de solo devolver una respuesta del modelo al cliente


# EL TOKEN SE DEVUELVE AL USUARIO CON LA INFORMACION DENTRO
# PRIMERO SE CREA EL ENDPOINT QUE RECIBE LA INFORMACION DEL USUARIO
"""

@router.post("/token")
async def login_for_access(form_data:Annotated[OAuth2PasswordRequestForm, Depends()],
                        db:db_dependency):
    # se llama a la funcion user_authenticated
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        return 'failed Auhtentication'
    return 'Succesful Authentication'

"""
@router.post("/token", response_model=Token)
async def login_for_access(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    # Crear el token JWT
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"} # devuelve un diccionario



# Endpoint para accededr a la creacion de usuarios


@router.get("/users")
async def list_all_users(db: db_dependency):
    users = db.query(Users).all()
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]





















    
    
    


