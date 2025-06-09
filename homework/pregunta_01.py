"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Ignorar las primeras 4 líneas (encabezado y líneas vacías)
    lines = lines[4:]

    registros = []
    temp_line = ""

    for line in lines:
        # Detectar si la línea comienza con un número (inicio de un nuevo registro)
        if re.match(r"^\s*\d+", line):
            if temp_line:
                registros.append(temp_line)
            temp_line = line.strip().lstrip('%').strip()  # Eliminar % inicial si aparece
        else:
            # Continuación del texto de palabras clave (multi-línea)
            temp_line += " " + line.strip()

    if temp_line:
        registros.append(temp_line)

    # Crear una lista con los campos extraídos por expresión regular
    data = []
    for reg in registros:
        match = re.match(
            r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s+(.+)$", reg
        )
        if match:
            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras_clave = match.group(4)

            # Limpieza del texto de palabras clave
            palabras_clave = palabras_clave.replace(". ", "")  # eliminar punto final
            palabras_clave = re.sub(r"\s+", " ", palabras_clave)  # espacios redundantes
            palabras_clave = palabras_clave.lstrip('%').strip()  # eliminar % restante

            data.append([cluster, cantidad, porcentaje, palabras_clave])

    columnas = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    # Formatear nombres de columnas
    columnas = [col.lower().replace(" ", "_") for col in columnas]

    df = pd.DataFrame(data, columns=columnas)

    return df

# Prueba visual
print(pregunta_01())
