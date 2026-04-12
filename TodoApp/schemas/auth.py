from pydantic import BaseModel


#creamos una clase para autenticacion de datos

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str # se añade el numero de telefo para poder validar 
    

# esta clase es para devolver mas informacion     
class Token(BaseModel):
    access_token: str
    token_type:str
