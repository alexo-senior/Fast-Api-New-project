
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, user 



# PRINCIPAL DE LA APP 

app = FastAPI(title="TodoApp create on FastApi")
# sql creara una bd llamada todos en la ubicacion de la app TODOAPP
# esto ocurrira automaticamente al ejecutar la app

models.Base.metadata.create_all(bind=engine) # crea las tablas en la bd si no existen

# ahora incluimos el router en el main

# para verificar que la app esta corriendo correctamente, 
# se puede crear una ruta de prueba que devuelva un mensaje de salud,
# y luego se puede probar esa ruta con una herramienta como Postman o 
# curl para asegurarse de que la app esta funcionando correctamente.

@app.get("/healthy")
def health_check():
    return {"message": "TodoApp is healthy!"}


#punto de entrada que importa y monta los routesrs 

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)




    
    
    
    
    
    
    
    
    



