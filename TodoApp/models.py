#Los modelos son las tablas de la base de datos
#contienen la estructuta y tipos de datos de cada columna
from database import Base
from sqlalchemy import Column, Integer , String, Boolean



class Todos(Base):
    __tablename__='todos' #nombre de la tabla
    # id va a ser una columna de tipo entero en nuestra bd 
    # primar key porque sera un registro unico index para darle facilicidad de busqueda
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    
    
    
    
    
    
    
    
    
    
    