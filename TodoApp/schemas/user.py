from pydantic import BaseModel, Field



#clase modelo para crear el acmbio de contraseña
class userVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)
    
    # SE CREA LA CLASE PARA ACTUALIZAR EL NUMERO DE TELEFONO DEL USUARIO, 
    # SE AÑADE UNA VALIDACION DE LONGITUD MINIMA Y MAXIMA PARA ASEGURAR QUE EL NUMERO DE TELEFONO SEA VALIDO
class PhoneUpdate(BaseModel):
    phone_number: str = Field(
        min_length=10, 
        max_length=15, 
        description="Nuevo número de teléfono del usuario"
        )
    
    
    
    