
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos


app = FastAPI(title="TodoApp create on FastApi")
# sql creara una bd llamada todos en la ubicacion de la app TODOAPP
# esto ocurrira automaticamente al ejecutar la app

models.Base.metadata.create_all(bind=engine) # crea las tablas en la bd si no existen

# ahora incluimos el router en el main

app.include_router(auth.router)
app.include_router(todos.router)



    
    
    
    
    
    
    
    
    



