import csv
import os

#Limpiar espacios y convertir el título a minúsculas para comparar.
def normalizar_titulo(titulo):
    return " ".join(titulo.split()).lower()

def es_entero_no_negativo(texto):
    return texto.isdigit()

#Cargar y guardar catálogo.
def cargar_catalogo(nombre_archivo):
    catalogo = []
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                titulo = fila.get("TITULO", "").strip()
                cantidad = fila.get("CANTIDAD", "").strip()
                if titulo != "" and es_entero_no_negativo(cantidad):
                    catalogo.append({"TITULO": titulo, "CANTIDAD": int(cantidad)})
    return catalogo

# Guardar el catálogo en el archivo CSV.
def guardar_catalogo(catalogo):
    with open("catalogo.csv", "w", newline="", encoding="utf-8") as archivo:
        campos = ["TITULO", "CANTIDAD"]
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for libro in catalogo:
            escritor.writerow(libro)

# Buscar un libro por título.
def buscar_libro(catalogo, titulo):
    titulo_normalizado = normalizar_titulo(titulo)
    for libro in catalogo:
        if normalizar_titulo(libro["TITULO"]) == titulo_normalizado:
            return libro
    return None

# Mostrar todos los libros del catálogo.
def mostrar_catalogo(catalogo):
    if not catalogo:
        print("El catálogo está vacío.\n")
        return
    print("\n--- CATÁLOGO COMPLETO ---")
    for libro in catalogo:
        print(f"{libro['TITULO']} → {libro['CANTIDAD']} ejemplares")
    print()

# Mostrar los libros agotados (cantidad == 0).
def listar_agotados(catalogo):
    print("\nLibros agotados:")
    agotados = [libro for libro in catalogo if libro["CANTIDAD"] == 0]
    if agotados:
        for libro in agotados:
            print(f"- {libro['TITULO']}")
    else:
        print("No hay libros agotados.")

# Consultar cuántos ejemplares hay de un título.
def consultar_disponibilidad(catalogo):
    titulo = input("Ingresá el título a consultar: ")
    libro = buscar_libro(catalogo, titulo)
    if libro:
        print(f"Ejemplares disponibles de '{libro['TITULO']}': {libro['CANTIDAD']}")
    else:
        print("El título no existe en el catálogo.")

# Carga múltiples títulos nuevos.
def ingresar_titulos(catalogo):
    while True:
        cantidad = input("¿Cuántos libros querés cargar?: ")
        if cantidad.isdigit() and int(cantidad) > 0:
            cantidad = int(cantidad)
            break
        else:
            print("Ingresá un número entero mayor a 0.")

    for _ in range(cantidad):
        while True:
            titulo = input("Título: ").strip()
            if not titulo:
                print("El título no puede estar vacío.")
                continue
            if buscar_libro(catalogo, titulo):
                print("Ese título ya existe. Ingresá uno diferente.")
                continue
            break
        catalogo.append({"TITULO": titulo, "CANTIDAD": 0})
        print(f"Libro '{titulo}' agregado con cantidad inicial 0.")


# Agregar un solo título nuevo.
def agregar_titulo(catalogo):
    titulo = input("Título: ").strip()
    if not titulo:
        print("El título no puede estar vacío.")
        return
    if buscar_libro(catalogo, titulo):
        print("Ese título ya existe.")
        return
    catalogo.append({"TITULO": titulo, "CANTIDAD": 0})
    print(f"Libro '{titulo}' agregado con cantidad inicial 0.")

# Sumar ejemplares a un título existente.
def ingresar_ejemplares(catalogo):
    titulo = input("Título al que querés agregar ejemplares: ")
    libro = buscar_libro(catalogo, titulo)
    if libro:
        while True:
            cant = input("¿Cuántos ejemplares querés agregar?: ").strip()
            if cant.isdigit() and int(cant) > 0:
                libro["CANTIDAD"] += int(cant)
                print("Ejemplares actualizados.")
                break
            else:
                print("Ingresá un número entero mayor a 0.")
    else:
        print("El título no existe.")


# Actualizar ejemplares por préstamo o devolución.
def actualizar_ejemplares(catalogo):
    titulo = input("Título a actualizar: ").strip()
    libro = buscar_libro(catalogo, titulo)
    if not libro:
        print("El título no existe.")
        return
    print("1. Préstamo\n2. Devolución")
    opcion = input("Elige una opción (escribe 1 o 2): ")
    match opcion:
        case "1":
            if libro["CANTIDAD"] > 0:
                libro["CANTIDAD"] -= 1
                print("Préstamo registrado.")
            else:
                print("No hay ejemplares disponibles.")
        case "2":
            libro["CANTIDAD"] += 1
            print("Devolución registrada.")
        case _:
            print("Opción inválida.")

# Menú principal
def menu():
    nombre_archivo = "catalogo.csv"
    catalogo = cargar_catalogo(nombre_archivo)
    print("Bienvenido al sistema de la biblioteca.")

    while True:
        print("\n--- MENÚ ---")
        print("1. Cargar múltiples títulos.")
        print("2. Ingresar ejemplares.")
        print("3. Mostrar catálogo.")
        print("4. Consultar disponibilidad.")
        print("5. Listar agotados.")
        print("6. Agregar título.")
        print("7. Actualizar ejemplares (préstamo/devolución).")
        print("8. Salir.")

        opcion = input("Elegí una opción: ")

        match opcion:
            case "1":
                ingresar_titulos(catalogo)
                guardar_catalogo(catalogo)
            case "2":
                ingresar_ejemplares(catalogo)
                guardar_catalogo(catalogo)
            case "3":
                mostrar_catalogo(catalogo)
            case "4":
                consultar_disponibilidad(catalogo)
            case "5":
                listar_agotados(catalogo)
            case "6":
                agregar_titulo(catalogo)
                guardar_catalogo(catalogo)
            case "7":
                actualizar_ejemplares(catalogo)
                guardar_catalogo(catalogo)
            case "8":
                print("Programa finalizado. ¡Hasta la próxima!")
                break
            case _:
                print("Opción inválida. Intentá de nuevo.")

menu()
