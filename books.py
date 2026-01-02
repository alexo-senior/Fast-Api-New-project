from fastapi import Body, FastAPI, HTTPException

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'science'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'history'},
    {'title': 'Title four', 'author': 'Author four', 'category': 'math'},
    {'title': 'Title five', 'author': 'Author five', 'category': 'math'},
    {'title': 'Title six', 'author': 'Author two', 'category': 'math'},
]

# tipo de solicitud , siempre debe ir arriba especificando
"""@app.get("/")
#@app.get("/api-endpoint") # para ver el mensaje se debe digitar la palabra
async  def first_api():
    return {"message": "Hello Alexis"}"""


@app.get("/books")
async def read_all_books():
    return BOOKS

 # Esta funcion se debe crear antes de la que contiene el parametro dinamico
 # Esto para evitar que no sea leida por FastApi

@app.get("/books/my_book")
async def read_all_books():
    return {'book_title':'my favorite book!'}

 # Parametros dinamicos
 # El endpoint debe coincidir con el valor del parametro que pase a la funcion
 # a lo que esta dentro del corchete se le puede pasar cualquier valor
   # se puede tipar para que sea str o int

"""@app.get("/books/{dynamic_param}")
async  def read_all_books(dynamic_param: str):
    return {'dynamic_param': dynamic_param}"""


 #PARAMETRO DINAMICO PARA BUSCAR TITULO DEL LIBRO

@app.get("/books/{book_title}") # cambio a busqueda por titulo
async  def read_all_book(book_title: str):
    for book in BOOKS: # recorre la lista de libros
        if book.get('title' ).casefold() == book_title.casefold(): # hace coincidir la cadena en minuscula
            return book
    raise HTTPException(status_code=404, detail="Book not found") # de esta forma se manejan los errores 404 



    # QUERY PARAMETERS ARE REQUEST PARAMETERS THAT HAVE BEEN ATTACHED AFTER A "?" IN THE URL
    # QUERY PARAMETERS HAVE NAME= VALUE PAIRS
    # EXAMPLE: 127.0.0.1:8000/BOOKS/?CATEGORY=SCIENCE

    # torod lo que esta despues de la barra y no es ruta, es un parametro de consulta o query parameter
    # y debe estar dentro de la funcion

@app.get("/books/")
async def read_category_by_query(category:str):
    books_to_return = [] # lista vacia para agregar los libros que coincidan con la categoria
    for books in BOOKS:
        if books.get('category').casefold() == category.casefold():
            books_to_return.append(books) #agrega los libros 
    return books_to_return #retorna la lista de los libros que coincidadn con la categoria

    # con parametro tipo query, sin parametro dinamico
    # este endpoint se movio a esta posicion para evitar que se pdieran mas parametros
    # como el endpoint de abajo que pide author y categoria
    #LOS ENDPOINTS MAS PEQUEÑOS SE COLOCAN ANTES DE LOS MAS  GRANDES 

@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return




    # Combinando parametros de ruta y y de consulta o query parameters 
    #se usa el parametro de ruta para ubicar el autor y el parametro de consulta para saber la categoria 

@app.get("/books/{book_author}/") #parametro de ruta dianmico   
async def read_author_by_category_by_query(book_author: str, category: str): #parametros de consulta
    books_to_return = []
    for books in BOOKS:
        if books.get('author').casefold() == book_author.casefold() and \
                books.get('category').casefold() == category.casefold():
            books_to_return.append(books)
    return books_to_return 
    
    
    # Body corresponde al cuerpo de lo que estamos creando
    #Metodd post o crear

@app.post("/book/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# Metodo update o editar
@app.put("/book/update_book")
async def update_book(update_book=Body()):
    for i in range (len(BOOKS)):
    # si el titulo recorrido coincide
        if BOOKS [i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book # actualiza el libro cuyo titulo


 # metodo Delete o eliminar

@app.delete("/book/delete_book{book_title")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i) #pop elimina el ultimo elemento y lo devuelve
            break # corta el ciclo o bucle



"""
Get all books from a specific author using path or query parameters
"""

 # de esta forma es un con parametro de ruta o dinamico

@app.get("/book/byauthor/{author}")
async def read_books_by_author_path(author:str):
    books_to_return =[]
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return










    
    
