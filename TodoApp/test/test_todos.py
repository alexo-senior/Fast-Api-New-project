from sqlalchemy import create_engine, text 
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import Base 
from main import app
from routers.todos import get_db as todos_get_db
from routers.auth import get_db as auth_get_db, get_current_user
# para forzar las pruebas
from fastapi.testclient import TestClient
from fastapi import status
#ppytest se usara ppara escribir pruebas unitarias para la aplicacion 
import pytest
# se importan los modelos de la base de datos para crear datos de prueba en la base de datos de pruebas
from models import Todos





# primero se crea una fake db para pruebas, se importa el modelo de la bd y se crean los datos de prueba
# # se crea una base de datos sqlite para pruebas, 
# la base de datos se llamara test.db y se ubicara en el mismo directorio del proyecto

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

# esta función se usará para SOBREESCRIIBIR la función get_db (en todo.py)
# en las pruebas, para que use la base de datos de pruebas en 
# lugar de la base de datos real. 

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

def override_get_current_user():
    return {"username": "codingwithAlexistest", "id": 1, "user_role": "admin"}
        
# se sobreescribe la dependencia get_db con la función override_get_db,
# para que use la base de datos de pruebas en lugar de la base de datos real

app.dependency_overrides[todos_get_db] = override_get_db
app.dependency_overrides[auth_get_db] = override_get_db

# se sobreescribe la dependencia get_current_user para que devuelva un usuario de prueba,
# con un id específico, para que las pruebas puedan acceder a los datos de ese usuario en
# la base de datos de pruebas.

app.dependency_overrides[get_current_user] = override_get_current_user

# se crea una instancia de TestClient pasando
# la app como argumento, para poder hacer solicitudes a la app en las pruebas
client = TestClient(app)

# se crea un fixture de pytest para crear un todo de prueba en la base de datos de pruebas,
# que se puede usar en las pruebas para verificar el funcionamiento de la app con datos reales de prueba.
# se crea una dependencia igual igual a la que se usa en la app, para que las pruebas puedan acceder a 
# la base de datos de pruebas y crear los datos de prueba necesarios para las pruebas.
@pytest.fixture
def test_todo():
    todo = Todos(title="Learn to code",
            description="Need to learn everyday",
            priority=5,
            complete=False,
            owner_id=1,
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos")) 
        connection.commit()# se eliminan los datos de prueba después de las pruebas para mantener la base de datos limpia
    
    
    
    


# este print prueba que la dependencia get_db ha sido sobreescrita correctamente, 
# mostrando el diccionario de dependencias sobreescritas en la app
#print(app.dependency_overrides)

#ahora para cambiar nuestras dependencias en las pruebas, 
# se crea una instancia de TestClient pasando la app como argumento



# ahora se pueden escribir las pruebas para la aplicación, 
# utilizando el cliente de pruebas para hacer solicitudes a la app y verificar las respuestas

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'title': 'Learn to code',
                                'description': 'Need to learn everyday', 
                                'priority': 5, 'complete': False}] 
    
    



        
        
        

