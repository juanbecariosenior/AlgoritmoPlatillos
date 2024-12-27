import pyodbc
import time
import sys
import csv
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options

# Ajustar el límite de recursión
sys.setrecursionlimit(2000)

ruta_archivo = "C:/Uipath/MesasWebJuan/entrada.csv"

def leer_monto_final(ruta_csv):
    with open(ruta_csv, mode="r",encoding="utf-8") as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            return float(fila["Total"])

# Función para conectar a la base de datos y obtener los platillos
def obtener_platillos_servidor(total_max):
    conexion = pyodbc.connect(
        "DRIVER={SQL};"
        "SERVER=servidor;"
        "DATABASE=base;"
        "UID=usuario;"
        "PWD=password;"
    )

    cursor = conexion.cursor()

    # Consulta con parámetro
    consulta = "SELECT Cod,Descripcion, Precio FROM RE_Platillos WHERE Precio > 1.00 AND Precio <= ? and Combo <> 1 and Descripcion not like '%Tiempo%' and Descripcion not like '%paquete%'"
    cursor.execute(consulta, total_max)

    datos = cursor.fetchall()

    conexion.close()

    if not datos:
        raise ValueError("No se encontraron platillos en la base de datos que cumplan con los criterios.")

    return {cod : (descripcion,precio)  for cod,descripcion,precio in datos if precio <= total_max}

# Función para encontrar la mejor combinación de platillos
def encontrar_mejor_combinacion(platillos, total):
    # Ordenar los platillos por precio de mayor a menor
    platillos_ordenados = sorted(platillos.items(), key=lambda x: x[1], reverse=True)

    mejor_combinacion = []
    mejor_suma = 0

    def backtrack(suma_actual, combinacion_actual, inicio):
        nonlocal mejor_combinacion, mejor_suma
        # Si la suma actual es igual al total, se encontró la combinación exacta
        if suma_actual == total:
            mejor_combinacion = list(combinacion_actual)
            mejor_suma = suma_actual
            return True  # Detener la recursión

        # Si la suma actual es mejor (sin pasarse del total), actualizar
        if suma_actual <= total and suma_actual > mejor_suma:
            mejor_combinacion = list(combinacion_actual)
            mejor_suma = suma_actual

        # Intentar agregar más platillos
        for i in range(inicio, len(platillos_ordenados)):
            cod, precio = platillos_ordenados[i]

            if suma_actual + precio > total:  # Si la suma excede el total, no seguir
                continue

            combinacion_actual.append((cod))
            if backtrack(suma_actual + precio, combinacion_actual, i + 1):  # Recursión
                return True  # Si se encontró la combinación exacta, terminar
            combinacion_actual.pop()

        return False  # Si no se encontró la combinación exacta

    # Iniciar el proceso de backtracking
    backtrack(0, [], 0)

    return mejor_combinacion

try:
    total = leer_monto_final(ruta_archivo)
    print(f"Total leido del archivo: {total}")

    # Lista de platillos con sus precios
    platillos = obtener_platillos_servidor(total)

    inicio_tiempo = time.time()

    # Buscar la mejor combinación
    resultado = encontrar_mejor_combinacion(platillos, total)

    fin_tiempo = time.time()

    # Mostrar resultados
    if resultado:
        print("Codigos Platillos seleccionados:")
        for cod in resultado:
            print(f"- {cod}")
    else:
        print("No se encontró una combinación exacta.")

    # Mostrar tiempo de ejecución
    tiempo_ejecucion = fin_tiempo - inicio_tiempo
    print(f"Tiempo de ejecución: {tiempo_ejecucion:.4f} segundos")

    fecha_hora_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    nombre_carpeta = f"resultados_{fecha_hora_actual}"

    ruta_carpeta = os.path.join("C:\Uipath\MesasWebJuan", nombre_carpeta)

    os.makedirs(ruta_carpeta,exist_ok=True)

    ruta_archivo_csv = os.path.join(ruta_carpeta,"resultado_platillos.csv")

    with open(ruta_archivo_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(["Cod"])  # Escribir encabezados
        for cod in resultado:
            escritor.writerow([cod])  # Escribir filas de resultados
          # Escribir el total

    print(f"Resultados guardados en: {ruta_archivo_csv}")

except ValueError as e:
    print(f"Error: {e}")












