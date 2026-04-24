from fastapi.testclient import TestClient
import main
from fastapi import status

# para conecar nuestro cliente de pruebas con la app, 
# se crea una instancia de TestClient pasando la app como argumento

client = TestClient(main.app) # main.app ya que la app esta definida en el main.py

def test_return_heath_check():
    response = client.get("healthy") # se hace una solicitud GET a la ruta /healthy
    assert response.status_code == status.HTTP_200_OK # se verifica que el codigo de estado sea 200 OK
    assert response.json() == {"message": "TodoApp is healthy!"} # se verifia que la respuesta JSON sea la esperada, es decir
    print(response.json()) 
    
    
    
    
    
    