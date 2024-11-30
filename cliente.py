import requests

#------------------------------------------------------------------------------------------------
#------------- Etapa 3: Desarrollar el cliente API ----------------------------------------------
#------------------------------------------------------------------------------------------------

#IP del servidor a utilizar
server_ip = "127.0.0.1"

def menu():
    print("\nMenú: ")
    print("1. Buscar libro por título.")
    print("2. Buscar libro por autor.")
    print("3. Agregar un libro.")
    print("4. Eliminar un libro por título.")
    print("5. Eliminar un libro por autor.")
    print("6. Ver todos los libros.")
    print("7. Actualizar libro por titulo.")
    print("8. salir.")
    
    rta = 10
    while rta <= 0 or rta > 8:
        rta = int(input("\nSeleccione una opción: "))
        if rta <= 0 or rta > 8:
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
        delete_book_by_author()
        return
    elif (rta == 6):
        get_books()
        return
    elif (rta == 7):
        update_book()
        return
    elif (rta == 8):
        return 1

def search_book_by_title():
    title = input("Ingrese el titulo a buscar: ")
    response = requests.get(f"http://{server_ip}:8000/books/title/{title}")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
    datos = response.json()
    print(datos)

def search_book_by_author():
    author = input("Ingrese el titulo a buscar: ")
    response = requests.get(f"http://{server_ip}:8000/books/author/{author}")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
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

    response = requests.post(f"http://{server_ip}:8000/books", json = libro)
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
    datos = response.json()
    print(datos)

def delete_book_by_title():
    title = input("Ingrese el titulo: ")
    response = requests.delete(f"http://{server_ip}:8000/books/by-title?title={title}")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
    datos = response.json()
    print(datos)

def delete_book_by_author():
    author = input("Ingrese el autor: ")
    response = requests.delete(f"http://{server_ip}:8000/books/by-author?author={author}")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
    datos = response.json()
    print(datos)

def get_books():
    response = requests.get(f"http://{server_ip}:8000/books")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return
    datos = response.json()
    print(datos)

def update_book():
    title = input("Ingrese el título del libro que desea actualizar: ")
    response = requests.get(f"http://{server_ip}:8000/books/title/{title}")
    if response.status_code == 404:
        print(f"Error: {response.json()['detail']}")
        return

    # Muestra los datos actuales del libro
    book = response.json()
    print("Detalles actuales del libro:")
    for key, value in book.items():
        print(f"{key}: {value}")

    # Te da a elegir que valor del libro querés actualizar
    print("\n¿Qué valor desea actualizar? (Escriba el campo exacto o presione Enter para salir)")
    print("Opciones:", ", ".join(book.keys()))
    field = input("Campo a actualizar: ")
    
    if field not in book:
        print("Campo inválido o vacío. Operación cancelada.")
        return
    
    # Solicita el nuevo valor para el campo
    new_value = input(f"Ingrese el nuevo valor para '{field}' (Actual: {book[field]}): ")

    # Intenta convertir el nuevo valor al tipo original (si es int, por ejemplo)
    if isinstance(book[field], int):
        try:
            new_value = int(new_value)
        except ValueError:
            print("El valor ingresado no es un número válido. Operación cancelada.")
            return

    # Actualiza el valor del libro
    book[field] = new_value

    # Realiza la solicitud PUT al servidor
    response = requests.put(f"http://{server_ip}:8000/books/{title}", json=book)
    
    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print(f"Error: {response.json()['detail']}")


##############################################

print("Iniciando ejecución. . .")
salida = 0
while(salida != 1):
    salida = menu()