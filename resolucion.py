from fastapi import FastAPI
import uvicorn
import requests
import os
import pandas as pd


#---------------------------------------------------------------------------
#------------- ETAPA N° 01: Elección y consulta de los datos ---------------
#---------------------------------------------------------------------------

# Realiza la lectura a la API
url = 'https://raw.githubusercontent.com/benoitvallon/100-best-books/refs/heads/master/books.json'
filename = 'books.json'

# Verificar si el archivo ya existe
if os.path.exists(filename):
    print(f"El archivo '{filename}' ya existe en el directorio actual. No se descargará nuevamente.")
else:
    try:
        # Descargar el contenido del archivo
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepcion si la solicitud fallo
        
        # Convierte la respuesta JSON en una lista de diccionarios
        datos = response.json()
        # Guardar el archivo en el directorio actual
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Archivo '{filename}' descargado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")

datos = pd.read_json("books.json")
#---------------------------------------------------------------------------
#------------- ETAPA N° 02: Desarrollo del servidor API --------------------
#---------------------------------------------------------------------------

def menu():
    print("Menú: \n")
    print("1. Buscar libro por título.")
    print("2. Buscar libro por autor.")
    print("3. Agregar un libro.")
    print("4. Eliminar un libro.")
    print("5. salir.")
    
    rta = 7
    while rta <= 0 or rta > 6:
        rta = int(input("\n Seleccione una opción: "))
        if rta <= 0 or rta > 6:
            print("Error. Ingresar un valor valido")     

    if (rta == 1):
        opcion_1()
        return
    elif (rta == 2):
        opcion_2()
        return
    elif (rta == 3):
        opcion_3()
        return
    elif (rta == 4):
        opcion_4()
        return
    elif (rta == 5):
        opcion_5()
        return 1

def opcion_1():
    pass

def opcion_2():
    print("\n Usted ha seleccionado la opción 2.")
    autor = "Chinua Achebe"
    lista = []

    for dato in datos:
        if (dato["author"].lower() == autor.lower()):
            if (dato["title"] not in lista):
                lista.append(dato["title"])
        
    if (len(lista) == 0):
        print("No se encontraron coincidencias.")
    else:
        print(f"¡Se encontraron", len(lista), "coincidencia/s!")
        for titulos in lista:
            print(titulos)

    return 

def opcion_3():
    pass

def opcion_4():
    pass

def opcion_5():
    print("El menú fue cerrado exitosamente!")
    return

def verificar_datos(rta):
    print("Error. Ingresar un valor valido")
    while rta < 0 and rta > 6:
        print("Menú: \n")
        print("1. Buscar libro por título.")
        print("2. Buscar libro por autor.")
        print("3. Agregar un libro.")
        print("4. Eliminar un libro.")
        print("5. salir.")

        rta = input("\n Seleccione una opción: ")

    return 

#---------------------------------------------------------------------------

print("Iniciando ejecución. . .")
salida = 0
while(salida != 1):
    salida = menu()




#---------------------------------------------------------------------------

#{
# "author": "Chinua Achebe",
# "country": "Nigeria",
# "imageLink": "images/things-fall-apart.jpg",
# "language": "English",
# "link": "https://en.wikipedia.org/wiki/Things_Fall_Apart\n",
# "pages": 209,
# "title": "Things Fall Apart",
# "year": 1958
#}

libros = 0
autores = []

for dato in datos:
    libros +=1
    if dato["author"] not in autores:
        autores.append(dato["author"])

print("Cantidad de libros: ", libros)
print("Cantidad de autores únicos:", len(autores))



print("\n Usted ha seleccionado la opción 2.")
autor = input("Ingrese el nombre del autor: ")
lista = []

for dato in datos:
    if (dato["author"] == autor):
        if (dato["title"] not in lista):
            lista.append(dato["title"])
    
if (len(lista) == 0):
    print("No se encontraron coincidencias.")
else:
    print(f"¡Se encontraron", len(lista), "coincidencia/s!")
    for titulos in lista:
        print(titulos)
    
