from typing import Optional
from fastapi import FastAPI,Path,Query , HTTPException
 # validaciones
from pydantic import BaseModel, Field 
from starlette import status 



app = FastAPI(
    title="Mi aplicacion de FastApi",
    description="Esta es una aplicacion para manejo de libros con FastApi",    
    version= "1.0.0")



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
    # aceptamos el alias "published_data" desde el JSON
    published_date: int = Field(gt=1999, lt=2031, alias="published_data")
    
    # para usar ejemplos descriptivos en Swagger y permitir alias
    model_config = {
        "populate_by_name": True,# se hace para aceptar alias, por si hay errores de nombres
        "json_schema_extra": {
            "example":{
                "title": "A new book",
                "author":"codinwithAlexis",
                "description":"A new description of a book",
                "rating":5,
                "published_data": 2029 # aqui coloque el alias data en vez de date
            }
        }
    }
    
    
    
        

    
BOOKS = [
    
    BOOK(1, 'computer science pro', 'codingwithalexis', 'a very nice book', 5,2030),
    BOOK(2, 'be fast wth fastapi', 'codingwithalexis', 'a great book', 5,2030),
    BOOK(3, 'master endpoints', 'codingwithalexis', 'a awesone book', 5,2029),
    BOOK(4, 'HP1', 'author 1', 'book description', 2,2028),
    BOOK(5, 'HP2', 'author 2', 'book description', 3,2027),
    BOOK(6, 'HP3', 'author 3', 'book description', 1,2026)
    
]



@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#BUSQUEDA POR ID parametro de ruta

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):# añade la validacion extra a parametros de ruta 
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")# si no encuentra el libro devuelve error 404
        
#BUSQUEDA POR RATING parametro de consulta     
        
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):# 
    books_to_return = [] # cre ala lista vacia
    for book in BOOKS: #por cada libro en la lista de libros
        if book.rating == book_rating: #si el rating del libro es coincide con el rating
            books_to_return.append(book) #agrega a la lista de libros e libro
    return books_to_return# retorna el libro agregado



# CONSULTAR LIBRO POR FECHA DE PUBLICACION, ULTIMO ENDPOINT

@app.get("/book/published", status_code=status.HTTP_200_OK)
async def read_books_by_published_date(published_date:int = Query(gt=1999, lt=2031)):# añade validacion para la fecha de publicacion
    books_to_return =[] # crea una lista vacia, espera ser llenada 
    for book in BOOKS:# recorre la lista de libros
        if book.published_date == published_date:# si esta coincide con la fecha de publicacion
            books_to_return.append(book) #agrega el libro a la lista 
    return books_to_return # retorna la lista de libros encontrados con esa fecha
            
    



    
 # ESTA FUNCION POST DEVUELVE NULL SIN EMBARGO UNA RESPUESTA DE 200
 # SE PUEDE CONSULTAR EL NUEVO LIBRO EN LA LISTA
 #BODY NO AÑADE VALIDACIONES A LLA APP,ACEPTA VALORES CUALQUIERA
 # ESO SE PUEDE CORREGIR PARA EVITAR ERRORES EN EL MANEJO DEL USUARIO
 #CON PYDANTIC SE MUESTRA EL ESQUEMA 
 

@app.post("/create-book", status_code=status.HTTP_201_CREATED)
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

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)# devuelve 204 porque fue exitosa la modificacion
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            
            # mejora para devolver un mensaje de respuesta
    if not book_changed:
        raise HTTPException(status_code=404, detail=' Item not found to update')        
    

            
            
            

# BORRAR UN LIBRO
            
@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):# añade validacion para eliminar solo los libros con id mayor a cero  
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail=' Item not found to delete')
        
    # en el caso de update y delete no se retorna nada porque el codigo 204
    # indica que la operacion fue exitosa pero no hay contenido que devolver
        
        
        

        
            
        
        
        
    

            
            
            
    

    
    

    
    
    
    
    
    
    
    