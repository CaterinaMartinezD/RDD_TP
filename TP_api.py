from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
import json

#------------------------------------------------------------------------------------------------
#------------- ETAPA N° 01: Elección y consulta de los datos ------------------------------------
#------------------------------------------------------------------------------------------------

url = 'https://raw.githubusercontent.com/benoitvallon/100-best-books/refs/heads/master/books.json'
filename = 'books.json'

# Verificar si el archivo ya existe
if os.path.exists(filename):
    print(f"El archivo '{filename}' ya existe en el directorio actual. No se descargará nuevamente.")
    with open(filename, "r", encoding="utf-8") as file:
        datos = json.load(file) 
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

#------------------------------------------------------------------------------------------------
#------------- ETAPA N° 02: Desarrollo del servidor API -----------------------------------------
#------------------------------------------------------------------------------------------------

app = FastAPI() # Inicia la aplicación FastAPI

# Función para leer el contenido del archivo JSON
def get_books():
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Función para guardar datos en el archivo JSON
def save_books(data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# Modelo para validar los datos de un libro
'''
class Book(BaseModel):
    author: str
    country: str
    imageLink: str
    language: str
    link: str
    pages: int
    title: str
    year: int
'''

################################################################
# Función para visualizar el menú
@app.get("/")
def menu():
    return { "Menú" : [{"N° 01. Buscar libro por título" : "/books/title/NOMBRE_LIBRO"}, {"N° 02. Buscar libro por autor" : "/books/author/NOMBRE_AUTOR"}, 
                        {"N° 03. Agregar un libro por titulo" : "COMPLETAR"}, {"N° 04. Eliminar un libro" : "/books"},
                        {"N° 05. Eliminar un libro por autor" : "/books"}, {"N° 06. Listado de libros" : "/books"}]}

################################################################
# Función para ver listado de libros
@app.get("/books")
def leer_archivo():
    datos = get_books()
    return {"books": datos}

################################################################
# GET: Busca un libro por título
@app.get("/books/title/{title}")
def buscar_titulo(title: str):
    datos = get_books()
    libros = [libro for libro in datos if libro["title"].lower() == title.lower()]

    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron coincidencias")

    # Si solo hay un libro, devuelve ese directamente
    if len(libros) == 1:
        return libros[0]

    # Si hay más de un libro (casos raros), devuelve todos
    return libros

################################################################
# GET: Busca un libro por autor
@app.get("/books/author/{author}")
def buscar_autor(author: str):
    datos = get_books()

    # Filtrar libros por autor (ignorando mayúsculas/minúsculas)
    libros = [libro for libro in datos if libro["author"].lower() == author.lower()]

    # Si no se encuentra ningún libro, lanzar excepción
    if not libros:
        raise HTTPException(status_code=404, detail="No se encontraron libros para el autor especificado.")

    # Si se encuentra un único libro, devolverlo directamente
    if len(libros) == 1:
        return libros[0]

    # Si hay múltiples libros, devolver la lista completa
    return libros

################################################################
# POST: Agregar un nuevo libro
@app.post("/books")
def agregar_libro(libro: dict):
    # Recupera los libros
    datos = get_books()
    
    # Itera los libros y busca que no haya uno con el mismo titulo
    for existing_book in datos:
        if existing_book["title"] == libro["title"]:
            raise HTTPException(status_code=400, detail=f"El libro '{libro["title"]}' ya existe.")
    # Si no lo hay, lo agrega
    datos.append(libro)
    save_books(datos)
    return {"message": f"Libro '{libro["title"]}' agregado exitosamente."}

################################################################
# DELETE: Eliminar un libro por su titulo
@app.delete("/books/by-title")
def eliminar_libro_titulo(title):
    datos = get_books()   # Recupera los libros

    # Itera los libros y verifica si existe
    for libro in datos:
        if libro["title"].lower() == title.lower():
            datos.remove(libro)
            save_books(datos)
            return {"message": f"El libro '{title}' fue eliminado exitosamente."}
        
    save_books(datos)
    return {"message": f"El libro '{title}' no fue encontrado."}

################################################################
# DELETE: Eliminar un libro por el autor
@app.delete("/books/by-author")
def eliminar_libro_autor(author):
    datos = get_books()   # Recupera los libros
    
    # Itera los libros y  verifica si existe
    for libro in datos:
        if libro["author"].lower() == author.lower():
            datos.remove(libro)
            save_books(datos)
            return {"message": f"El autor '{author}' fue eliminado exitosamente."}
        
    save_books(datos)
    return {"message": f"El autor '{author}' no fue encontrado."}

################################################################
# PUT: Actualizar un libro buscando por el título
@app.put("/books/{title}")
def update_book(title: str, libro: dict):
    libros = get_books()

    for index, existing_book in enumerate(libros):
        if existing_book["title"] == title:
            libros[index] = libro
            save_books(libros)
            return {"message": f"Libro '{title}' actualizado exitosamente."}
    raise HTTPException(status_code=404, detail=f"El libro '{title}' no se encontró.")

################################################################