import requests

def menu():
    print("\nMenú: \n")
    print("1. Buscar libro por título.")
    print("2. Buscar libro por autor.")
    print("3. Agregar un libro.")
    print("4. Eliminar un libro por titulo.")
    print("5. Ver todos los libros.")
    print("6. salir.")
    
    rta = 7
    while rta <= 0 or rta > 6:
        rta = int(input("\n Seleccione una opción: "))
        if rta <= 0 or rta > 6:
            print("Error. Ingresar un valor valido")     

    if (rta == 1):
        search_book_by_title()
        return
    elif (rta == 2):
        search_book_by_author()
        return
    elif (rta == 3):
        append_book()
        return
    elif (rta == 4):
        delete_book_by_title()
        return
    elif (rta == 5):
        get_books()
        return
    elif (rta == 6):
        return 1


def search_book_by_title():
    title = input("Ingrese el titulo a buscar: ")
    response = requests.get(f"http://127.0.0.1:8000/books/title/{title}")
    datos = response.json()
    print(datos)

def search_book_by_author():
    author = input("Ingrese el titulo a buscar: ")
    response = requests.get(f"http://127.0.0.1:8000/books/author/{author}")
    datos = response.json()
    print(datos)

def append_book():
    author = input("Ingrese el autor: ")
    country = input("Ingrese el pais: ")
    imageLink = input("Ingrese un link la imagen: ")
    language = input("Ingrese el lenguaje: ")
    link = input("Ingrese el link al libro: ")
    pages = int(input("Ingrese la cantidad de paginas: "))
    title = input("Ingrese el titulo: ")
    year = int(input("Ingrese el año: "))
    libro = {'author': author,
             'country': country,
             'imageLink': imageLink,
             'languaje': language,
             'link': link,
             'pages': pages,
             'title': title,
             'year': year 
            }

    response = requests.post("http://127.0.0.1:8000/books", json = libro)
    datos = response.json()
    print(datos)

def delete_book_by_title():
    title = input("Ingrese el titulo: ")
    response = requests.delete(f"http://127.0.0.1:8000/books?title={title}")
        #f"http://127.0.0.1:8000/books?title={title}")
    datos = response.json()
    print(datos)

def get_books():
    response = requests.get("http://127.0.0.1:8000/books")
    datos = response.json()
    print(datos)

print("Iniciando ejecución. . .")
salida = 0
while(salida != 1):
    salida = menu()