#Los modelos son las tablas de la base de datos
#contienen la estructuta y tipos de datos de cada columna
from database import Base
from sqlalchemy import Column, Integer , String, Boolean, ForeignKey

# nueva clase que creara una nueva tabla llamada Users
"""
class Users(Base):
    __tablename__ = 'Users'
    """
    
class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index= True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String) # contraseña encriptada que no se puede descifrar
    is_active = Column(Boolean, default=True)# muestra si el usuario essta o no activo en la cuenta
    role = Column(String) # comprueba si el usuario es o no administrador
    phone_number = Column(String)
    
    
    
    
    
    

# clase Todos que crara una nueva tabla llamada todos 

class Todos(Base):
    __tablename__='todos' 

    # id va a ser una columna de tipo entero en nuestra bd
    # primary key porque sera un registro unico index para darle facilicidad de busqueda
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    # al iniciar sesion el usuario con su clave puede acceder a todas las tareas
    # pendientes que tengan o coincidan con ese mismo id
    # la FK debe apuntar al nombre real de la tabla, en este caso en minúsculas
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    