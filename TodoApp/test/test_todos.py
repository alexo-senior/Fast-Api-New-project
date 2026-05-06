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


# ahora se pueden escribir las pruebas para la aplicación, 
# utilizando el cliente de pruebas para hacer solicitudes a la app y verificar las respuestas

def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'title': 'Learn to code',
                                'description': 'Need to learn everyday', 
                                'priority': 5, 'complete': False,
                                'owner_id': 1}]
    

# se prueba la obtencio de un todo por id con un usuario autenticado, 
# utilizando el fixture de prueba para crear un todo de prueba en la base 
# de datos de pruebas, y luego haciendo una solicitud GET al endpoint 
# correspondiente para obtener ese todo por su id, y verificando que la 
# respuesta sea correcta y contenga los datos del todo de prueba creado. 
# ya no espera una lista  sino un unico todo 
def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'title': 'Learn to code',
                                'description': 'Need to learn everyday', 
                                'priority': 5, 'complete': False,
                                'owner_id': 1}
    
# seprueba la obtencion por medio de un id que no existe, 
# para verificar que la app maneja bien los casos en los 
# se solicita un todo errado o que no existe  y devuelve la respuesta correcta 

def test_read_one_athenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code ==404
    assert response.json() == {'detail':'Todo not found'}
    
    # prueba exitosa, se muestra un mensaje indicando que la prueba ha pasado
    print("test_read_one_athenticated_not_found passed")
    
# se prueba la creación de un nuevo todo, haciendo una solicitud POST al endpoint correspondiente,
# con los datos del nuevo todo en el cuerpo de la solicitud, y verificando que la
# respuesta sea correcta y que el nuevo todo se haya creado correctamente en la base de datos de pruebas

def test_create_todo_(test_todo):
    request_data={
        'title':'New Todo',
        'description':'New todo description',
        'priority':5,
        'complete':False
        
        }
    response = client.post('/todo/',json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')   
    
