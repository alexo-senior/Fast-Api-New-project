from sqlalchemy import create_engine 
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base 
from main import app
from routers.todos import get_db 


# primero se crea una fake db para pruebas, se importa el modelo de la bd y se crean los datos de prueba
# # se crea una base de datos sqlite para pruebas, 
# el archivo se llamara test.db y se ubicara en el mismo directorio del proyecto

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db" 

# se crea un motor de base de datos para la base de datos de pruebas
# se crea un entorno aislado paras pruebas, con una base de datos en
# memoria, para evitar interferencias con la base de datos real

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
    ) 


# se crea una clase de sesión para la base de datos de pruebas

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# se crea la base de datos de pruebas y las tablas correspondientes

Base.metadata.create_all(bind=engine)

# esta función se usará para sobreescribir la función get_db (en todo.py)
# en las pruebas, para que use la base de datos de pruebas en 
# lugar de la base de datos real. 

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# se sobreescribe la dependencia get_db con la función override_get_db,
# para que use la base de datos de pruebas en lugar de la base de datos real

app.dependency_overrides[get_db] = override_get_db

# este print prueba que la dependencia get_db ha sido sobreescrita correctamente, 
# mostrando el diccionario de dependencias sobreescritas en la app
#print(app.dependency_overrides)





        
        
        

