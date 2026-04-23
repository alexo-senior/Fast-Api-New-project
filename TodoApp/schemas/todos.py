from pydantic import BaseModel, Field, ConfigDict


#creamos una clase basada en BaseModel de pydantic
# Esquema para crear datos /actualizar tareas 
class TodoRequest(BaseModel):
    # el id no se pasa por ser clave primaria y debe ser autoincremental
    title:str = Field(min_length=3)
    description:str = Field(min_length=3, max_length=100)
    priority:int = Field(gt=0, lt=6)
    complete:bool = Field(default=False)
    
    
    
    
class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str
    priority: int
    complete: bool