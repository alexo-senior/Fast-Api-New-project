from typing import Optional
from fastapi import FastAPI, Body
 # validaciones
from pydantic import BaseModel, Field 



app = FastAPI()

 #SE HA CREADO UN NUEVO OBJETO DONDE SE INICIALIZA UN CONSTRUCTOR
 #QUE ESTABLECE TODA LA INFORMACION

class BOOK:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int
    
    # CADA VEZA QUE SE EJECUTA LA APP CONTENDRA 6 LIBROS
    # SE PASA LA INFORMACION AL CONSTRUCTOR CON EL ID, TITLE,ETC
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
        
  # NUEVO OBJETO 
  # se usa field para personalizar las validaciones de campos
  
class BookRequest(BaseModel)       :
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str= Field(min_length=1, max_length=100)
    #greater than or less than(mayor que o menor que)
    rating: int= Field(gt=0, lt=6) # puntuacion entre 1 y 5
    published_date:int = 2012
    
    #para usarr mas descriptivas a traves de swagger
    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "A new book",
                "author":"codinwithAlexis",
                "description":"A new description of a book",
                "rating":5
                
            }
        }
    }
    
    
    
        

    
BOOKS = [
    
    BOOK(1, 'computer science pro', 'codingwithalexis', 'a very nice book', 5,2024),
    BOOK(2, 'be fast wth fastapi', 'codingwithalexis', 'a great book', 5,2025),
    BOOK(3, 'master endpoints', 'codingwithalexis', 'a awesone book', 5,2023),
    BOOK(4, 'HP1', 'author 1', 'book description', 2,2022),
    BOOK(5, 'HP2', 'author 2', 'book description', 3,2021),
    BOOK(6, 'HP3', 'author 3', 'book description', 1,2019)
    
]



@app.get("/books")
async def read_all_books():
    return BOOKS

#BUSQUEDA POR ID parametro de ruta

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
        
#BUSQUEDA POR RATING parametro de consulta     
        
@app.get("/books/")
async def read_book_by_rating(book_rating:int):
    books_to_return = [] # cre ala lista vacia
    for book in BOOKS: #por cada libro en la lista de libros
        if book.rating == book_rating: #si el rating del libro es coincide con el rating
            books_to_return.append(book) #agrega a la lista de libros e libro
    return books_to_return# retorna el libro agregado



    
 # ESTA FUNCION POST DEVUELVE NULL SIN EMBARGO UNA RESPUESTA DE 200
 # SE PUEDE CONSULTAR EL NUEVO LIBRO EN LA LISTA
 #BODY NO AÑADE VALIDACIONES A LLA APP,ACEPTA VALORES CUALQUIERA
 # ESO SE PUEDE CORREGIR PARA EVITAR ERRORES EN EL MANEJO DEL USUARIO
 #CON PYDANTIC SE MUESTRA EL ESQUEMA 
 

@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book = BOOK(**book_request.model_dump())
    #print(type(new_book))
    # pasa la funcion de encontrar id y añadir a la lista nueva
    BOOKS.append(find_book_id(new_book)) 
    
    
    
    # funcion normal para que el id sea incrmental
    # si el id es mayor que cero,entonces firmar el id 
    # de libro al ultimo elemento de la lista[-1] mas uno
    
def find_book_id(book: BOOK):
        if len(BOOKS) > 0:
        #si la longuitud del id es mayor a cero graba al ultimo elemento mas 1
        # esto es para hacerlo consecutivo o incremental    
            book.id = BOOKS[-1].id +1
        else:
            # sino lo crea con el id 1 ya que seria el primero de la lista
            book.id = 1
        return book
    
    # otra forma de hacerlo mas sencillo es:
"""   
def find_book_id(book:BOOK):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book"""
    
    
    
# ACTUALIZAR UN LIBRO

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            # mejora para devolver un mensaje de respuesta
            return {"message": "Book updated"}
    return {"error": "Book not found"}

            
            
            

# BORRAR UN LIBRO
            
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
        
        
        
    

            
            
            
    

    
    

    
    
    
    
    
    
    
    