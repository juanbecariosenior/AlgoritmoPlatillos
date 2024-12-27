import csv

ruta_archivo = "C:/Users/Becario/Desktop/entrada.csv"

with open(ruta_archivo, mode="r",encoding="utf-8") as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    for fila in lector:
        id_mesa = fila["ID"]
        mesa = fila["Mesa"]
        personas = int(fila["Comensales"])
        monto_final = float(fila["Total"])

        print(f"ID: {id_mesa},Mesa: {mesa},Personas:{personas}, Monto Final: {monto_final:.2f}")