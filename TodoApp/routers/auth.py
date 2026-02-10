from fastapi import APIRouter
from pydantic import BaseModel
from models import Users



router = APIRouter()

#creamos una clase para autenticacion de datos

class CreateUserRequest(BaseModel):
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    
        
    

@router.post("/auth/")
async def created_user(create_user_request:CreateUserRequest):
    #debe tener la informacion del modelo o tabla
    
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request.password, # campo password por hashed_password
        is_active= True
        
    )
    return create_user_model

    
    
    


