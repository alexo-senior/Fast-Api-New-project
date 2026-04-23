

import pytest


# ejemplo de prueba unitaria con pytest
# assert evalua si la expresión es verdadera, si no lo es, lanza un error
def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
    
    
def test_is_instancece():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)
    

def test_boolean():
    validated = True
    assert validated is True
    assert ('Hello' == 'World') is False
    

# la funcion assert solo acepta un argumento, 
# por lo que no se pueden comparar dos valores directamente, 
# sino que se debe evaluar la expresión y luego pasar el resultado a assert
def test_type():
    assert type('Hello') is str
    assert type('World') is not int
    

def test_greater_than_and_less_than():
    assert 7 > 3
    assert 4 < 10
    
    
def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False] # declara que todos los elementos son False
    assert 1 in num_list # es verdadero 1 esta en la lista
    assert 7 not in num_list # es verdadero que no esta en la lista
    assert all(num_list) # es verdadero porque todos los elementos de la lista son verdaderos (no son 0, False, None, etc.)
    assert not any(any_list) # es verdadero porque ninguno de los elementos de la lista es verdadero (todos son False)
    
    
    
    # crea una clase estudiante un objeto con atributos y prueba su instancia y tipo de dato
class Student:
    def __init__(self, first_name: str,last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

# con pyytest fixture se puede crear una función que inicialice el objeto estudiante y 
# luego usar esa función en las pruebas, evitando así repetir la instancia del objeto en cada prueba.
# se usa un decorador @pytest.fixture para indicar que la función es un fixture, y luego se puede usar 
# el nombre de la función como argumento en las pruebas para acceder al objeto inicializado.

@pytest.fixture
def defaul_employee():
    return Student('Alexis', 'ibarra', 'Python Programming', 3)


    # crea un funcion para inicializaar el objeto estudiante
    # se incluye la funcion decorradora para que automaatice la inicializacion del objeto estudiante 
    # en cada prueba que lo necesite, evitando asi repetir el codigo de inicializacion en cada prueba.
    
"""def test_student(defaul_employee):
    p = Student('Alexis', 'ibarra', 'Python Programming', 3) # instancia de la clase estudiante con p como objeto
    assert p.first_name == 'Alexis', 'First name should be Alexis'
    assert p.last_name == 'ibarra', 'Last name should be ibarra'
    assert p.major == 'Python Programming', 'Major should be Python Programming' 
    assert p.years == 3, 'Years should be 3'
    """
"""Es de notar que se instancia el objeto p con la clase Student, y luego se prueban sus atributos con assert,
    sin embargo puede que unna clase tenga varias pruebas y no se quiera repetir la instancia del objeto en cada prueba,
    por lo que se puede usar un fixture de pytest"""
    
    #elimina la instancia del objeto estudiante en la prueba y usa el fixture para acceder al objeto inicializado,
    # lo que hace que el codigo sea mas limpio y facil de mantener, ya que si se necesita cambiar la instancia del 
    # objeto estudiante, solo se tiene que cambiar en el fixture y no en cada prueba que lo use.
    
def test_student(defaul_employee):
    p = Student('Alexis', 'ibarra', 'Python Programming', 3) # instancia de la clase estudiante con p como objeto
    assert defaul_employee.first_name == 'Alexis', 'First name should be Alexis'
    assert defaul_employee.last_name == 'ibarra', 'Last name should be ibarra'
    assert defaul_employee.major == 'Python Programming', 'Major should be Python Programming' 
    assert defaul_employee.years == 3, 'Years should be 3'
    
    

        